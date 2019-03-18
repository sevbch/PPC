# -*- coding: utf-8 -*-
"""
Created on Sat Feb 09 15:46:37 2019

@author: Guillaume
"""

from Solving import solve, print_sol, coloring_graph, sat_graph
from Queens import create_queens_instance
from time import time


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
look_ahead_strat = 3
# 0 : maintain arc consistency
# 1 : forward checking
# 2 : FC+AC
# 3 : FC + AC de temps en temps
# --------------------- recherche dynamique ---------------------
dynamic_search = False
# change de branche et de stratégie automatiquement si le problème semble difficile
# la recherche dynamique ne tient pas compte des paramètres ci-dessus


# ****************** INSTANCE & RESOLUTION ******************
# --------------------- reines ---------------------

# --- paramètres : on active la recherche dynamique
dynamic_search = True
t1 = time()
I_Q = create_queens_instance(10) # taille de la grille en paramètre
t2 = time()
print("Temps de création : "+str(t2-t1))
sol, nb_col, nbr_nodes,nbr_fails,br_time,ac_time,fc_time = solve(I_Q,branching_strat,var_strat,search_strat,look_ahead_strat,dynamic_search)
t3 = time()
print("Temps de résolution : "+str(t3-t2))
print_sol(sol,I_Q)


# --------------------- graphes ---------------------

#filename = "./graphes/jean.col" # solution exacte : 10
filename = "./graphes/myciel3.col" # solution exacte : 4
#filename = "./graphes/myciel4.col" # solution exacte : 5
#filename = "./graphes/myciel5.col" # solution exacte : 6
#filename = "./graphes/queen9_9.col" # solution exacte : 9
#filename = "./graphes/miles1000.col" # solution exacte : 42
#filename = "./graphes/DSJC125.9.col" # solution exacte : ?
#filename = "./graphes/fpsol2.i.1.col" # solution exacte : 65
#filename = "./graphes/queen14_14.col" # solution exacte : ?


# --- paramètres : stratégie FC + AC de temps en temps
branching_strat = 2
var_strat = 1
search_strat = 1
look_ahead_strat = 3
dynamic_search=False
time_limit_int = 600 # temps limite pour une résolution lors d'une itération de coloring_graph
time_limit_tot = 1200 # temps limite total de coloring_graph

# --- minimisation du nombre de couleurs utilisées
col, time_tot, nbr_it, time_it, col_it, nb_nodes_it = coloring_graph(filename,branching_strat,var_strat,search_strat,look_ahead_strat,dynamic_search,time_limit_int,time_limit_tot)
print("Temps de résolution total : "+str(time_tot))


# --- faisabilité uniquement
dynamic_search = True
nb_col_max = 6 # nombre maximal de couleurs autorisées
time_limit = 120 # temps limite
sat_graph(filename,nb_col_max,branching_strat,var_strat,search_strat,look_ahead_strat,dynamic_search,time_limit)