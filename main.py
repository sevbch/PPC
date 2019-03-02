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


# ****************** PARAMETRES DE RESOLUTION ******************
# Si graphe : pour une solution qui minimise le nombre de couleurs utilisées, mettre :
# branching_strat = 1
# var_strat = 1
# search_strat = 1
# look_ahead_strat = 0
# --------------------- style de branchement ---------------------
branching_strat = 1
# 0 : branchement binaire, on coupe le domaine d'une variable en 2
# 1 : branchement avec au plux d_max branches : on fixe les valeurs d'une variable dans l'instanciation partielle
# --------------------- variable de branchement ---------------------
var_strat = 1
# 0 : on branche sur la variable de plus grand domaine (cf branching_strat = 0)
# 1 : on branche sur la variable de plus petit domaine (cf branching_strat = 1)
# --------------------- stratégie de parcours ---------------------
search_strat = 1
# 0 : en largeur
# 1 : en profondeur
# 2 : en profondeur, mais le fils est choisi aléatoirement
# --------------------- stratégie look-ahead ---------------------
look_ahead_strat = 2
# 0 : maintain arc consistency
# 1 : forward checking
# 2 : FC+AC
# 3 : FC + AC de temps en temps



# ****************** INSTANCE & RESOLUTION ******************

"""
# --------------------- reines ---------------------
t1 = time()
#I_Q = create_queens_instance(125)
print(time()-t1)
#I_Q.compute_useful_objects()
t2 = time()
print("Temps de création : "+str(t2-t1))
sol, nb_col = solve(I_Q,branching_strat,var_strat,search_strat,look_ahead_strat)
t3 = time()
#print_sol(sol, I_Q)
print("Temps de résolution : "+str(t3-t2))
"""


# --------------------- graphes ---------------------

def coloring_graph(filename,branching_strat,var_strat,search_strat,look_ahead_strat):
    
    t1 = time()
    I2 = create_graph_instance(filename)
    I2.compute_useful_objects()
    t2 = time()
    print("Temps de création : "+str(t2-t1))
    
    sol2, nb_col2 = solve(I2,branching_strat,var_strat,search_strat,look_ahead_strat)
    sol1, nb_col1 = sol2, nb_col2
    I1 = I2.copy_instance()
    I1.compute_useful_objects()
    
    while sol2 != []:
        
        # on garde en mémoire la solution précédente
        sol1, nb_col1 = sol2, nb_col2
        del I1
        I1 = I2.copy_instance()
        del I2
        
        # on réduit le domaine
        n = I1.N
        var_domains = [list(reversed(range(1,nb_col2))) for x in range(n)]
        constraints_list = []
        for x in range(n):
            for y in range(x):
                tuple_list = []
                for x_value in var_domains[x]:
                    for y_value in var_domains[y]:
                        if x_value != y_value:
                            tuple_list.append((x_value,y_value))
                constraints_list.append((x,y,tuple_list))
        I2 = Instance(n,var_domains,constraints_list)
        I2.compute_useful_objects()
        
        # on regarde si c'est faisable
        sol2, nb_col2 = solve(I2,branching_strat,var_strat,search_strat,look_ahead_strat)
    
    t3 = time()
    print_sol(sol1,I1)
    print("Nombre de couleurs utilisées : "+str(nb_col1))
    print("Temps de résolution : "+str(t3-t2))



# ****************** résolution ******************
#filename = "./graphes/jean.col" # solution exacte : 10
#filename = "./graphes/myciel3.col" # solution exacte : 4
#filename = "./graphes/myciel4.col" # solution exacte : 5
filename = "./graphes/myciel5.col" # solution exacte : 6
#filename = "./graphes/queen10_10.col" # solution exacte : 10
#filename = "./graphes/miles1000.col" # solution exacte : 42
#coloring_graph(filename,branching_strat,var_strat,search_strat,look_ahead_strat)



# vieille méthode pour checker
t1 = time()
I = create_graph_instance(filename,5)
print(I.N,I.M)
if I!=[]:
    I.compute_useful_objects()
    t2 = time()
    print("Temps de création : "+str(t2-t1))
    sol, nb_col = solve(I,branching_strat,var_strat,search_strat,look_ahead_strat)
    t3 = time()
    print("Nombre de couleurs utilisées : "+str(nb_col))
    #print_sol(sol, I)
    print("Temps de résolution : "+str(t3-t2))
else:
    t2 = time()
    print("Temps de création : "+str(t2-t1))
    print("Problème infaisable par clique max")
