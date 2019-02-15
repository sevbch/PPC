# -*- coding: utf-8 -*-
"""
Created on Sat Feb 09 15:46:37 2019

@author: Guillaume
"""

from Node import Node
from copy import copy
from Reines import create_Reines_instance
from time import time

def copy_domains(D):
    new_D = []
    for d in D:
        new_D.append(copy(d))
    return new_D

def choose_node(nodes_list,search_strat):
    if search_strat == 0:
        node = nodes_list.pop(0)
        return node
    elif search_strat == 1:
        node = nodes_list.pop()
        return node
    else:
        print("cette stratégie n'existe pas")
        return []
    
def print_sol(solution,I):
    for x in range(I.N):
        print("Variable "+str(x)+" affectée à la valeur "+str(solution.Domains[x][0])+"\n")


def main(I,branching_strat,var_strat,search_strat,look_ahead_strat):
    
    root_node = Node('',copy_domains(I.Domains))
    nodes_list = [root_node]
    found_feas = False
    nbr_nodes = 0
    nbr_fails = 0
    #print(root_node.Domains)
    
    while nodes_list != [] and not found_feas:
        
        current_node = choose_node(nodes_list,search_strat)
        
        #print("My ID",current_node.get_ID())
        
        #print("My before after AC",current_node.Domains)
        
        # *** stratégie look ahead ***
        if look_ahead_strat == 0 or (look_ahead_strat == 1 and nbr_nodes == 0) :
            current_node.AC3(I)
        elif look_ahead_strat ==1:
            if nbr_nodes > 0:
                current_node.FC(I)
        
        #print("My domain after AC",current_node.Domains)
        
        current_node.set_status()
        status = current_node.get_status()
        
        #print("My status",status)
        
        if status == 1: # solution found
            found_feas = True
            solution = current_node
            
        elif status == -1: # unfeasible
            nbr_fails += 1
            current_node = [] # libère la mémoire
            
        else:
            var_ID, var_value = current_node.find_branch(var_strat)
            current_node.branch(var_ID,var_value,branching_strat)
            for k in range(len(current_node.branch)):
                nodes_list.append(current_node.branch[k])
                
            
        nbr_nodes += 1
            
            
    if found_feas:
        print_sol(solution,I)
        print("Il y a eu "+str(nbr_nodes)+" noeuds explorés\n")
        print("Il y a eu "+str(nbr_fails)+" échecs\n")
        return solution
    
    else:
        print("Le problème est infaisable\n")
        return []



# *** Résolution & tests ***

t1 = time()
I = create_Reines_instance(4)
I.compute_useful_objects()
t2 = time()
branching_strat = 1 # style de branchement
# 0 : branchement binaire, on coupe le domaine d'une variable en 2
# 1 : branchement avec au plux d_max branches : on fixe les valeurs d'une variable dans l'instanciation partielle
var_strat = 1 # variable de branchement
# 0 : on branche sur la variable de plus grand domaine (cf branching_strat = 0)
# 1 : on branche sur la variable de plus petit domaine (cf branching_strat = 1)
search_strat = 1 # stratégie de parcours
# 0 : en largeur
# 1 : en profondeur
look_ahead_strat = 0 # stratégie look-ahead
# 0 : maintain arc consistency
# 1 : forward checking
print("Temps de création : "+str(t2-t1))
main(I,branching_strat,var_strat,search_strat,look_ahead_strat)
t3 = time()
print("Temps de résolution : "+str(t3-t2))