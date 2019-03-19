# -*- coding: utf-8 -*-
"""
Created on Tue Feb 19 22:17:55 2019

@author: sev
"""

from Instance import Instance
import io
import networkx as nx
from networkx.algorithms.approximation import max_clique



class Graph:
    def __init__(self,n,deg_max,edges):
        self.n = n
        self.deg_max = deg_max
        self.edges = edges



def get_graph(filename):
    edges = [] # liste des arêtes
    deg_max = 0 # degré max du graphe --> deg_max + 1 = borne sup du nombre chromatique
    with io.open(filename,'r') as f:
        for line in f:
            ch = line[0]
            if ch == 'c': # ligne de commentaire
                continue;
            elif ch == 'e' or ch == 'p':
                l = []
                for s in line.split(' '):
                    l.append(s)
                if ch == 'p':
                    n = int(l[2])
                    deg = [0 for i in range(n)]
                else:
                    u = int(l[1])-1
                    v = int(l[2][:-1])-1
                    if v < u:
                        v = int(l[1])-1
                        u = int(l[2][:-1])-1
                    if u < v:
                        edges.append((u,v))
                        deg[u] += 1
                        deg[v] += 1
                        if deg[u] > deg_max:
                            deg_max = deg[u]
                        elif deg[v] > deg_max:
                            deg_max = deg[v]
            else: # ligne vide = fin du fichier
                break
    f.closed
    edges2=list(set(edges))
    if len(edges2)!=len(edges):
        deg_max = int(deg_max/2)
#    print("Il y a "+str(len(edges2))+" arêtes dans le graphe")
    g = Graph(n,deg_max,edges)
    return g



def create_graph_instance(filename, colours=None):
    g = get_graph(filename)
    n = g.n
    if colours==None:
        max_col=g.deg_max+1
        var_domains = [list(reversed(range(1, int(g.deg_max + 2)))) for i in range(g.n)]
#        print("Tentative de coloration avec au plus "+str(g.deg_max+1)+" couleurs \n")
    else:
        max_col=colours
#        print("Tentative de coloration avec au plus "+str(max_col)+" couleurs \n")
        var_domains = [list(reversed(range(1, colours + 1))) for i in range(g.n)]
    constraints_list = []
    CL=find_max_clique(g.edges)
    col=1
    for p in CL:
        var_domains[p]=[col]
        col+=1
    print("Clique max détectée avec "+str(col-1)+" couleurs")
    if colours!=None and colours < col-1:
        return []
    Uni = [[] for i in range(n)]
    # Uni[x] est la liste des variables dont les contraintes touchent x
    Cons_ID = [[-1 for i in range(j)] for j in range(n)]
    # Cons_ID[x][y] renvoie l'ID de la contrainte C(x,y), et -1 sinon. On impose TOUJOURS x_ID>y_ID
    Cons_Tuple = []
    # Cons_Tuple[ID][val1][val2] renvoie True si la contrainte ID accepte le tuple (val1,val2)
    for e in g.edges:
        x = e[1]
        y = e[0]
        Cons_Tuple.append([[False for d in range(int(max_col+1))] for z in range(int(max_col+1))])
        Uni[x].append(y)
        Uni[y].append(x)
        count=0
        for x_value in var_domains[x]:
            for y_value in var_domains[y]:
                if x_value != y_value:
                    Cons_Tuple[-1][x_value][y_value] = True
                    count+=1
        Cons_ID[x][y] = len(Cons_Tuple)-1
        if count==len(var_domains[x])*len(var_domains[y]):
            Uni[x].pop()
            Uni[y].pop()
            Cons_Tuple.pop()
            Cons_ID[x][y]=-1
    I = Instance(g.n,var_domains,constraints_list,col-1,Uni,Cons_ID,Cons_Tuple)
    return I

def find_max_clique(edges):
    G=nx.from_edgelist(edges)
    L=max_clique(G)
    return L