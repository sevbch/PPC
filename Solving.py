# -*- coding: utf-8 -*-
"""
Created on Wed Feb 20 22:10:45 2019

@author: sev
"""

from Node import Node
from copy import copy

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


def solve(I,branching_strat,var_strat,search_strat,look_ahead_strat):
    
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



