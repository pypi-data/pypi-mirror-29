"""Python script for performing egta"""
import argparse
import json
import logging
import smtplib
import sys
import traceback
from logging import handlers

from egtaonline import api
from gameanalysis import gamereader

from egta import countsched
from egta import savesched
from egta.script import bootstrap
from egta.script import brute
from egta.script import eosched
from egta.script import gamesched
from egta.script import innerloop
from egta.script import simsched
from egta.script import trace
from egta.script import zipsched


_log = logging.getLogger(__name__)


# TODO Create a scheduler that runs jobs on flux, but without going through
# egta online, potentially using spark
# TODO Add more efficient regret / deviation gains scheduler

def main(*argv):
    parser = argparse.ArgumentParser(
        description="""Command line egta. To run, both an equilibrium finding
        method and a profile scheduler must be specified. Each element
        processes the arguments after it, e.g. `egta -a brute -b game -c` will
        pass -a to the base parser, -b to the brute equilibrium solver, and -c
        to the game profile scheduler.""")

    # Standard arguments
    parser.add_argument(
        '--output', '-o', metavar='<output-file>', type=argparse.FileType('w'),
        default=sys.stdout, help="""The file to write the output to. (default:
        stdout)""")
    parser.add_argument(
        '--verbose', '-v', action='count', default=0, help="""Sets the
        verbosity of commands. Output is send to standard error.""")
    parser.add_argument(
        '-e', '--email_verbosity', action='count', default=0, help="""Verbosity
        level for emails.""")
    parser.add_argument(
        '-r', '--recipient', metavar='<email-address>', action='append',
        default=[], help="""Specify an email address to receive email logs at.
        Can specify multiple email addresses.""")
    parser.add_argument(
        '--count', metavar='<sims>', type=int, default=1, help="""Number of
        simulations to schedule to count towards a single payoff. (default:
        %(default)d)""")
    parser.add_argument(
        '--profile-data', metavar='<gamefile>', help="""If specified, record
        all of the payoff data sampled, and write them as an observation game
        file to the specified location.""")
    parser.add_argument(
        '--support-thresh', metavar='<support-thresh>', type=float,
        default=1e-3, help="""Threshold for a strategy probability to consider
        it in support. (default: %(default)g)""")
    parser.add_argument(
        '--tag', metavar='<identifier>', help="""This tag will be displayed in
        logs to help identify which script the log refers to. If unspecified
        but a Game ID is, then "Game <id>" will be used.""")

    # Egta online authentication
    parser_auth = parser.add_mutually_exclusive_group()
    parser_auth.add_argument(
        '--auth-string', '-a', metavar='<auth-string>', help="""The string
        authorization token to connect to egta online.""")
    parser_auth.add_argument(
        '--auth-file', '-f', metavar='<auth-file>', help="""Filename that just
        contains the string of the auth token.""")

    # Information about the game to sample
    game_spec = parser.add_mutually_exclusive_group(required=True)
    game_spec.add_argument(
        '--game-id', '-g', metavar='<game-id>', type=int, help="""An egtaonline
        game id that specifies that game profile to load. A game profile is a
        configuration, number of players per role, and strategy names per
        roll.""")
    game_spec.add_argument(
        '--game-json', metavar='<game-json>', type=argparse.FileType('r'),
        help="""A game file that must specify the number of players per role,
        and names of all role and strategies in a standard game analysis
        format.""")

    # All of the actual methods to run
    eq_methods = parser.add_subparsers(
        title='operations', dest='method', metavar='<operation>', help="""The
        operation to run on the game. Available commands are:""")
    for module in [innerloop, brute, bootstrap, trace]:
        method = module.add_parser(eq_methods)
        method.run = module.run

        schedulers = method.add_subparsers(
            title='schedulers', dest='scheduler', metavar='<scheduler>',
            help="""The scheduler to use for acquiring samples from profiles.
            Available commands are:""")
        method.sched = schedulers
        for module in [eosched, gamesched, simsched, zipsched]:
            sched = module.add_parser(schedulers)
            sched.create_scheduler = module.create_scheduler

    # Parse args and process
    args = parser.parse_args(argv)
    method = eq_methods.choices[args.method]
    sched = method.sched.choices[args.scheduler]

    if args.auth_string is None and args.auth_file is not None:
        with open(args.auth_file) as auth_file:  # pragma: no cover
            args.auth_string = auth_file.read().strip()

    if args.tag is not None:
        tag = args.tag
    elif args.game_id is not None:
        tag = 'Game {:d}'.format(args.game_id)
    else:
        tag = '?'

    stderr_handle = logging.StreamHandler(sys.stderr)
    stderr_handle.setLevel(50 - 10 * min(args.verbose, 4))
    stderr_handle.setFormatter(logging.Formatter(
        '%(asctime)s {} ({}) %(levelname)s %(message)s'.format(
            args.method, tag)))
    log_handlers = [stderr_handle]

    # Email Logging
    if args.recipient:  # pragma: no cover
        smtp_host = 'localhost'

        # We need to do this to match the from address to the local host name
        # otherwise, email logging will not work. This seems to vary somewhat
        # by machine
        with smtplib.SMTP(smtp_host) as server:
            smtp_fromaddr = 'EGTA Online <egta_online@{host}>'.format(
                host=server.local_hostname)

        email_handler = handlers.SMTPHandler(
            smtp_host, smtp_fromaddr, args.recipient,
            'EGTA Status for {} {}'.format(args.method, tag))
        email_handler.setLevel(50 - args.email_verbosity * 10)
        email_handler.setFormatter(logging.Formatter(
            '%(levelname)s %(message)s'))
        log_handlers.append(email_handler)

    logging.basicConfig(level=0, handlers=log_handlers)

    try:
        if args.game_id is not None:
            with api.EgtaOnlineApi(auth_token=args.auth_string) as ea:
                jgame = ea.get_game(args.game_id).get_observations()
        else:
            jgame = json.load(args.game_json)
        game = gamereader.loadj(jgame)

        extra = {}
        if 'configuration' in jgame:
            extra['configuration'] = dict(jgame['configuration'])
        if 'simulator_fullname' in jgame:
            extra['simname'] = jgame['simulator_fullname']

        sched = sched.create_scheduler(game, args, **extra)
        if args.profile_data is not None:
            sched = prof_data = savesched.SaveScheduler(sched)
        if args.count > 1:
            sched = countsched.CountScheduler(sched, args.count)
        with sched:
            method.run(sched, args)

        if args.profile_data is not None:
            gamej = prof_data.get_samplegame().to_json()
            with open(args.profile_data, 'w') as f:
                json.dump(gamej, f)

    except KeyboardInterrupt as ex:  # pragma: no cover
        _log.critical('execution interrupted by user')
        raise ex

    except Exception as ex:  # pragma: no cover
        exc_type, exc_value, exc_traceback = sys.exc_info()
        _log.critical(''.join(traceback.format_exception(
            exc_type, exc_value, exc_traceback)))
        raise ex


def main_entry_point():
    return main(*sys.argv[1:])  # pragma: no cover
