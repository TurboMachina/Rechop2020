from source.classeSaut import Saut
import scipy.stats as sc

def hull_dobbel_periode(x0, a, c, m):
    if(c < m):
        lower = c # useless ?
        bigger = m
    else:
        lower = m
        bigger = c
    half_of_bigger = bigger // 2
    for i in range(half_of_bigger + 1):
        if(c % i == 0 and m % i == 0):
            return False

    for p in range(2, m//2):
        if(est_premier(p) and m % p == 0):
            if p % (a * (a - 1)) != 0: # verif si cette formule est bonne
                return False

    if(m % 4 == 0):
        return ((a - 1) % 4) == 0 # on renvoie bien true ou false dans les bons cas ?
        # on renvoie true ou false si le if passe, rien sinon ?


def generer_suite_aleatoire(x0, a, c ,m):
    suite_aleatoire = []
    suite_aleatoire.append(x0)
    xn_plusun = (a * x0 + c) % m
    while(xn_plusun != x0):
        suite_aleatoire.append(xn_plusun)
        xn = xn_plusun
        xn_plusun = (a * xn + c) % m
    return suite_aleatoire

def est_premier(nombre):
    half_of_number = nombre // 2
    for i in range(2,half_of_number+1):
        if(nombre % i == 0):
            return False
    return True

def merge(merge_start_id, merge_end_id, test_des_sauts):
    pass

def test_des_sauts(suite_aleatoire, valeur_test_saut):
    niveau_incertitude = 0.05
    n = len(suite_aleatoire)
    test_des_sauts = []
    for i in range(n-2):
        new_saut = Saut(i, (0.9**i)*0.1, None, n*pi) # wtf le pi ici ?
        test_des_sauts.append(new_saut)
    
    index_val = 0
    while(suite_aleatoire[index_val] != valeur_test_saut and index_val < n):
        index_val += 1
    saut = 0
    for i in range(index_val+1, n):
        if(suite_aleatoire[i] != valeur_test_saut):
            saut += 1
        else:
            test_des_sauts[saut].ri += 1
            saut = 0

    for i in range(n-1,-1,-1):
        if(test_des_sauts[i].npi < 5):
            npi_temp = test_des_sauts[i].npi
            merge_start_id = i
            while(i >= 0 and npi_temp > 5):
                i -= 1
                npi_temp += test_des_sauts[i].npi
            merge_end_id = i
            test_des_sauts = merge(merge_start_id, merge_end_id, test_des_sauts)
    
    khi_carre = 0
    for i in range(len(test_des_sauts)):
        tds = test_des_sauts[i]
        khi_carre += ((tds.ri - tds.pi)**2) / (tds.npi)
    degre_de_liberte = len(test_des_sauts) - 1
    proba = 1 - niveau_incertitude
    # TODO khi carré
    valeur_max = sc.chi2_contingency() # go creuser la doc de scipy pour voir comment ça marche

    return khi_carre >= 0 and khi_carre <= valeur_max

    # TODO def Merge (Simpson mdr)
    
def main_generateur():
    x0 = input()
    a  = input()
    c = input()
    m = input()
    valeurTestSaut = input()

    if(not hull_dobbel_periode(x0, a, c, m)):
        print("Paramètres incorrects")
        return None
    suite_aleatoire = generer_suite_aleatoire(x0, a, c, m)
    if(test_des_sauts(suite_aleatoire, valeurTestSaut)):
        print("Test des sauts foiré XD")
        return None

    return suite_aleatoire # pas dans le DA mais utile pour après