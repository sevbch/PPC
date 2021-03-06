# -*- coding: utf-8 -*-
"""
Created on Wed Feb 20 22:10:45 2019

@author: sev
"""

from Node import Node
from copy import copy
import numpy as np
from time import time
from Graph import create_graph_instance
from copy import deepcopy as dcopy
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
        print("Variable "+str(x)+" affectée à la valeur "+str(solution.Domains[x][0]))
        tab[x][solution.Domains[x][0]-1]=1
    print(tab)
        


def solve(I,branching_strat,var_strat,search_strat,look_ahead_strat,dynamic_search, time_limit=100000000000):
    
    t_ini = time()
    
    if dynamic_search:
        branching_strat = 2
        var_strat = 1
        search_strat = 1
        look_ahead_strat = 1

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
    br3_time=0
    #print(root_node.Domains)
    
    while nodes_list != [] and not found_feas and time()-t_ini<time_limit:
        
        #print([node.ID for node in nodes_list])
        current_node = choose_node(nodes_list,search_strat,nchildren)
        #print(current_node.ID)
        
#        print("itération "+str(nbr_nodes)+"\n")
        
        #print("My ID",current_node.get_ID())
        
        #print("My domain before AC",current_node.Domains)
        
        # *** stratégie look ahead ***
        if nbr_nodes<0:
            b1=time()
            current_node.AC3(I)
            b2=time()
            ac_time+=b2-b1

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
            elif look_ahead_strat == 3:
                b1=time()
                count_FC+=current_node.FC(I)
                b2=time()
                fc_time+=b2-b1
                
                if len(current_node.ID)%30==0:
                    b1=time()
                    current_node.AC3(I)
                    b2=time()
                    ac_time+=b2-b1
            else:
                print("Pas de stratégie valide")
        
        #print("My domain after AC",current_node.Domains)
        
        #input()
        
        current_node.set_status()
        status = current_node.get_status()

        
        if status == 1: # solution found
            found_feas = True
            solution = current_node
            
        elif status == -1: # unfeasible
            nbr_fails += 1
            del current_node #libère la mémoire
            nchildren=0
            if nbr_nodes == 0: # on est à la racine ==> infaisable
                break
            
        else:
            b1=time()
            var_ID, var_value = current_node.find_branch(var_strat)
            b3=time()
            #current_node.branch(var_ID,var_value,branching_strat)
            #nchildren=len(current_node.branches)
            #for k in range(nchildren):
             #   nodes_list.append(current_node.branches[k])
            new_nodes=current_node.branch(var_ID,var_value,branching_strat)
            nchildren=len(new_nodes)
            nodes_list+=new_nodes
            b2=time()
            br_time+=b2-b1
            br3_time+=b3-b1
            del current_node #libère la mémoire
                
        nbr_nodes += 1
        
        if dynamic_search and nbr_nodes%10000==0:
            branching_strat=1
            search_strat=2
            n=nodes_list.pop(0)
            nodes_list.append(n)
        
        if nbr_nodes%100000==0:
            print("Progress report")
            print(nbr_nodes)
            print("Noeuds en memoire "+str(len(nodes_list)))
            print("Il y a eu "+str(nbr_nodes)+" noeud(s) exploré(s)")
            print("Il y a eu "+str(nbr_fails)+" échec(s)")
            print("Le FC a enlevé "+str(count_FC)+" fois des variables")
            print("Temps passé à brancher seulement : "+str(br_time))
            print("Temps passé à brancher seulement (br3) : "+str(br3_time))
            print("Temps passé sur l'AC : "+str(ac_time))
            print("Temps passé sur le FC : "+str(fc_time)+"\n")
            print("Temps total écoulé : "+str(time()-start))
            
        
    if found_feas:
#        print_sol(solution,I)
        print("Il y a eu "+str(nbr_nodes)+" noeud(s) exploré(s)")
        print("Il y a eu "+str(nbr_fails)+" échec(s)")
        print("Le FC a enlevé "+str(count_FC)+" fois des variables")
        print("Temps passé à brancher seulement : "+str(br_time))
        print("Temps passé sur l'AC : "+str(ac_time))
        print("Temps passé sur le FC : "+str(fc_time)+"\n")
        return solution, nb_col(solution,I), nbr_nodes,nbr_fails,br_time,ac_time,fc_time

    elif time()-t_ini >= time_limit:
