# x0, a, , m

class GenerateurSA:
    def __init__(self, x0, a, c, m):
        self._x0 = x0
        self._xn = x0
        self._a = a
        self._c = c
        self._m = m

    def __iter__(self):
        return self

    def __next__(self):
        self._xn = (self._a * self._xn + self._c) % self._m
        return self._xn
