from source.classesStationClient import Station
import source.générateurSA as gen_suite_aleatoire
import sys

def generer_duree_service(indice_suite_aleatoire):
    pass

def generer_arrivee_clients(temps_simulation, suite_aleatoire, indice_suite_aleatoire, tab_poisson, m):
    clients = []
    proba_poisson = suite_aleatoire[temps_simulation] / m
    if(proba_poisson <= tab_poisson[0]):
        nb_clients = 0
    else:
        for i_poisson in range(1, len(tab_poisson)):
            if(proba_poisson <= tab_poisson[i_poisson] and proba_poisson > tab_poisson[i_poisson -1]):
                nb_clients = i_poisson
    for i in range(nb_clients): # TODO il est possible que nb_clients n'existe pas
        est_prioritaire = generer_duree_service(indice_suite_aleatoire)

def gestion_file_attente():
    tab_poisson = [24,18,10,3,3,2]
    x0, a, c, m, suite_aleatoire = gen_suite_aleatoire.main_generateur()
    cout_optimal = sys.maxsize
    nb_stations_optimal = 1
    temps_simulation_max = 600
    nb_stations_ordinaire_max = 48
    nb_stations_ordinaires = 5
    taille_max_file_express = 10
    indice_suite_aleatoire = 0

    while(nb_stations_ordinaires <= nb_stations_ordinaire_max):
        temps_simulation = 0
        file_express = []
        file_ordinaire = []
        stations = []
        nb_declasses = 0
        nb_ejectes = 0
        min_express = 0
        min_ordinaire = 0
        min_prioritaire = 0
        for i in range(nb_stations_ordinaires + 1): # pas en +2 : correction de Mme Derwa
            stations.append(Station([], 0, 0))

        while(temps_simulation <= temps_simulation_max):

            clients = generer_arrivee_clients(temps_simulation, suite_aleatoire, indice_suite_aleatoire, tab_poisson, m)
            


            temps_simulation += 1

        nb_stations_ordinaires += 1