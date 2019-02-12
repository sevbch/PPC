# -*- coding: utf-8 -*-
"""
Created on Tue Feb 05 11:14:42 2019

@author: Guillaume
"""
from copy import copy

class Node:
    
    def __init__(self,ID,var_domains):
        self.ID=ID
        self.Domains=var_domains
        
    def revise(self,x,y,x_value,I):
        """Essaie de trouver y_value pour y tel que (x_value,y_value) soit faisable pour (x,y)"""
        c_id=I.Cons_ID[x][y]
        for y_value in self.Domains[y]:
            if I.Cons_Tuple[c_id][x_value][y_value]:
                return True
        return False
        
    def AC3(self,Instance):
        I=Instance
        aTester=[] #liste des paires à tester
        for x in range(I.N):
            for y in range(x):
                if I.Cons_ID[x][y]!=-1:
                    aTester.append((x,y))
        #print("here",aTester)
        while aTester!=[]:
            (x,y)=aTester.pop()
            #print(x,self.Domains[x])
            for x_value in self.Domains[x]:    
                supported=self.revise(x,y,x_value,I)
                #print(supported)
                if not supported:
                    self.Domains[x].remove(x_value)
                    for y2 in I.Uni[x]:
                        if y2<x:
                            aTester.append((x,y2))
                        else:
                            aTester.append((y2,x))
        
    def FF(self):
        return
    
    def get_ID(self):
        return self.ID
    
    def set_status(self):
        status=1
        for d in self.Domains:
            if len(d)>=2:
                status=0
            if len(d)==0:
                status=-1
                break    
        self.status=status
        return
    
    def get_status(self):
        return self.status
    
    def copy_domains(self):
        new_D=[]
        for d in self.Domains:
            new_D.append(copy(d))
        return new_D
    
    def find_branch(self):
        best_length=0
        for d in range(len(self.Domains)):
            if len(self.Domains[d])>best_length:
                best_id=d
                best_length=len(self.Domains[d])
        #print("best var to branch",best_id)
        mid=int(len(self.Domains[best_id])/2)
        value=(self.Domains[best_id][mid-1] + self.Domains[best_id][mid])/2.            
        return best_id, value
    
    def branch(self,var,value):
        ID_left = self.get_ID() +'0'
        ID_right = self.get_ID() +'1'
        D_left=self.copy_domains()
        D_right=self.copy_domains()
        idx=0
        while D_left[var][idx]<=value:
            idx+=1
        D_left[var]=D_left[var][0:idx]
        D_right[var]=D_right[var][idx::]
        self.left_child=Node(ID_left,D_left)
        self.right_child=Node(ID_right,D_right)