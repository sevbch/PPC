# -*- coding: utf-8 -*-
"""
Created on Wed Feb 20 22:10:45 2019

@author: sev
"""

from Node import Node
from copy import copy
import numpy as np
from time import time
np.random.seed(0)


def copy_domains(D):
    new_D = []
    for d in D:
        new_D.append(copy(d))
    return new_D



def choose_node(nodes_list,search_strat,nchildren):
    if search_strat == 0: #en largeur
        node = nodes_list.pop(0)
        return node
    elif search_strat == 1: #en profondeur
        node = nodes_list.pop()
        return node
    elif search_strat == 2: #aléatoire sur les derniers fils
        if nchildren==0:
            node = nodes_list.pop()
            return node
        else:
            rdn=np.random.randint(0,nchildren)
            node = nodes_list.pop(-rdn-1)
            return node
    else:
        print("cette stratégie n'existe pas")
        return []

def nb_col(solution,I):
    col = 0
    for x in range(I.N):
        if solution.Domains[x][0] > col:
            col = solution.Domains[x][0]
    return col
    
def print_sol(solution,I):
    tab=np.zeros((I.N,I.N))
    for x in range(I.N):
        print("Variable "+str(x)+" affectée à la valeur "+str(solution.Domains[x][0])+"\n")
        #tab[x][solution.Domains[x][0]-1]=1
    #print(tab)
        


def solve(I,branching_strat,var_strat,search_strat,look_ahead_strat):
    
    root_node = Node('',copy_domains(I.Domains))
    nodes_list = [root_node]
    found_feas = False
    nbr_nodes = 0
    nbr_fails = 0
    count_FC = 0
    nchildren=1
    br_time=0
    ac_time=0
    fc_time=0
    #print(root_node.Domains)
    
    while nodes_list != [] and not found_feas:
        
        #print([node.ID for node in nodes_list])
        current_node = choose_node(nodes_list,search_strat,nchildren)
        #print(current_node.ID)
        
#        print("itération "+str(nbr_nodes)+"\n")
        
        #print("My ID",current_node.get_ID())
        
        #print("My domain before AC",current_node.Domains)
        
        # *** stratégie look ahead ***
        if nbr_nodes == 0: # on est à la racine ==> on fait AC
            b1=time()
            current_node.AC3(I)
            b2=time()
            ac_time+=b2-b1
#            print("coucou")
        else:
            if look_ahead_strat == 0:
                b1=time()
                current_node.AC3(I)
                b2=time()
                ac_time+=b2-b1
            elif look_ahead_strat == 1:
                b1=time()
                count_FC+=current_node.FC(I)
                b2=time()
                fc_time+=b2-b1
            elif look_ahead_strat == 2:
                b1=time()
                count_FC+=current_node.FC(I)
                b2=time()
                fc_time+=b2-b1
                
                b1=time()
                current_node.AC3(I)
                b2=time()
                ac_time+=b2-b1
        
        #print("My domain after AC",current_node.Domains)
        
        #input()
        
        current_node.set_status()
        status = current_node.get_status()
#        if nbr_nodes == 0: # on est à la racine ==> on fait AC
#            print("status à la première itération : "+str(status)+"\n")
        
#        print("My status",status)
        
        if status == 1: # solution found
            found_feas = True
            solution = current_node
            
        elif status == -1: # unfeasible
            nbr_fails += 1
            current_node = [] # libère la mémoire
            nchildren=0
            if nbr_nodes == 0: # on est à la racine ==> infaisable
#                print("on est ici")
                break
            
        else:
            b1=time()
            var_ID, var_value = current_node.find_branch(var_strat)
            current_node.branch(var_ID,var_value,branching_strat)
            nchildren=len(current_node.branch)
            for k in range(nchildren):
                nodes_list.append(current_node.branch[k])
            nchildren=len(current_node.branch)
            b2=time()
            br_time+=b2-b1
                
        
        nbr_nodes += 1
        if nbr_nodes%10000==0:
            print(nbr_nodes)
            
            
    if found_feas:
        #print_sol(solution,I)
        print("Il y a eu "+str(nbr_nodes)+" noeud(s) exploré(s)\n")
        print("Il y a eu "+str(nbr_fails)+" échec(s)\n")
        print("Le FC a enlevé "+str(count_FC)+" fois des variables")
        print("Temps passé à brancher seulement : "+str(br_time))
        print("Temps passé sur l'AC : "+str(ac_time))
        print("Temps passé sur le FC : "+str(fc_time))
        return solution, nb_col(solution,I)
    
    else:
        print("Le problème est infaisable\n")
        return [], 0



