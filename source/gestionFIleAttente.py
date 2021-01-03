import classesStationClient as stcl
import générateurSA as gen_suite_aleatoire
from generateurSAiterable import GenerateurSA
import sys
import math
     

def generer_Xn(suite):
    x = next(suite)
    if x==-1:
        suite.reset()
        x = next(suite)
    return x
    
def generer_Un(suite):
    return generer_Xn(suite) / suite._m
    
def generer_Yn(suite):
    return int(math.floor(generer_Un(suite)*10))

def generer_duree_service(suite, tab_expo_neg):
    nombre_aleatoire = (generer_Yn(suite)+1)*6
    for i in range(0,len(tab_expo_neg)):
        pre,post = tab_expo_neg[i]
        if pre <= nombre_aleatoire <= post:
            return (i+1)

def generer_arrivee_clients(suite, tab_proba_poisson,tab_expo_neg):
    clients = []
    proba_poisson = generer_Un(suite)
    nb_clients = 0
    for i in range(0,len(tab_proba_poisson)):
        pre,post = tab_proba_poisson[i]
        if pre < proba_poisson <= post:
            nb_clients = i
    if proba_poisson > 0.999 :
        nb_clients = 8
    if(nb_clients>0):
        for i in range(nb_clients):
            duree_service = generer_duree_service(suite,tab_expo_neg)
            if(duree_service == 1):
                classe = "express"
            else:
                if(generer_Yn(suite) == 1):
                    classe = "prioritaire"
                else:
                    classe = "ordinaire"
            clients.append(stcl.Client(classe, duree_service))
    return clients

def generer_rapport_pre(rapport, nb_stations, temps_simulation, stations, file_ordinaire, file_express, clients):
    if nb_stations == 7 and temps_simulation <= 20:
        if temps_simulation != 0 :
            rapport.write("==========================================")
        rapport.write("\nDébut de Minute : " + str(temps_simulation))
        
        #Rapport stations
        for i in range(0, nb_stations):
            if 0 <= i <= 1 :
                text = "\n\tStation express n° " + str(i)
            else :
                text = "\n\tStation ordinaire n° " + str(i)
            rapport.write(text)
            if(stations[i].client != None):
                text = "\n\t\tClient de type " + stations[i].client.classe
                rapport.write(text + " et temps de service restant : " + str(stations[i].client.duree_service))
            else:
                text ="\n\t\tPas de client en station"
                rapport.write(text)
            
        #Rapport file express
        if(len(file_express) > 0):
            text = "\n\n\tFile express : " + str(len(file_express))
            text+= " clients" if len(file_express) > 1 else " client"
        else:
            text = "\n\n\tFile express vide"
        rapport.write(text)
        if(len(file_express) >= 10):
            rapport.write("\n\tCette file est pleine")

            
        #Rapport file ordinaire
        if(len(file_ordinaire) > 0):
            text = "\n\tFile ordinaire : " + str(len(file_ordinaire))
            text+= " clients" if len(file_express) > 1 else " client"
        else:
            text = "\n\tFile ordinaire vide"
        rapport.write(text)
            
        #Nouvelle arrivée
        if(len(clients) > 0):
            rapport.write("\n\n\tNombre de clients arrivé à cette minute : " + str(len(clients)))
            rapport.write("\n\tClasse des clients :")
            for i in range(0, len(clients)):
                rapport.write("\n\t\tClient n°" + str(i) + " : " + clients[i].classe + "\n")
        else:
            rapport.write("\n\n\tAucun client n'est arrivé à cette minute\n")
    
def generer_rapport_middle(rapport, nb_stations, temps_simulation, file_ordinaire, file_express, nb_ejecte, nb_declasses):
    if nb_stations == 7 and temps_simulation <= 20:
        rapport.write("\nMilieu de Minute : " + str(temps_simulation))
        #Rapport file express
        if(len(file_express) > 0):
            text = "\n\tFile express : " + str(len(file_express))
            text+= " clients" if len(file_express) > 1 else " client"
        else:
            text = "\n\tFile express vide"
        rapport.write(text)
        if(len(file_express) >= 10):
            rapport.write("\n\t\tLa file express est pleine")
            
        #Rapport file ordinaire
        if(len(file_ordinaire) > 0):
            text = "\n\tFile ordinaire : " + str(len(file_ordinaire))
            text+= " clients" if len(file_express) > 1 else " client"
        else:
            text = "\n\tFile ordinaire vide"
        rapport.write(text)
        rapport.write("\n\tClients ejecte de leur station par un prioritaire et remis au début de file ce tour ci : " + str(nb_ejecte))
        rapport.write("\n\tClients declasse car la file express était pleine : " + str(nb_declasses) + "\n")
                
