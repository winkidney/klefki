from klefki.crypto.ssss import SSSS
from klefki.const import SECP256K1_P as P
from klefki.types.algebra.utils import randfield
from klefki.types.algebra.meta import field
import random

def test_ssss():
    F = field(P)
    s = SSSS(F)
    k = random.randint(1, 100)
    n = k * 3
    secret = randfield(F)

    s.setup(secret, k, n)

    assert s.decrypt([s.join() for _ in range(k - 1)]) != secret
    assert s.decrypt([s.join() for _ in range(k)]) == secret
    assert s.decrypt([s.join() for _ in range(k + 1)]) == secret


def test_vss():
    F = field(P)
    s = SSSS(F)
    k = random.randint(1, 100)
    n = k * 3
    secret = randfield(F)

    s.setup(secret, k, n)

    assert s.decrypt([s.join() for _ in range(k - 1)]) != secret
    assert s.decrypt([s.join() for _ in range(k)]) == secret
    assert s.decrypt([s.join() for _ in range(k + 1)]) == secret
    v_to_verify = s.get_v_i_to_verify(2)
    assert s.verify(v_to_verify, 2) == v_to_verify
