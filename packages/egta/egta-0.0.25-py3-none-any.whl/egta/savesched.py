import itertools
import threading

import numpy as np
from gameanalysis import paygame
from gameanalysis import utils

from egta import profsched


class SaveScheduler(profsched.Scheduler):
    """A scheduler that saves all of the payoff data for output later

    Parameters
    ----------
    game : BaseGame
        The base game of the scheduler.
    sched : Scheduler
        The bas scheduler to save payoffs from
    """

    def __init__(self, sched):
        self._sched = sched
        self._payoffs = {}

    def schedule(self, profile):
        return _SavePromise(self._payoffs, profile,
                            self._sched.schedule(profile))

    def game(self):
        return self._sched.game()

    def get_samplegame(self):
        by_obs = {}
        for prof, pays in self._payoffs.items():
            prof_list, pays_list = by_obs.setdefault(len(pays), ([], []))
            prof_list.append(prof.array)
            pays_list.append(pays)
        profiles = np.array(list(itertools.chain.from_iterable(
            p for p, _ in by_obs.values())), int)
        sample_pays = [np.array(p) for _, p in by_obs.values()]
        return paygame.samplegame_replace(self.game(), profiles, sample_pays)

    def __enter__(self):
        self._sched.__enter__()
        return self

    def __exit__(self, *args):
        self._sched.__exit__(*args)


class _SavePromise(profsched.Promise):
    def __init__(self, data, profile, promise):
        self._data = data
        self._profile = profile
        self._promise = promise
        self._saved = False
        self._lock = threading.Lock()

    def get(self):
        payoff = self._promise.get()
        with self._lock:
            if not self._saved:
                payoffs = self._data.setdefault(
                    utils.hash_array(self._profile), [])
                payoffs.append(payoff)
                self._saved = True
        return payoff
