# -*- coding: utf-8 -*-
"""
Created on Tue Feb 05 11:14:42 2019

@author: Guillaume
"""
import numpy.random as rdn

def remove_values_from_list(the_list, val):
   return [value for value in the_list if value != val]

class Node:
    
    def __init__(self,ID,var_domains):
        self.ID = ID
        self.Domains = var_domains
        self.father_var = 0
        self.status = 10 # initialisation à une valeur quelquonque
        self.to_check=[]
        
    def revise(self,x,y,x_value,I):
        """Essaie de trouver y_value pour y tel que (x_value,y_value) soit faisable pour C(x,y)"""
        if x>y:
            c_id = I.Cons_ID[x][y]
            for y_value in self.Domains[y]:
                if I.Cons_Tuple[c_id][x_value][y_value]:
                    #print("La variable "+str(x)+" de valeur "+str(x_value) +" est ok\navec la variable "+str(y)+" de valeur "+str(y_value))
                    return True
            #print("La variable "+str(x)+" de valeur "+str(x_value) +" n'est pas ok\navec la variable "+str(y))
            return False
        else:
            c_id = I.Cons_ID[y][x]
            for y_value in self.Domains[y]:
                if I.Cons_Tuple[c_id][y_value][x_value]:
                    #print("La variable "+str(x)+" de valeur "+str(x_value) +" est ok\navec la variable "+str(y)+" de valeur "+str(y_value))
                    return True
            #print("La variable "+str(x)+" de valeur "+str(x_value) +" n'est pas ok\navec la variable "+str(y))
            return False
        
    def AC1(self,I):
        term=False
        infeasible = False
        while not term and not infeasible:
            term=True
            for x in range(I.N):
                for y in range(x):
                    if I.Cons_ID[x][y] != -1:
                        toPOP=[]
                        for x_value in self.Domains[x]:  
                            supported = self.revise(x,y,x_value,I)
                            if not supported:
                                toPOP.append(x_value)
                                term=False
                        for x_value in toPOP:
                            self.Domains[x].remove(x_value)
                            if len(self.Domains[x]) == 0:
                                self.status = -1
#                                print("infaisabilité détectée dans AC, status : "+str(self.status))
                                infeasible = True
                                break
                        toPOP=[]
                        for y_value in self.Domains[y]:  
                            supported = self.revise(y,x,y_value,I)
                            if not supported:
                                toPOP.append(y_value)
                                term=False
                        for y_value in toPOP:
                            self.Domains[y].remove(y_value)
                            if len(self.Domains[y]) == 0:
                                self.status = -1
#                                print("infaisabilité détectée dans AC, status : "+str(self.status))
                                infeasible = True
                                break
                        
        
    def AC3(self,I):
        aTester = [] #liste des paires à tester
        if self.ID=='':
            for x in range(I.N):
                for y in I.Uni[x]:
                    if x>y:
                        aTester.append((x,y))
                        aTester.append((y,x))
        else:
            for x in self.to_check:
                for y in I.Uni[x]:
                    aTester.append((x,y))
                    aTester.append((y,x))
        infeasible = False
        while aTester != [] and not infeasible:
            (x,y) = aTester.pop()
            removed=False
            toPOP=[]
            for x_value in self.Domains[x]:    
                supported = self.revise(x,y,x_value,I)
                if not supported:
                    toPOP.append(x_value)
                    removed=True
            for x_value in toPOP:
                self.Domains[x].remove(x_value)
                if len(self.Domains[x]) == 0:
                    self.status = -1
                    infeasible = True
            if removed:
                for y2 in I.Uni[x]:
                    if y2!=y:
                        aTester.append((y2,x))
    
    def AC4(self,I):
        # initialisation
        Q = []
        S = [[[] for d in range(I.d_max+1)] for y in range(I.N)]
        Count = [[[0 for d in range(I.d_max+1)] for y in range(I.N)] for x in range(I.N)]
        x = 0
        infeasible = False
        while x < I.N and not infeasible:
            for y in range(x):
                if I.Cons_ID[x][y] != -1: # une contrainte lie x et y
                    c_id = I.Cons_ID[x][y]
                    toPOP=[]
                    for a in self.Domains[x]:
                        for b in self.Domains[y]:
                            if I.Cons_Tuple[c_id][a][b]:
                                Count[x][y][a] += 1
                                S[y][b].append((x,a))
                        if Count[x][y][a] == 0:
                            toPOP.append(a)
                    for a in toPOP:
                        self.Domains[x].remove(a)
                        if len(self.Domains[x]) == 0:
                            self.status = -1
#                            print("infaisabilité détectée dans AC, status : "+str(self.status))
                            infeasible = True
                            break
                        Q.append((x,a))
                    toPOP=[]
                    for a in self.Domains[y]:
                        for b in self.Domains[x]:
                            if I.Cons_Tuple[c_id][b][a]:
                                Count[y][x][a] += 1
                                S[x][b].append((y,a))
                        if Count[y][x][a] == 0:
                            toPOP.append(a)
                    for a in toPOP:
                        self.Domains[y].remove(a)
                        if len(self.Domains[y]) == 0:
                            self.status = -1
