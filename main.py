# -*- coding: utf-8 -*-
"""
Created on Sat Feb 09 15:46:37 2019

@author: Guillaume
"""
from Instance import Instance
from Solving import solve, print_sol
from Queens import create_queens_instance
from time import time
from Graph import create_graph_instance
from Node import Node
from copy import deepcopy as dcopy
import pandas as pd


# ****************** PARAMETRES DE RESOLUTION ******************
# Si graphe : pour une solution qui minimise le nombre de couleurs utilisées, mettre :
# branching_strat = 1
# var_strat = 1
# search_strat = 1
# look_ahead_strat = 0
# --------------------- style de branchement ---------------------
branching_strat = 2
# 0 : branchement binaire, on coupe le domaine d'une variable en 2
# 1 : branchement avec au plux d_max branches : on fixe les valeurs d'une variable dans l'instanciation partielle
# 2 : pareil que 1 mais en créant seulement 1 noeud à la fois (moins gourmand en mémoire)
# --------------------- variable de branchement ---------------------
var_strat = 1
# 0 : on branche sur la variable de plus grand domaine (cf branching_strat = 0)
# 1 : on branche sur la variable de plus petit domaine (cf branching_strat = 1)
# 2 : aléatoire
# --------------------- stratégie de parcours ---------------------
search_strat = 1
# 0 : en largeur
# 1 : en profondeur
# 2 : en profondeur, mais le fils est choisi aléatoirement (ne marche qu'avec branching_strat=1)
# --------------------- stratégie look-ahead ---------------------
look_ahead_strat = 1
# 0 : maintain arc consistency
# 1 : forward checking
# 2 : FC+AC
# 3 : FC + AC de temps en temps
# --------------------- recherche dynamique ---------------------
dynamic_search=True
# change de branche et de stratégie automatiquement si le problème semble difficile
# la recherche dynamique ne tient pas compte des paramètres ci-dessus



# ****************** INSTANCE & RESOLUTION ******************
# --------------------- reines ---------------------
"""
t1 = time()
I_Q = create_queens_instance(15)
t2 = time()
print("Temps de création : "+str(t2-t1))
sol, nb_col, nbr_nodes,nbr_fails,br_time,ac_time,fc_time = solve(I_Q,branching_strat,var_strat,search_strat,look_ahead_strat,dynamic_search)
t3 = time()
print("Temps de résolution : "+str(t3-t2))
print_sol(sol,I_Q)
"""

# --------------------- graphes ---------------------

def coloring_graph(filename,branching_strat,var_strat,search_strat,look_ahead_strat, time_limit):
    
    t1 = time()
    I2 = create_graph_instance(filename)
    LB = I2.lb
#    print("Clique max dans ce graphe (borne inf au nombre chromatique) : ",LB)
    I2.compute_useful_objects()
    t2 = time()
#    print("Temps de création : "+str(t2-t1))
    
    it = 1
    print("\n"+"Résolution numéro : "+str(it)+"\n")
    sol, nb_col, nbr_nodes,nbr_fails,br_time,ac_time,fc_time = solve(I2,branching_strat,var_strat,
                                                                     search_strat,look_ahead_strat,dynamic_search,time_limit)
    print("Nombre de couleurs utilisées : "+str(nb_col)+"\n")
    
    while sol != [] and nb_col != LB and time()-t2<time_limit:
        bestsol=dcopy(sol.Domains)
        t1 = time()
        I = create_graph_instance(filename,nb_col-1)
        print(I.N,I.M)
        if I!=[]:
            I.compute_useful_objects()
            t2 = time()
            print("Temps de création : "+str(t2-t1))
            sol, nb_col, nbr_nodes,nbr_fails,br_time,ac_time,fc_time = solve(I,branching_strat,var_strat,
                                                                     search_strat,look_ahead_strat,dynamic_search,time_limit)
            t3 = time()
            print("Nombre de couleurs utilisées : "+str(nb_col))
            #print_sol(sol, I)
            print("Temps de résolution : "+str(t3-t2))
        else:
            t2 = time()
            print("Temps de création : "+str(t2-t1))
            print("Problème infaisable par clique max")
        it += 1
    
    if time()-t2 >= time_limit:
        return 0, 0
    else:
        return bestsol, time()-t2


# ****************** résolution ******************
#filename = "./graphes/jean.col" # solution exacte : 10
#filename = "./graphes/myciel3.col" # solution exacte : 4
#filename = "./graphes/myciel4.col" # solution exacte : 5
#filename = "./graphes/myciel5.col" # solution exacte : 6
#filename = "./graphes/queen10_10.col" # solution exacte : ?
filename = "./graphes/miles1000.col" # solution exacte : 42
#filename = "./graphes/DSJC125.9.col" # solution exacte : ?
#filename = "./graphes/fpsol2.i.1.col" # solution exacte : 65
#filename = "./graphes/queen14_14.col" # solution exacte : ?


#coloring_graph(filename,branching_strat,var_strat,search_strat,look_ahead_strat)



# vieille méthode pour checker
t1 = time()
I = create_graph_instance(filename)
if I!=[]:
    t2 = time()
    print("Temps de création : "+str(t2-t1))
    sol, nb_col, nbr_nodes,nbr_fails,br_time,ac_time,fc_time = solve(I, branching_strat, var_strat, search_strat, look_ahead_strat, dynamic_search)
    t3 = time()
    print("Nombre de couleurs utilisées : "+str(nb_col))
    #print_sol(sol, I)
    print("Temps de résolution : "+str(t3-t2))
else:
    t2 = time()
    print("Temps de création : "+str(t2-t1))
    print("Problème infaisable par clique max")
