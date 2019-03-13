# -*- coding: utf-8 -*-
"""
Created on Tue Feb 05 11:00:17 2019

@author: Guillaume
"""
from copy import copy
from copy import deepcopy as dcopy

class Instance:
    
    def __init__(self,nbr_var,var_domains,constraints_list,lower_bound=0,Uni=None,Cons_ID=None,Cons_Tuple=None):
        self.N = nbr_var
        self.M = len(constraints_list)
        self.Domains = var_domains
        self.d_max = 0
        for i in range(nbr_var):
            d = max(var_domains[i])
            if d > self.d_max:
                self.d_max = d
        if Uni==None:
            self.Constraints = constraints_list
        self.lb = lower_bound
        self.Uni=Uni
        self.Cons_ID=Cons_ID
        self.Cons_Tuple=Cons_Tuple
     
    """Obsolète    
    def compute_useful_objects(self):
        
        Uni = [[] for i in range(self.N)]
        # Uni[x] est la liste des variables dont les contraintes touchent x
        Cons_ID = [[-1 for i in range(j)] for j in range(self.N)]
        # Cons_ID[x][y] renvoie l'ID de la contrainte C(x,y), et -1 sinon. On impose TOUJOURS x_ID>y_ID
        Cons_Tuple = [[[False for d in range(self.d_max+1)] for d in range(self.d_max+1)] for m in range(self.M)]
        # Cons_Tuple[ID][val1][val2] renvoie True si la contrainte ID accepte le tuple (val1,val2)
        for c in range(self.M):
            Cons = self.Constraints[c]
            x_ID = Cons[0]
            y_ID = Cons[1]
            tuples = Cons[2]
            Uni[x_ID].append(y_ID)
            Uni[y_ID].append(x_ID)
            Cons_ID[x_ID][y_ID] = c
            for (val1,val2) in tuples:
                Cons_Tuple[c][val1][val2] = True
            self.Constraints[c]=[] #libère la mémoire
        self.Uni = Uni
        self.Cons_ID = Cons_ID
        self.Cons_Tuple = Cons_Tuple
        self.Constraints=[] #libère la mémoire
    """
    def copy_instance(self):
        n = copy(self.N)
        var_domains = dcopy(self.Domains)
        constraints_list = dcopy(self.Constraints)
        return Instance(n,var_domains,constraints_list)
    
            