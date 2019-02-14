# -*- coding: utf-8 -*-
"""
Created on Sat Feb 09 16:51:15 2019

@author: Guillaume
"""

from Instance import Instance

def create_Reines_instance(n):
    var_domains = [list(range(n)) for i in range(n)]
    constraints_list = []
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