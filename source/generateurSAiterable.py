# x0, a, , m
class GenerateurSA:
    def __init__(self, x0, a, c, m):
        self._x0 = x0
        self._xn = x0
        self._a = a
        self._c = c
        self._m = m
        self._count = 0
        
    def __iter__(self):
        return self

    def __next__(self):
        if self._count <= self._m :
            self._xn = (self._a * self._xn + self._c) % self._m
            self._count += 1
            return self._xn
        else:
            return -1

    def reset(self):
        self._xn = self._x0
        self._count = 0
