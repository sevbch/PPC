# -*- coding: utf-8 -*-
"""
Created on Sun Mar 17 16:49:43 2019

@author: sev
"""

from Solving import solve, coloring_graph
from time import time
from Graph import create_graph_instance
import pandas as pd
import os


RESULTS_FC_AC_sat={}
RESULTS_FC_AC_sat[0]=("Instance","Solution","Temps","Noeuds","Echecs","Temps BR","Temps AC","Temps FC")
RESULTS_FC_AC={}
RESULTS_FC_AC[0]=("Instance","Solution","Temps","Itérations","Temps par itération","Couleurs par itération","Noeuds par itération")



directory = os.fsencode("./graphes/")
it = 1


for file in os.listdir(directory):
    
    filename = directory+file
    print("fichier numéro : "+str(it))
    print(str(filename))
    
    t1 = time()
    I = create_graph_instance(filename)
    
    t2 = time()
    print("Temps de création : "+str(t2-t1))
    
    time_limit = 120
    
    # --- FC + AC de temps en temps satisfiabilité
    branching_strat = 2
    var_strat = 1
    search_strat = 1
    look_ahead_strat = 3
    dynamic_search=False
    t2 = time()
    sol, nb_col, nbr_nodes,nbr_fails,br_time,ac_time,fc_time = solve(I,branching_strat,var_strat,
                                                                     search_strat,look_ahead_strat,dynamic_search,time_limit)
    t3 = time()
    print("Temps de résolution FC + AC de temps en temps : "+str(t3-t2))
    RESULTS_FC_AC_sat[it]=(file,nb_col,t3-t2,nbr_nodes,nbr_fails,br_time,ac_time,fc_time)
    
    
    time_limit_int = 600 # temps limite pour une résolution lors d'une itération de coloring_graph
    time_limit_tot = 1200 # temps limite total de coloring_graph
    
    # --- FC + AC de temps en temps optimisation
    branching_strat = 2
    var_strat = 1
    search_strat = 1
    look_ahead_strat = 3
    dynamic_search=False
    t2 = time()
    col, time_tot, nbr_it, time_it, col_it, nb_nodes_it = coloring_graph(filename,branching_strat,var_strat,search_strat,
                                                                         look_ahead_strat,dynamic_search,time_limit_int,time_limit_tot)
    t3 = time()
    print("Temps de résolution coloration FC + AC de temps en temps : "+str(t3-t2))
    RESULTS_FC_AC[it]=(file,col,time_tot, nbr_it, time_it, col_it, nb_nodes_it)
    
    
    
    DF_RESULTS_FC_AC_sat = pd.DataFrame()
    DF_RESULTS_FC_AC = pd.DataFrame()
    
    DF_RESULTS_FC_AC_sat = (DF_RESULTS_FC_AC_sat.from_dict(RESULTS_FC_AC_sat)).T
    DF_RESULTS_FC_AC = (DF_RESULTS_FC_AC.from_dict(RESULTS_FC_AC)).T
    
    DF_RESULTS_FC_AC_sat.to_csv("FC_AC_sat.csv")
    DF_RESULTS_FC_AC.to_csv("FC_AC.csv")
    
    it += 1