#        print("Temps limite atteint")
        return [], 0, 0, 0, 0, 0, 0
    
    else:
        print("***** Le problème est infaisable *****")
        print("Il y a eu "+str(nbr_nodes)+" noeud(s) exploré(s)")
        print("Il y a eu "+str(nbr_fails)+" échec(s)")
        print("Le FC a enlevé "+str(count_FC)+" fois des variables")
        print("Temps passé à brancher seulement : "+str(br_time))
        print("Temps passé sur l'AC : "+str(ac_time))
        print("Temps passé sur le FC : "+str(fc_time)+"\n")
        return [], 0, 0, 0, 0, 0, 0
    
    



def coloring_graph(filename,branching_strat,var_strat,search_strat,look_ahead_strat,dynamic_search,time_limit_int,time_limit_tot):
    
    t_ini = time()
    it = 1
    time_it = []
    nb_nodes_it=[]
    print("\n"+"Résolution numéro : "+str(it))
    I = create_graph_instance(filename)
    print("Temps de création : "+str(time()-t_ini))
    LB = I.lb
    t2 = time()
    sol, nb_col, nbr_nodes,nbr_fails,br_time,ac_time,fc_time = solve(I,branching_strat,var_strat,
                                                                     search_strat,look_ahead_strat,dynamic_search,time_limit_int)
    t3 = time()
    time_it.append(t3-t2)
    print("Nombre de couleurs utilisées : "+str(nb_col))        
    print("Nombre de noeuds : "+str(nbr_nodes))
    bestcol = nb_col
    col_it = []
    col_it.append(nb_col)
    nb_nodes_it.append(nbr_nodes)
    
    while sol != [] and nb_col != LB and time()-t_ini < time_limit_tot:
        bestsol = dcopy(sol.Domains)
        t1 = time()
        I = create_graph_instance(filename,nb_col-1)
        it += 1
        if I!=[]:
            t2 = time()
            print("\n"+"Résolution numéro : "+str(it))
            print("Temps de création : "+str(t2-t1))
            sol, nb_col, nbr_nodes,nbr_fails,br_time,ac_time,fc_time = solve(I,branching_strat,var_strat,
                                                                     search_strat,look_ahead_strat,dynamic_search,time_limit_int)
            t3 = time()
            time_it.append(t3-t2)            
            print("Nombre de couleurs utilisées : "+str(nb_col))
            print("Nombre de noeuds : "+str(nbr_nodes))
            #print_sol(sol, I)
            print("Temps de résolution : "+str(t3-t2))        
            col_it.append(nb_col)
            nb_nodes_it.append(nbr_nodes)
            if (nb_col > 0 and nb_col < bestcol):
                bestcol = nb_col
        else:   
            t2 = time()
            print("Temps de création : "+str(t2-t1))
            print("Problème infaisable par clique max")
            
    print("\n"+"Nombre de couleurs optimal : "+ str(bestcol))
    
    if time()-t_ini >= time_limit_tot or t3-t2 >= time_limit_int:
        return 0, time()-t_ini, it, time_it, col_it, nb_nodes_it
    else:
        return bestcol, time()-t_ini, it, time_it, col_it, nb_nodes_it
    
    
def sat_graph(filename,nb_col_max,branching_strat,var_strat,search_strat,look_ahead_strat,dynamic_search,time_limit=10000000):
    t1 = time()
    I = create_graph_instance(filename, nb_col_max)
    if I!=[]:
        t2 = time()
        print("Temps de création : "+str(t2-t1))
        sol, nb_col, nbr_nodes,nbr_fails,br_time,ac_time,fc_time = solve(I, branching_strat, var_strat, search_strat, look_ahead_strat, dynamic_search, time_limit)
        t3 = time()
        print("Nombre de couleurs utilisées : "+str(nb_col))
        print("Temps de résolution : "+str(t3-t2))
    else:
        t2 = time()
        print("Temps de création : "+str(t2-t1))
        print("Problème infaisable par clique max")
    return 0