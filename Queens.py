# -*- coding: utf-8 -*-
"""
Created on Sat Feb 09 16:51:15 2019

@author: Guillaume
"""

from Instance import Instance

def create_queens_instance(n,breakS=False):
    var_domains = [list(range(1,n+1)) for i in range(n)]
    constraints_list = []
    if breakS:
        if n%2==0:
            m=n/2
        else:
            m=(n+1)/2
        var_domains[0]=list(range(1,m+1))
    for x in range(n):
        for y in range(x):
            tuple_list = []
            for x_value in var_domains[x]:
                for y_value in var_domains[y]:
                    if x_value != y_value and x_value - y_value != x - y and y_value - x_value != x - y:
                        tuple_list.append((x_value,y_value))
            constraints_list.append((x,y,tuple_list))
    I = Instance(n,var_domains,constraints_list)
    return I