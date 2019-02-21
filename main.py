# -*- coding: utf-8 -*-
"""
Created on Sat Feb 09 15:46:37 2019

@author: Guillaume
"""

from Solving import solve
from Queens import create_queens_instance
from time import time
from Graph import create_graph_instance


# *** INSTANCE ***

t1 = time()

# *** instance reine
#I = create_queens_instance(4)

# *** instance graphe
filename = "./graphes/anna.col"
I = create_graph_instance(filename)

I.compute_useful_objects()
t2 = time()


# *** PARAMETRES DE RESOLUTION ***

# Si graphe : pour une solution qui minimise le nombre de couleurs utilisées, mettre :
# branching_strat = 1
# var_strat = 1
# search_strat = 1
# look_ahead_strat = 0

# *** style de branchement
branching_strat = 1
# 0 : branchement binaire, on coupe le domaine d'une variable en 2
# 1 : branchement avec au plux d_max branches : on fixe les valeurs d'une variable dans l'instanciation partielle

# *** variable de branchement
var_strat = 1
# 0 : on branche sur la variable de plus grand domaine (cf branching_strat = 0)
# 1 : on branche sur la variable de plus petit domaine (cf branching_strat = 1)

# *** stratégie de parcours
search_strat = 1
# 0 : en largeur
# 1 : en profondeur

# *** stratégie look-ahead
look_ahead_strat = 0
# 0 : maintain arc consistency
# 1 : forward checking

print("Temps de création : "+str(t2-t1))

solve(I,branching_strat,var_strat,search_strat,look_ahead_strat)

t3 = time()
print("Temps de résolution : "+str(t3-t2))