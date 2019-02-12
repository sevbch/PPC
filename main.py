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
    new_D=[]
    for d in D:
        new_D.append(copy(d))
    return new_D

def choose_node(nodes_list):
    node=nodes_list.pop(0)
    return node

def print_sol(solution,I):
    for x in range(I.N):
        print("Variable "+str(x)+" affectée a la valeur "+str(solution.Domains[x][0])+"\n")

def main(I):
    
    root_node=Node('',copy_domains(I.Domains))
    nodes_list=[root_node]
    found_feas=False
    nbr_nodes=0
    nbr_fails=0
    
    #print(root_node.Domains)
    
    while nodes_list!=[] and not found_feas:
        
        current_node=choose_node(nodes_list)
        
        #print("My ID",current_node.get_ID())
        
        #print("My before after AC",current_node.Domains)
        
        current_node.AC3(I)
        
        #print("My domain after AC",current_node.Domains)
        
        #current_node.FF()
        
        current_node.set_status()
        status=current_node.get_status()
        
        #print("My status",status)
        
        if status==1: #solution found
            found_feas=True
            solution=current_node
            
        elif status==-1: #unfeasible
            nbr_fails+=1
            current_node=[] #libère la mémoire
            
        else:
            var_ID, var_value = current_node.find_branch()
            current_node.branch(var_ID,var_value)
            nodes_list.append(current_node.left_child)
            nodes_list.append(current_node.right_child)
            
        nbr_nodes+=1
            
            
    if found_feas:
        print_sol(solution,I)
        print("Il y a eu "+str(nbr_nodes)+" noeuds explorés\n")
        print("Il y a eu "+str(nbr_fails)+" échecs\n")
        return solution
    
    else:
        print("Le probleme est infaisable\n")
        return []
t1=time()
I=create_Reines_instance(8)
I.compute_useful_objects()
t2=time()
print("Temps de création : "+str(t2-t1))
main(I)
t3=time()
print("Temps de résolution : "+str(t3-t2))