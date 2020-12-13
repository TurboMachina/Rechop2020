class Station:
    def __init__(self, clients, min_occupees, min_inoccupees):
        self._clients = clients
        self._min_occupees = min_occupees
        self._min_inoccupees = min_inoccupees

    @property
    def clients(self):
        return self._clients
    @property
    def min_occupees(self):
        return self._min_occupees
    @property
    def min_inoccupees(self):
        return self._min_inoccupees


class Client:
    def __init__(self, classe, duree_service):
        self._classe = classe
        self._duree_service = duree_service
    
    @property
    def classe(self):
        return self._classe
    @property
    def duree_service(self):
        return self._duree_service



class Switch(dict):
    def __getitem__(self, item):
        for key in self.keys():
            if item in key:
                return super().__getitem__(key)
        raise KeyError(item)    

switch = Switch({
    range(0, 24): 1,
    range(25, 42): 2,
    range(43, 52): 3,
    range(53, 55): 4,
    range(56, 58): 5,
    range(59, 60): 6
})