import pytest
import random
import time

import numpy as np
from egtaonline import api
from egtaonline import mockserver
from gameanalysis import rsgame

from egta import countsched
from egta import eosched


def test_basic_profile():
    game = rsgame.emptygame([4, 4], [11, 11])
    profs = game.random_profiles(20)

    with mockserver.Server() as server, api.EgtaOnlineApi() as egta:
        # Setup egta
        sim = egta.get_simulator(server.create_simulator(
            'sim', '1', delay_dist=lambda: random.random() / 10))
        sim.add_dict({role: strats for role, strats
                      in zip(game.role_names, game.strat_names)})

        # Schedule all new profiles and verify it works
        # This first time should have to wait to schedule more
        sched = eosched.EgtaOnlineScheduler(
            game, egta, sim['id'], 1, {}, 1, 10, 0, 0)
        with sched:
            proms = [sched.schedule(p) for p in profs]
            pays = np.stack([p.get() for p in proms])
        assert np.allclose(pays[profs == 0], 0)
        assert sched._num_running_profiles == 0

        # Schedule old profiles and verify it still works
        sched = eosched.EgtaOnlineScheduler(
            game, egta, sim['id'], 1, {}, 1, 25, 0, 0)
        with sched:
            proms = [sched.schedule(p) for p in profs]
            pays = np.stack([p.get() for p in proms])
        assert np.allclose(pays[profs == 0], 0)
        assert sched._num_running_profiles == 0

        # Schedule two at a time, in two batches
        base_sched = eosched.EgtaOnlineScheduler(
            game, egta, sim['id'], 1, {}, 1, 25, 0, 0)
        sched = countsched.CountScheduler(base_sched, 2)
        with sched:
            proms = [sched.schedule(p) for p in profs]
            pays = np.stack([p.get() for p in proms])
        assert np.allclose(pays[profs == 0], 0)
        assert base_sched._num_running_profiles == 0

        # Try again now that everything should be scheduled
        base_sched = eosched.EgtaOnlineScheduler(
            game, egta, sim['id'], 1, {}, 1, 25, 0, 0)
        sched = countsched.CountScheduler(base_sched, 2)
        with sched:
            proms = [sched.schedule(p) for p in profs]
            pays = np.stack([p.get() for p in proms])
        assert np.allclose(pays[profs == 0], 0)
        assert base_sched._num_running_profiles == 0


def test_extra_samples():
    game = rsgame.emptygame([4, 4], [11, 11])
    profs = game.random_profiles(20)

    with mockserver.Server() as server, api.EgtaOnlineApi() as egta:
        # Setup egta
        sim = egta.get_simulator(server.create_simulator(
            'sim', '1', delay_dist=lambda: random.random() / 10))
        sim.add_dict({role: strats for role, strats
                      in zip(game.role_names, game.strat_names)})

        # Schedule all new profiles and verify it works
        # This first time should have to wait to schedule more
        sched = eosched.EgtaOnlineScheduler(
            game, egta, sim['id'], 1, {}, 1, 25, 0, 0)
        with sched:
            proms = [sched.schedule(p) for p in profs]
            pays1 = np.stack([p.get() for p in proms])
            proms = [sched.schedule(p) for p in profs]
            pays2 = np.stack([p.get() for p in proms])
            pays3 = np.stack([p.get() for p in proms])
        assert np.allclose(pays1[profs == 0], 0)
        assert np.allclose(pays2[profs == 0], 0)
        assert np.allclose(pays2, pays3)
        assert sched._num_running_profiles == 0


def test_existing_game():
    game = rsgame.emptygame([4, 4], [11, 11])
    profs = game.random_profiles(20)

    with mockserver.Server() as server, api.EgtaOnlineApi() as egta:
        # Setup egta
        sim = egta.get_simulator(server.create_simulator(
            'sim', '1', delay_dist=lambda: random.random() / 10))
        sim.add_dict({role: strats for role, strats
                      in zip(game.role_names, game.strat_names)})
        eogame = sim.create_game('game', game.num_players)
        for role, count, strats in zip(game.role_names, game.num_role_players,
                                       game.strat_names):
            eogame.add_role(role, count)
            for strat in strats:
                eogame.add_strategy(role, strat)

        # Schedule all new profiles and verify it works
        # This first time should have to wait to schedule more
        sched = eosched.EgtaOnlineScheduler(
            game, egta, sim['id'], 1, {}, 1, 25, 0, 0, game_id=eogame['id'])
        with sched:
            proms = [sched.schedule(p) for p in profs]
            pays1 = np.stack([p.get() for p in proms])
            proms = [sched.schedule(p) for p in profs]
            pays2 = np.stack([p.get() for p in proms])
        assert np.allclose(pays1[profs == 0], 0)
        assert np.allclose(pays2[profs == 0], 0)
        assert np.allclose(pays1, pays2)
        assert sched._num_running_profiles == 0


def test_exception_in_get():
    game = rsgame.emptygame([4, 4], [11, 11])
    profs = game.random_profiles(20)

    with mockserver.Server() as server, api.EgtaOnlineApi() as egta:
        # Setup egta
        sim = egta.get_simulator(server.create_simulator(
            'sim', '1', delay_dist=lambda: random.random() / 10))
        sim.add_dict({role: strats for role, strats
                      in zip(game.role_names, game.strat_names)})

        with eosched.EgtaOnlineScheduler(
                game, egta, sim['id'], 1, {}, 1, 25, 0, 0) as sched:
            proms = [sched.schedule(p) for p in profs]
            server.throw_exception(TimeoutError)
            with pytest.raises(TimeoutError):
                for p in proms:  # pragma: no branch
                    p.get()


def test_exception_in_schedule():
    game = rsgame.emptygame([4, 4], [11, 11])
    prof = game.random_profile()

    with mockserver.Server() as server, api.EgtaOnlineApi() as egta:
        # Setup egta
        sim = egta.get_simulator(server.create_simulator(  # pragma: no cover
            'sim', '1', delay_dist=lambda: random.random() / 10))
        sim.add_dict({role: strats for role, strats
                      in zip(game.role_names, game.strat_names)})

        with eosched.EgtaOnlineScheduler(
                game, egta, sim['id'], 1, {}, 0.1, 25, 0, 0) as sched:
            # so that enough calls to get_requirements are made
            server.throw_exception(TimeoutError)
            time.sleep(1)
            with pytest.raises(TimeoutError):
                sched.schedule(prof)


def test_scheduler_deactivate():
    game = rsgame.emptygame([4, 4], [11, 11])

    with mockserver.Server() as server, api.EgtaOnlineApi() as egta:
        # Setup egta
        sim = egta.get_simulator(server.create_simulator('sim', '1'))
        sim.add_dict({role: strats for role, strats
                      in zip(game.role_names, game.strat_names)})

        # Schedule all new profiles and verify it works
        # This first time should have to wait to schedule more
        with eosched.EgtaOnlineScheduler(
                game, egta, sim['id'], 1, {}, 0.1, 10, 0, 0) as sched:
            # Deactivate scheduler
            for esched in egta.get_generic_schedulers():
                esched.deactivate()
            # Schedule a profile so that requirements are checked
            sched.schedule(game.random_profile())
            # Wait to check that it's deactivate
            time.sleep(.5)
            with pytest.raises(AssertionError):
                sched.schedule(game.random_profile())
