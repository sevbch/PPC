# -*- coding: utf-8 -*-
"""
Created on Wed Mar 06 16:57:38 2019

@author: Guillaume
"""

from Instance import Instance
from Solving import solve, print_sol
from Queens import create_queens_instance
from time import time
from Graph import create_graph_instance
from Node import Node
from copy import deepcopy as dcopy
import pandas as pd


RESULTS_LA1={}
RESULTS_LA2={}
RESULTS_LA1_Alea={}
RESULTS_DC={}
RESULTS_LA1[0]=("Temps","Noeuds","Echecs","Temps BR","Temps AC","Temps FC")
RESULTS_LA2[0]=("Temps","Noeuds","Echecs","Temps BR","Temps AC","Temps FC")
RESULTS_LA1_Alea[0]=("Temps","Noeuds","Echecs","Temps BR","Temps AC","Temps FC")
RESULTS_DC[0]=("Temps","Noeuds","Echecs","Temps BR","Temps AC","Temps FC")

for n in range(6,10):
    
    branching_strat = 2
    var_strat = 1
    search_strat = 1
    look_ahead_strat = 1
    dynamic_search=False
    t1 = time()
    
    I_Q = create_queens_instance(n)
    I_Q.compute_useful_objects()
    
    t2 = time()
    print("Temps de création : "+str(t2-t1))
    sol, nb_col, nbr_nodes,nbr_fails,br_time,ac_time,fc_time = solve(I_Q,branching_strat,var_strat,search_strat,look_ahead_strat,dynamic_search)
    t3 = time()
    print("Temps de résolution : "+str(t3-t2))
    RESULTS_LA1[n]=(t3-t2,nbr_nodes,nbr_fails,br_time,ac_time,fc_time)
    
    branching_strat = 2
    var_strat = 1
    search_strat = 1
    look_ahead_strat = 2
    dynamic_search=False
    t2 = time()
    sol, nb_col, nbr_nodes,nbr_fails,br_time,ac_time,fc_time = solve(I_Q,branching_strat,var_strat,search_strat,look_ahead_strat,dynamic_search)
    t3 = time()
    print("Temps de résolution : "+str(t3-t2))
    RESULTS_LA2[n]=(t3-t2,nbr_nodes,nbr_fails,br_time,ac_time,fc_time)
    
    branching_strat = 1
    var_strat = 2
    search_strat = 2
    look_ahead_strat = 1
    dynamic_search=True
    t2 = time()
    sol, nb_col, nbr_nodes,nbr_fails,br_time,ac_time,fc_time = solve(I_Q,branching_strat,var_strat,search_strat,look_ahead_strat,dynamic_search)
    t3 = time()
    print("Temps de résolution : "+str(t3-t2))
    RESULTS_LA1_Alea[n]=(t3-t2,nbr_nodes,nbr_fails,br_time,ac_time,fc_time)
    
    DF_LA1 = pd.DataFrame()
    DF_LA2 = pd.DataFrame()
    DF_LA1_Alea = pd.DataFrame()
    DF_DC = pd.DataFrame()
    DF_LA1 = (DF_LA1.from_dict(RESULTS_LA1)).T
    DF_LA2 = (DF_LA2.from_dict(RESULTS_LA2)).T
    DF_LA1_Alea = (DF_LA1_Alea.from_dict(RESULTS_LA1_Alea)).T
    DF_DC = (DF_DC.from_dict(RESULTS_DC)).T
    DF_LA1.to_csv("LA1.csv")
    DF_LA2.to_csv("LA2.csv")
    DF_LA1_Alea.to_csv("LA1_Alea.csv")
    DF_DC.to_csv("DC.csv")
    print(n)