#                            print("infaisabilité détectée dans AC, status : "+str(self.status))
                            infeasible = True
                            break
                        Q.append((y,a))
            x += 1
        # AC4
        while Q != [] and not infeasible:
            (y,b) = Q.pop()
            for (x,a) in S[y][b]:
                Count[x][y][a] -= 1
                if ((Count[x][y][a] == 0) and (a in self.Domains[x])):
                    self.Domains[x].remove(a)
                    if len(self.Domains[y]) == 0:
                            self.status = -1
#                            print("infaisabilité détectée dans AC, status : "+str(self.status))
                            infeasible = True
                            break
                    Q.append((x,a))
    
    def FC(self, I):
        count=0
        if len(self.Domains[self.father_var]) == 1:
            list_FC = [self.father_var]
            infeasible = False
            while list_FC!=[] and not infeasible:
                x=list_FC.pop()
                a = self.Domains[x][0]
                y_idx=0
                max_y_idx=len(I.Uni[x])
                while not infeasible and y_idx < max_y_idx:
                    y=I.Uni[x][y_idx]
                    if x>y:
                        c_id = I.Cons_ID[x][y]
                        toPOP=[]
                        for b in self.Domains[y]:
                            if not I.Cons_Tuple[c_id][a][b]:
                                toPOP.append(b)
                        if toPOP!=[]:
                            self.to_check.append(y)
                            for b in toPOP:
                                self.Domains[y].remove(b)
                                count+=1
                            Dy=len(self.Domains[y])
                            if Dy == 0:
                                self.status = -1
                                infeasible = True
                                break
                            elif Dy==1:
                                list_FC.append(y)
                    else:
                        c_id = I.Cons_ID[y][x]
                        toPOP=[]
                        for b in self.Domains[y]:
                            if not I.Cons_Tuple[c_id][b][a]:
                                toPOP.append(b)
                        if toPOP!=[]:
                            self.to_check.append(y)
                            for b in toPOP:
                                self.Domains[y].remove(b)
                                count+=1
                            Dy=len(self.Domains[y])
                            if Dy == 0:
                                self.status = -1
                                infeasible = True
                                break
                            elif Dy==1:
                                list_FC.append(y)
                    y_idx += 1
        return count

    
    def get_ID(self):
        return self.ID
    
    def set_status(self):
        if self.status == 10:
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
    
    def find_branch(self,var_strat):
        
        if var_strat == 0:
            best_length = 0
            for d in range(len(self.Domains)):
                leng=len(self.Domains[d])
                if leng > best_length:
                    best_id = d
                    best_length = leng
            mid = int(len(self.Domains[best_id])/2)
            value = (self.Domains[best_id][mid-1] + self.Domains[best_id][mid])/2.            
            return best_id, value
        
        elif var_strat == 1:
            shortest_length = 1000000000 # max(len(self.Domains[d])for d in range(len(self.Domains)))+1
            for d in range(len(self.Domains)):
                leng=len(self.Domains[d])
                if leng < shortest_length and leng >= 2:
                    best_id = d
                    shortest_length = leng         
            return best_id, 0
        
        elif var_strat == 2:
            possible = [d for d in range(len(self.Domains)) if len(self.Domains[d])>=2]
            best_id = possible[rdn.randint(0,len(possible))]
            return best_id, 0
        
        else:
            print ("cette stratégie de branchement n'existe pas")
    
    
    def branch(self,var,value,branching_strat):
        
        if branching_strat == 0:
            ID_left = self.get_ID() +'0'
            ID_right = self.get_ID() +'1'
            D_left = [[j for j in self.Domains[i]] for i in range(len(self.Domains))]
            D_right = [[j for j in self.Domains[i]] for i in range(len(self.Domains))]
            idx = 0
            while D_left[var][idx] <= value:
                idx += 1
            D_left[var] = D_left[var][0:idx]
            D_right[var] = D_right[var][idx::]
            new_nodes=[]
            new_nodes.append(Node(ID_right,D_right))
            new_nodes[0].father_var = var
            new_nodes[0].to_check.append(var)
            new_nodes.append(Node(ID_left,D_left))
            new_nodes[1].father_var = var
            new_nodes[1].to_check.append(var)
            
        elif branching_strat == 1:
            k = 0
            new_nodes = []
            for val in self.Domains[var]:
                ID_branch = self.get_ID() + str(k)
                D_branch = [[j for j in self.Domains[i]] for i in range(len(self.Domains))]
                D_branch[var]=[val]
                new_nodes.append(Node(ID_branch,D_branch))
                new_nodes[k].father_var = var
                new_nodes[k].to_check.append(var)
                k += 1
                
        elif branching_strat == 2:
            
            val=self.Domains[var][-1]
            ID_left = self.get_ID() +'0'
            ID_right = self.get_ID() +'1'
            D_left = [[j for j in self.Domains[i]] for i in range(len(self.Domains))]
            D_right = [[j for j in self.Domains[i]] for i in range(len(self.Domains))]
            D_left[var]=[val]
            D_right[var].pop(-1)
            new_nodes=[]
            new_nodes.append(Node(ID_right,D_right))
            new_nodes[0].father_var = var
            new_nodes[0].to_check.append(var)
            new_nodes.append(Node(ID_left,D_left))
            new_nodes[1].father_var = var
            new_nodes[1].to_check.append(var)
            
            
        else:
            print ("ce style de branchement n'existe pas")
            new_nodes=[]


        return new_nodes