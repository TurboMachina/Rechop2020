# correction Mme Derwa : avancer Pas à pas dans la recu et pas tout stocker en mémoire
# -> Prendre un paramètre indice supplémentaire


from classeSaut import Saut
from generateurSAiterable import GenerateurSA
from xlwt import Workbook 
from scipy import stats
from functools import reduce
import math



#----------------------------------------------------------------------------
#           génération suite
#----------------------------------------------------------------------------

#test si un nombre est premier
def est_premier_entreeux(c,m):
    for i in range(2,min(c,m)) :
        if c%i == 0 and m%i == 0 :
            return False
    return True

estPremier = lambda x : not any ([x % i == 0 for i in range(2,x)])


#2 hypothese à vérifier pour Hull Dobell
def fact_premier_m(m,a):
    for p in range(2,int(m/2)):
        if estPremier(p) and m%p == 0 :
            if(p%(a*(a-1)) == 0):
                return False
    return True

#3 hypothese à vérifier pour Hull Dobell          
def m_mult_4(m,a):
    if m % 4 == 0:
        return (a-1) % 4 == 0
    return True

#test pour vérifier que c'est une suite de nombre aléatoire
def Hull_Dobell(x0, a, c, m):
    return est_premier_entreeux(c,m) and fact_premier_m(m,a) and m_mult_4(m, a)
        
#renvoie la suite aléatoire et en donne sa période
def periode_serie(x0,a,c,m):
    serie = [x0]
    x1 = (a*x0 + c) %m
    serie.append(x1)  
    for iSerie in range(2,m):
        xn = (a*serie[iSerie-1] + c) %m
        if xn == x1:
            return (iSerie-1, serie)
        serie.append(xn)
    return (m, serie)

#----------------------------------------------------------------------------
#           Tests validités
#----------------------------------------------------------------------------


