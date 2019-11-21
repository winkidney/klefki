from scipy.interpolate import lagrange
from numpy.polynomial.polynomial import Polynomial

from random import randint


def _lagrange(points):
    def P(x):
        total = 0
        n = len(points)
        for i in range(n):
            xi, yi = points[i]

            def g(i, n):

                tot_mul = 1
                for j in range(n):
                    if i == j:
                        continue
                    xj, yj = points[j]
                    tot_mul *= (x - xj) / float(xi - xj)

                return tot_mul

            total += yi * g(i, n)
        return total

    return P


class NaiveSSS:
    def __init__(self, n: int, k: int, secret: int):
        """
        :param n: number of shares
        :param k: number of shares which required for rebuild a secret
        """
        self._list_of_a = [randint(1, 2 ** 10) for _ in range(k)]
        self._list_of_a[0] = secret
        assert len(self._list_of_a) == k
        self._secret = secret
        self._f_x = Polynomial(self._list_of_a)
        self._real_fx = lambda x: (x, self._f_x(x))
        list_of_x = self._get_given_x(n)
        self._shares = [self._real_fx(x) for x in list_of_x]

    def rebuild_secret(self, k_shares: list):
        """
        return the secret
        """
        list_x = [share[0] for share in k_shares]
        list_f_x = [share[1] for share in k_shares]
        polynomial = lagrange(list_x, list_f_x)
        return polynomial(0)

    @property
    def secret(self):
        """
        private key
        """
        return self._secret

    @property
    def shares(self):
        return self._shares

    @staticmethod
    def _get_given_x(n):
        list_of_x = set()
        while len(list_of_x) < n:
            # x != 0
            # to avoid overflow in polynomial calculation in SciPy
            # use smaller number for concept verification
            list_of_x.add(randint(1, 2 ** 10))
        return list(list_of_x)