def generer_rapport_post(rapport, nb_stations, temps_simulation, stations, file_ordinaire, file_express):
    if nb_stations == 7 and temps_simulation <= 20:
        rapport.write("\nFin de Minute : " + str(temps_simulation))
        #Rapport stations
        for i in range(0, nb_stations):
            if 0 <= i <= 1 :
                text = "\n\tStation express n° " + str(i)
            else :
                text = "\n\tStation ordinaire n° " + str(i)
            rapport.write(text)
            if(stations[i].client != None):
                rapport.write("\n\t\tClient de type " + stations[i].client.classe)
                rapport.write("\n\t\tTemps de service restant : " + str(stations[i].client.duree_service))
            else:
                rapport.write("\n\t\tPas de client en station")
            
        #Rapport file express
        if(len(file_express) > 0):
            text = "\n\tFile express : " + str(len(file_express))
            text+= " clients" if len(file_express) > 1 else " client"
            rapport.write(text)
        else:
            rapport.write("\n\tFile express vide")
        if(len(file_express) >= 10):
            rapport.write("\n\tCette file est pleine")
            
        #Rapport file ordinaire
        if(len(file_ordinaire) > 0):
            text = "\n\tFile ordinaire : " + str(len(file_ordinaire))
            text+= " clients" if len(file_express) > 1 else " client"
        else:
            text = "\n\tFile ordinaire vide\n\n"
        rapport.write(text)
            
        