def test_des_sauts(suite_aleatoire, valeur_test_saut, m):
    n = 0
    wb = Workbook()
    preRegroup = wb.add_sheet("Pre-regroupement")
    preRegroup.write(0,0, 'Longueur du saut')
    preRegroup.write(0,1, 'Ri')
    preRegroup.write(0,2, 'Pi')
    preRegroup.write(0,3, 'N*Pi')
    postRegroup = wb.add_sheet("Post-regroupement")
    postRegroup.write(0,0, 'Longueur du saut')
    postRegroup.write(0,1, 'Ri')
    postRegroup.write(0,2, 'Pi')
    postRegroup.write(0,3, 'N*Pi')
    # le test s'intéresse aux longueurs des sauts avant de recroiser une valeur
    # de la suite
    
    # etape 1
    #H0 : la suite xn est acceptable
    #H1 : la suite xn n'est pas acceptable
    
    #etape 2
    alpha = 0.05
    
    #etape 3
    #créations des longueurs de sauts
    tabSauts = []
    for i in range (0,m-2):
        pi = (0.9**i)*0.1
        tabSauts.append(Saut(i,pi,0,0))
        
    #parcours de la suite pour incrémenter les ri correspondant
    x = math.floor((suite_aleatoire._x0/m)*10)
    while(x != valeur_test_saut) :
        x = math.floor((next(suite_aleatoire)/m)*10)
    saut = 0
    while(x != -1) :
        x = math.floor((next(suite_aleatoire)/m)*10)
        if(x != valeur_test_saut):
            saut+=1
        else:
            tabSauts[saut]._ri += 1
            n+= 1
            saut = 0
            
    #determine n
    #ecriture des résultat pré-regroupement
    for i in range(0, len(tabSauts)):
        tabSauts[i]._npi = n * tabSauts[i].pi
        preRegroup.write(i+1,0, tabSauts[i].saut)
        preRegroup.write(i+1,1, tabSauts[i].ri)
        preRegroup.write(i+1,2, tabSauts[i].pi)
        preRegroup.write(i+1,3, tabSauts[i].npi)
    
    #etape 4
    #regroupement pour que n*pi > 5
    nb_classes_regroup = 0
    for i in range(len(tabSauts)-1,0,-1):
        if tabSauts[i].npi < 5 :
            nb_classes_regroup += 1
            tabSauts[i-1]._npi += tabSauts[i].npi
            tabSauts[i-1]._ri += tabSauts[i].ri
            tabSauts[i-1]._pi += tabSauts[i].pi
            if(type(tabSauts[i].saut) == int):
                tabSauts[i-1]._saut = (tabSauts[i-1].saut,tabSauts[i].saut)
            else:
                pre,post = tabSauts[i].saut
                tabSauts[i-1]._saut = (tabSauts[i-1].saut,post)
            del tabSauts[i]
    
    #ecriture des résultat pré-regroupement
    for i in range(0, len(tabSauts)):
        if(type(tabSauts[i].saut) == int):
            postRegroup.write(i+1,0, tabSauts[i].saut)
        else :
            pre, post = tabSauts[i].saut
            postRegroup.write(i+1,0, str(pre) + " - " + str(post) )
            
        postRegroup.write(i+1,1, tabSauts[i].ri)
        postRegroup.write(i+1,2, tabSauts[i].pi)
        postRegroup.write(i+1,3, tabSauts[i].npi)
    
    last_line = i    
    
    
    
    #etape 5
    #calcul zone de rejet à partir de la table de Khi carré théorique
    deb_reg_rejet = stats.chi2.ppf(1 - alpha, len(tabSauts) - 1)
    #calcul du Khi carré observé
    X_obs = []
    for i in range(0, len(tabSauts)):
        X_obs.append(math.pow(tabSauts[i].ri- tabSauts[i].npi,2)/ tabSauts[i].npi)
    
    X_obs = reduce(lambda x,y : x+y, X_obs)
    postRegroup.write(last_line+3, 0, "Khi² observé :")
    postRegroup.write(last_line+3, 1, X_obs)
    postRegroup.write(last_line+4, 0, "Khi² théorique :")
    postRegroup.write(last_line+4, 1, deb_reg_rejet)
    
    #etape 6
    if deb_reg_rejet < X_obs :
        postRegroup.write(last_line+5, 0, "Rejet de H0, la suite n'est pas acceptable au test des courses")
        wb.save("adm_" + str(valeur_test_saut) + ".xls")
        return False
    else :
        postRegroup.write(last_line+5, 0, "Non rejet de H0, la suite est acceptable au test des courses")
        wb.save("adm_" + str(valeur_test_saut) + ".xls")
        return True
    

    
def main(x0,a,c,m):
    tabTest = []
    if(not Hull_Dobell(x0, a, c, m)):
        print("Paramètres incorrects")
        return False
    else:
        print("Paramètres x0:"+str(x0)+" a:"+ str(a)+" c:"+ str(c) +" m:"+ str(m) + " validés par Théoréme de Hull-Dobell\n=========\n=========\n=========")
        suite_aleatoire = GenerateurSA(x0, a, c, m)
        for valeur_test_saut in range(0,10):
            suite_aleatoire.reset()
            tabTest.append(True) if (test_des_sauts(suite_aleatoire, valeur_test_saut, m)) else tabTest.append(False)
            print("Le test des sauts est réussi pour la valeur " +  str(valeur_test_saut)) if all(tabTest) else print("Le test des sauts à échouer pour la valeur " + str(valeur_test_saut))
        if all(tabTest):
            print("=========\n=========\n=========\nLe test des sauts est réussi pour toutes les valeurs")
        else :
            tabFalse= []
            for i in range(0,len(tabTest)):
                if not tabTest[i] :
                    tabFalse.append(i)
            print("=========\n=========\n=========\nLe test des sauts à échoue pour les valeurs : " + str(tabFalse))
    return all(tabTest)
