class Saut:
    def __init__(self, saut, pi, ri, npi):
        self._saut = saut
        self._pi = pi
        self._ri = ri
        self._npi = npi

    @property
    def saut(self):
        return self._saut
    @property
    def pi(self):
        return self._pi
    @property
    def ri(self):
        return self._ri
    @property
    def npi(self):
        return self._npi