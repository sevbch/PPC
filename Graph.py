# -*- coding: utf-8 -*-
"""
Created on Tue Feb 19 22:17:55 2019

@author: sev
"""

from Instance import Instance
import io



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
                    if u > v:
                        edges.append((u,v))
                        deg[u] += 1
                        deg[v] += 1
                        if deg[u] > deg_max:
                            deg_max = deg[u]
                        elif deg[v] > deg_max:
                            deg_max = deg[v]
            else: # ligne vide = fin du fichier
                break;
    f.closed
    g = Graph(n,deg_max,edges)
    return g



def create_graph_instance(filename):
    g = get_graph(filename)
    var_domains = [list(reversed(range(1, g.deg_max + 2))) for i in range(g.n)]
    constraints_list = []
    for e in g.edges:
        tuple_list = []
        x = e[0]
        y = e[1]
        for x_value in var_domains[x]:
            for y_value in var_domains[y]:
                if x_value != y_value:
                    tuple_list.append((x_value,y_value))
        constraints_list.append((x,y,tuple_list))
    I = Instance(g.n,var_domains,constraints_list)
    return I
