from random import randint

import pytest

from klefki.crypto.sss import NaiveSSS


@pytest.mark.parametrize(
    "secret",
    [randint(0, 2 ** 32) for _ in range(100)],
)
def test_naive_sss(secret):
    sss = NaiveSSS(4, 3, secret)
    shares = sss.shares
    assert len(shares) == 4
    ret = sss.rebuild_secret(shares)
    info = {
        "shares": shares,
        "coef": sss._f_x.coef,
    }
    assert round(ret) == secret, info
    least_shares = shares[:3]
    ret = sss.rebuild_secret(least_shares)
    info = {
        "shares": least_shares,
        "coef": sss._f_x.coef,
    }
    assert round(ret) == secret, info
    invalid_shares = shares[:1]
    ret = sss.rebuild_secret(invalid_shares)
    info = {
        "shares": invalid_shares,
        "coef": sss._f_x.coef,
    }
    assert round(ret) != secret, info
