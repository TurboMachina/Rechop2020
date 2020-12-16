class Station:
    def __init__(self, client, min_occupees, min_inoccupees):
        self._client = client
        self._min_occupees = min_occupees
        self._min_inoccupees = min_inoccupees

    @property
    def client(self):
        return self._client
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
