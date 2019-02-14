# -*- coding: utf-8 -*-
"""
Created on Tue Feb 05 11:14:42 2019

@author: Guillaume
"""
from copy import copy

class Node:
    
    def __init__(self,ID,var_domains):
        self.ID = ID
        self.Domains = var_domains
        self.father_var = 0
        
    def revise(self,x,y,x_value,I):
        """Essaie de trouver y_value pour y tel que (x_value,y_value) soit faisable pour C(x,y)"""
        c_id = I.Cons_ID[x][y]
        for y_value in self.Domains[y]:
            if I.Cons_Tuple[c_id][x_value][y_value]:
                return True
        return False
        
    def AC3(self,I):
        aTester = [] #liste des paires à tester
        for x in range(I.N):
            for y in range(x):
                if I.Cons_ID[x][y] != -1:
                    aTester.append((x,y))
        #print("here",aTester)
        while aTester != []:
            (x,y) = aTester.pop()
            #print(x,self.Domains[x])
            for x_value in self.Domains[x]:    
                supported = self.revise(x,y,x_value,I)
                #print(supported)
                if not supported:
                    self.Domains[x].remove(x_value)
                    for y2 in I.Uni[x]:
                        if y2 < x:
                            aTester.append((x,y2))
                        else:
                            aTester.append((y2,x))
    
    def AC4(self,I):
        # initialisation
        Q = []
        S = [[[] for d in range(I.d_max+1)] for y in range(I.N)]
        Count = [[[0 for d in range(I.d_max+1)] for y in range(I.N)] for x in range(I.N)]
        for x in range(I.N):
            for y in range(x):
                if I.Cons_ID[x][y] != -1:
                    c_id = I.Cons_ID[x][y]
                    for a in self.Domains[x]:
                        for b in self.Domains[y]:
                            if I.Cons_Tuple[c_id][a][b]:
                                Count[x][y][a] += 1
                                S[y][b].append((x,a))
                        if Count[x][y][a] == 0:
                            self.Domains[x].remove(a)
                            Q.append((x,a))
        # AC4
        while Q != []:
            (y,b) = Q.pop()
            for (x,a) in S[y][b]:
                Count[x][y][a] -= 1
                if Count[x][y][a] == 0 and a in self.Domains[x]:
                    self.Domains[x].remove(a)
                    Q.append((x,a))
    
    def FC(self, I):
        x = self.father_var
        a = self.Domains[x][0]
        for y in range(x):
            if I.Cons_ID[x][y] != -1:
                c_id = I.Cons_ID[x][y]
                for b in self.Domains[y]:
                    if not I.Cons_Tuple[c_id][a][b]:
                        self.Domains[y].remove(b)
    
    def get_ID(self):
        return self.ID
    
    def set_status(self):
        status = 1
        for d in self.Domains:
            if len(d) >= 2:
                status = 0
            if len(d) == 0:
                status =- 1
                break
        self.status = status
        return
    
    def get_status(self):
        return self.status
    
    def copy_domains(self):
        new_D = []
        for d in self.Domains:
            new_D.append(copy(d))
        return new_D
    
    
    def find_branch(self,var_strat):
        
        if var_strat == 0:
            best_length = 0
            for d in range(len(self.Domains)):
                if len(self.Domains[d]) > best_length:
                    best_id = d
                    best_length = len(self.Domains[d])
            #print("best var to branch",best_id)
            mid = int(len(self.Domains[best_id])/2)
            value = (self.Domains[best_id][mid-1] + self.Domains[best_id][mid])/2.            
            return best_id, value
        
        elif var_strat == 1:
            shortest_length = 10000 # max(len(self.Domains[d])for d in range(len(self.Domains)))+1
            for d in range(len(self.Domains)):
                if len(self.Domains[d]) < shortest_length and len(self.Domains[d]) >= 2:
                    best_id = d
                    shortest_length = len(self.Domains[d])          
            return best_id, 0
        
        else:
            print ("cette stratégie de branchement n'existe pas")
    
    
    def branch(self,var,value,branching_strat):
        
        if branching_strat == 0:
            ID_left = self.get_ID() +'0'
            ID_right = self.get_ID() +'1'
            D_left = self.copy_domains()
            D_right = self.copy_domains()
            idx = 0
            while D_left[var][idx] <= value:
                idx += 1
            D_left[var] = D_left[var][0:idx]
            D_right[var] = D_right[var][idx::]
            self.branch = []
            self.branch.append(Node(ID_left,D_left))
            self.branch[0].father_var = var
            self.branch.append(Node(ID_right,D_right))
            self.branch[1].father_var = var
            
        elif branching_strat == 1:
            k = 0
            self.branch = []
            for val in self.Domains[var]:
                ID_branch = self.get_ID() + str(k)
                D_branch = self.copy_domains()
                D_branch[var].clear()
                D_branch[var].append(val)
                self.branch.append(Node(ID_branch,D_branch))
                self.branch[k].father_var = var
                k += 1
        else:
            print ("ce style de branchement n'existe pas")


















