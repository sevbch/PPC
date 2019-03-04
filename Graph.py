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
    g = Graph(n,deg_max,edges)
    return g



def create_graph_instance(filename, colours=None):
    g = get_graph(filename)
    if colours==None:
        var_domains = [list(reversed(range(1, g.deg_max + 2))) for i in range(g.n)]
        print("Tentative de coloration avec au plus "+str(g.deg_max+1)+" couleurs \n")
    else:
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
    for e in g.edges:
        tuple_list = []
        x = e[1]
        y = e[0]
        for x_value in var_domains[x]:
            for y_value in var_domains[y]:
                if x_value != y_value:
                    tuple_list.append((x_value,y_value))
        constraints_list.append((x,y,tuple_list))
    I = Instance(g.n,var_domains,constraints_list,col-1)
    return I

def find_max_clique(edges):
    G=nx.from_edgelist(edges)
    L=max_clique(G)
    return L