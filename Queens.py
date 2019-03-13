# -*- coding: utf-8 -*-
"""
Created on Sat Feb 09 16:51:15 2019

@author: Guillaume
"""

from Instance import Instance

def create_queens_instance(n,breakS=False):
    var_domains = [list(range(1,n+1)) for i in range(n)]
    constraints_list = []
    Uni = [[] for i in range(n)]
    # Uni[x] est la liste des variables dont les contraintes touchent x
    Cons_ID = [[-1 for i in range(j)] for j in range(n)]
    # Cons_ID[x][y] renvoie l'ID de la contrainte C(x,y), et -1 sinon. On impose TOUJOURS x_ID>y_ID
    Cons_Tuple = []
    # Cons_Tuple[ID][val1][val2] renvoie True si la contrainte ID accepte le tuple (val1,val2)
    if breakS:
        if n%2==0:
            m=n/2
        else:
            m=(n+1)/2
        var_domains[0]=list(range(1,m+1))
    for x in range(n):
        for y in range(x):
            Cons_Tuple.append([[False for d in range(n+1)] for d in range(n+1)])
            Uni[x].append(y)
            Uni[y].append(x)
            for x_value in var_domains[x]:
                for y_value in var_domains[y]:
                    if x_value != y_value and x_value - y_value != x - y and y_value - x_value != x - y:
                        Cons_Tuple[-1][x_value][y_value] = True
            Cons_ID[x][y] = len(Cons_Tuple)-1
    I = Instance(n,var_domains,constraints_list,0,Uni,Cons_ID,Cons_Tuple)
    return I