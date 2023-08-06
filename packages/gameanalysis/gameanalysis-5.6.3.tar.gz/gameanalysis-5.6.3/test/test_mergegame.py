import json

import numpy as np
import pytest

from gameanalysis import agggen
from gameanalysis import gamegen
from gameanalysis import mergegame
from gameanalysis import paygame
from gameanalysis import rsgame
from test import utils


def test_merge():
    profs1 = [[2, 0],
              [1, 1]]
    pays1 = [[1, 0],
             [2, 3]]
    game1 = paygame.game(2, 2, profs1, pays1)
    profs2 = [[2, 0],
              [1, 1],
              [0, 2]]
    pays2 = [[4, 0],
             [5, np.nan],
             [0, 7]]
    game2 = paygame.game(2, 2, profs2, pays2)
    mgame = mergegame.merge(game1, game2, 0.2)
    assert mgame.num_profiles == 2
    assert mgame.num_complete_profiles == 1
    pay = mgame.get_payoffs([2, 0])
    assert np.allclose(pay, [1.6, 0])
    pay = mgame.get_payoffs([1, 1])
    assert np.allclose(pay, [2.6, np.nan], equal_nan=True)
    pay = mgame.get_payoffs([0, 2])
    assert np.allclose(pay, [0, np.nan], equal_nan=True)


@pytest.mark.parametrize('players,strats', utils.games)
@pytest.mark.parametrize('t', [0.0, 0.2, 0.5, 0.8, 1.0])
def test_random_merge(players, strats, t):
    game1 = gamegen.game(players, strats, .5)
    game2 = agggen.normal_aggfn(players, strats, 3)
    mgame = mergegame.merge(game1, game2, t)

    assert mgame.num_profiles == game1.num_profiles
    assert mgame.num_complete_profiles == game1.num_complete_profiles
    exp_pays = ((1 - t) * game1.get_payoffs(mgame.profiles()) +
                t * game2.get_payoffs(mgame.profiles()))
    assert np.allclose(exp_pays, mgame.payoffs())

    for mix in mgame.random_mixtures(20):
        exp_devs = ((1 - t) * game1.deviation_payoffs(mix) +
                    t * game2.deviation_payoffs(mix))
        assert np.allclose(mgame.deviation_payoffs(mix), exp_devs,
                           equal_nan=True)

        d1, j1 = game1.deviation_payoffs(mix, jacobian=True)
        d2, j2 = game2.deviation_payoffs(mix, jacobian=True)
        exp_devs = (1 - t) * d1 + t * d2
        exp_jac = (1 - t) * j1 + t * j2
        md, mj = mgame.deviation_payoffs(mix, jacobian=True)
        assert np.allclose(md, exp_devs, equal_nan=True)
        assert np.allclose(mj, exp_jac, equal_nan=True)

    profs = mgame.random_profiles(20)
    exp_pays = ((1 - t) * game1.get_payoffs(profs) +
                t * game2.get_payoffs(profs))
    assert np.allclose(mgame.get_payoffs(profs), exp_pays, equal_nan=True)

    for prof in profs:
        assert (prof in mgame) == (prof in game1)

    ngame = mgame.normalize()
    with np.errstate(invalid='ignore'):  # For nan comparison
        assert np.all((ngame.min_strat_payoffs() >= -1e-7) |
                      np.isnan(ngame.min_strat_payoffs()))
        assert np.all((ngame.max_strat_payoffs() <= 1 + 1e-7) |
                      np.isnan(ngame.min_strat_payoffs()))

    rest = mgame.random_restriction()
    rgame = mgame.restrict(rest)
    rgame1 = game1.restrict(rest)
    assert (rsgame.emptygame_copy(rgame) ==
            rsgame.emptygame_copy(rgame1))
    assert rgame.num_profiles == rgame1.num_profiles

    assert repr(game1) == repr(mgame)[5:]

    mstr = json.dumps(mgame.to_json())
    copy = mergegame.merge_json(json.loads(mstr))
    assert mgame == copy

    rev = mergegame.merge(game2, game1, 1 - t)
    assert rev == mgame


@pytest.mark.parametrize('players,strats', utils.games)
@pytest.mark.parametrize('t', [0.0, 0.2, 0.5, 0.8, 1.0])
def test_random_merge_complete(players, strats, t):
    game1 = agggen.normal_aggfn(players, strats, 3)
    game2 = agggen.normal_aggfn(players, strats, 3)
    mgame = mergegame.merge(game1, game2, t)
    assert mgame.is_complete()
    assert mgame.num_profiles == mgame.num_all_profiles
    assert mgame.num_complete_profiles == mgame.num_all_profiles
    assert np.all(mgame.profiles() == mgame.all_profiles())