def gestion_file_attente(suite, rapport, rapport_couts):
    tab_proba_poisson = [(0,0.135),(0.135,0.406),(0.406,0.677),(0.677,0.857),(0.857,0.947),(0.947,0.983),(0.983,0.995),(0.995,0.998),(0.998,0.999)]
    tab_expo_neg = [(0,24),(24,42),(42,52),(52,55),(55,58),(58,60)]
    cout_optimal = sys.float_info.max
    nb_stations_optimal = 1
    temps_simulation_max = 600
    nb_stations_max = 50
    nb_stations = 7
    taille_max_file_express = 10

    while(nb_stations <= nb_stations_max):
        suite.reset()
        temps_simulation = 0
        file_express = []
        file_ordinaire = []
        stations = []
        nb_declasses = 0
        nb_ejectes = 0
        min_express = 0
        min_ordinaire = 0
        min_prioritaire = 0
        for i in range(nb_stations + 1):
            stations.append(stcl.Station(None, 0, 0))

        while(temps_simulation <= temps_simulation_max):
            clients = generer_arrivee_clients(suite, tab_proba_poisson,tab_expo_neg)
            nb_declasses_current = 0
            nb_ejectes_current = 0
            generer_rapport_pre(rapport, nb_stations, temps_simulation, stations, file_ordinaire, file_express, clients)
            
            # Gérer arrivées clients
            for i in range(len(clients)):
                if(clients[i].classe == "express"):
                    if(len(file_express) < taille_max_file_express):
                        file_express.append(clients[i])
                    else:
                        clients[i]._classe = "ordinaire"
                        file_ordinaire.append(clients[i])
                        nb_declasses += 1
                        nb_declasses_current += 1
                elif(clients[i].classe == "ordinaire"):
                    file_ordinaire.append(clients[i])
                elif(clients[i].classe == "prioritaire"):
                    min_prioritaire += clients[i].duree_service
                    #Chercher si station vide
                    i_station = 2
                    while(i_station < nb_stations and stations[i_station].client is not None):
                        i_station+=1
                    if(stations[i_station].client is None) :
                        stations[i_station]._client = clients[i]
                    else:  
                        i_ejecte = 0
                        #Chercher client avec max temps de traitement
                        max_temps = 0
                        for i_station in range (2, len(stations)):
                            if(stations[i_station].client.duree_service > max_temps and stations[i_station].client.classe == "ordinaire"):
                                i_ejecte = i_station
                        
                        client_ejecte = stations[i_ejecte].client
                        stations[i_ejecte]._client = clients[i]
                        nb_ejectes += 1
                        nb_ejectes_current += 1
                        file_ordinaire.insert(0, client_ejecte)
                            
            generer_rapport_middle(rapport, nb_stations, temps_simulation, file_ordinaire, file_express, nb_ejectes_current, nb_declasses_current)
            
            # Gerer express
            for i_station in range(3):
                if(stations[i_station].client is None):
                    if(len(file_express)>0):
                        stations[i_station]._client = file_express[0]
                        del file_express[0]
                else:
                        if(stations[i_station].client.duree_service == 0 and len(file_express) > 0):
                            stations[i_station]._client = file_express[0]
                            min_express += file_express[0].duree_service
                            del file_express[0]
                        elif(stations[i_station]._client.duree_service == 0 and len(file_express) == 0):
                            stations[i_station]._client = None 
                            
                            
            #Gerer Ordinaire
            for i_station in range(2,len(stations)):
                if(stations[i_station].client is None):
                    if(len(file_ordinaire)>0):
                        stations[i_station]._client = file_ordinaire[0]
                        del file_ordinaire[0]
                else:
                    if(stations[i_station]._client.duree_service == 0 and len(file_ordinaire) > 0):
                        stations[i_station]._client = file_ordinaire[0]
                        if(file_ordinaire[0]._classe == "ordinaire"):
                            min_ordinaire += file_ordinaire[0].duree_service
                        else:
                            min_prioritaire += file_ordinaire[0].duree_service
                        del file_ordinaire[0]
                    elif(stations[i_station].client.duree_service == 0 and len(file_ordinaire) == 0):
                        stations[i_station]._client = None
                    
            
            #Passage d'une minute en station
            for i_station in range(0,len(stations)):
                if(stations[i_station].client is not None):
                    stations[i_station].client._duree_service -= 1
                    stations[i_station]._min_occupees+=1
                else:
                    stations[i_station]._min_inoccupees += 1
                            
            generer_rapport_post(rapport, nb_stations, temps_simulation, stations, file_ordinaire, file_express)               
            temps_simulation += 1
            
        #Calcul des couts
        couts_inoccupation_express = 0
        couts_inoccupation_ordinaire = 0
        couts_occupation_express = 0
        couts_occupation_ordinaire = 0
        couts_express = (min_express / 60) * 35
        couts_ordinaire = (min_ordinaire / 60) * 25
        couts_prioritaire = (min_prioritaire / 60) * 45
        couts_declasses = (nb_declasses * 15)
        couts_ejectes = (nb_ejectes * 20)
        for i_station in range(0, len(stations)):
            if 0 <= i_station <= 1:
                couts_occupation_express += (stations[i_station].min_occupees / 60) * 32
                couts_inoccupation_express += (stations[i_station].min_inoccupees / 60) * 18
            else:
                couts_occupation_ordinaire += (stations[i_station].min_occupees / 60) * 30
                couts_inoccupation_ordinaire += (stations[i_station].min_inoccupees / 60) * 18
    
        cout_total = couts_inoccupation_express + couts_inoccupation_ordinaire + couts_occupation_express + couts_occupation_ordinaire + couts_express + couts_ordinaire + couts_prioritaire + couts_declasses + couts_ejectes
        rapport_couts.write("Rapport pour le nombre de station : " + str(nb_stations))
        rapport_couts.write("\nCouts des stations express")
        rapport_couts.write("\n\tCouts d'innocupation : " + str(couts_inoccupation_express))
        rapport_couts.write("\n\tCouts d'occupation :" + str(couts_occupation_express))
        rapport_couts.write("\nCouts des stations ordinaires")
        rapport_couts.write("\n\tCouts d'innocupation : " + str(couts_inoccupation_ordinaire))
        rapport_couts.write("\n\tCouts d'occupation :" + str(couts_occupation_ordinaire))
        rapport_couts.write("\n\n\nRapport pour le temps passé dans le systéme")
        rapport_couts.write("\n\tCouts pour les clients express : " + str(couts_express))
        rapport_couts.write("\n\tCouts pour les clients prioritaire : " + str(couts_prioritaire))
        rapport_couts.write("\n\tCouts pour les clients ordinaire : " + str(couts_ordinaire))
        rapport_couts.write("\n\n\nCouts pour les déclassement : " + str(couts_declasses))
        rapport_couts.write("\nCouts pour les ejections de station : " + str(couts_ejectes))
        rapport_couts.write("\n\n\nCouts total de la simulation : " + str(cout_total))
        rapport_couts.write('\n============================================')
        rapport_couts.write('\n============================================\n\n')

        
        #Chercher optimal
        if(cout_total < cout_optimal):
            cout_optimal = cout_total
            nb_stations_optimal = nb_stations
        
        nb_stations += 1
    print("Le nombre de station optimal est : " + str(nb_stations_optimal))

if __name__ == "__main__":
    x0 = int(input("x0 ?"))
    a = int(input("a ?"))
    c = int(input("c ?"))
    m = int(input ("m ?"))
    # while not gen_suite_aleatoire.main(x0,a,c,m):
    #     x0 = int(input("x0 ?"))
    #     a = int(input("a ?"))
    #     c = int(input("c ?"))
    #     m = int(input ("m ?"))
    suite = GenerateurSA(x0,a,c,m)
    gen_suite_aleatoire.main(x0,a,c,m)
    # rapport = open("rapport_simulation.txt", "w")
    # rapport_couts = open("rapport_couts.txt", "w")
    # gestion_file_attente(suite, rapport, rapport_couts)
    # rapport.close()
    # rapport_couts.close()
