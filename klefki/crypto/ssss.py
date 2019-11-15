'''
* ref https://en.wikipedia.org/wiki/Shamir%27s_Secret_Sharing
The essential idea of Adi Shamir's threshold scheme is that 2 points are sufficient to define a line, 3 points are sufficient to define a parabola, 4 points to define a cubic curve and so forth. That is, it takes $k$ points to define a polynomial of degree $k-1$.



'''

import random
from functools import reduce
from operator import add, mul
from klefki.types.algebra.fields import FiniteField
from klefki.types.algebra.meta import field
from klefki.types.algebra.utils import randfield


def get_v_i(g, a_i):
    return g * a_i


class SSSS:
    def __init__(self, F: FiniteField):
        self.F = F
        self.node_count=0

    def setup(self, Secret, k, n):
        self.k = k
        self.n = n
        self.g = randfield(self.F)
        a = [randfield(self.F) for _ in range(k - 1)]
        self.v_list = [get_v_i(self.g, a_i) for a_i in a]
        self._powers = [(i, i) for i in range(1, k - 1)]
        self.f = lambda x: Secret + reduce(
            add, [a[index] * (x ** power) for index, power in self._powers])
        return self

    def get_v_i_to_verify(self, i):
        return self.v_list[i]

    def verify(self, v_to_verify, i):
        v_j = None
        for index, j in self._powers:
            if v_j is None:
                v_j = self.v_list[j] ** (i ** j)
            else:
                v_j *= self.v_list[j] ** (i ** j)
        product = v_j
        return product

    def join(self):
        assert self.node_count < self.n
        self.node_count += 1
        x = randfield(self.F)
        if not hasattr(self, 'f'):
            raise Exception("Needs to encrypt first")
        return (x, self.f(x))


    def decrypt(self, priv):
        x, fx = zip(*priv)
        k = len(fx)
        return reduce(add,
                      [fx[j] * reduce(
                          mul,
                          [x[m] / (x[m]-x[j]) for m in range(k-1) if m != j]) for j in range(k-1)])
