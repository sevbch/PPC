# -*- coding: utf-8 -*-
"""
Created on Tue Mar 12 20:06:55 2019

@author: sev
"""

from Solving import solve
from time import time
from Graph import create_graph_instance
import pandas as pd
import os
from main import coloring_graph



RESULTS_FC={}
RESULTS_FC[0]=("Temps","Noeuds","Echecs","Temps BR","Temps AC","Temps FC")
RESULTS_FC_AC={}
RESULTS_FC_AC[0]=("Temps","Noeuds","Echecs","Temps BR","Temps AC","Temps FC")
RESULTS_FC_AC_alea={}
RESULTS_FC_AC_alea[0]=("Temps","Noeuds","Echecs","Temps BR","Temps AC","Temps FC")
RESULTS_DS={}
RESULTS_DS[0]=("Temps","Noeuds","Echecs","Temps BR","Temps AC","Temps FC")
RESULTS_FC_alea={}
RESULTS_FC_alea[0]=("Temps","Noeuds","Echecs","Temps BR","Temps AC","Temps FC")


# --------------------------------------- UNIQUEMENT PROBLEME DE SATISFIABILITE ---------------------------------------
time_limit = 120
directory = os.fsencode("./graphes/")
it = 1

for file in os.listdir(directory):
    
    filename = directory+file
    print(str(filename))
    
    t1 = time()
    I = create_graph_instance(filename)
    I.compute_useful_objects()
    
    t2 = time()
    print("Temps de création : "+str(t2-t1))
    
    # --- uniquement FC
    branching_strat = 2
    var_strat = 1
    search_strat = 1
    look_ahead_strat = 1
    dynamic_search = False
    sol, nb_col, nbr_nodes,nbr_fails,br_time,ac_time,fc_time = solve(I,branching_strat,var_strat,
                                                                     search_strat,look_ahead_strat,dynamic_search,time_limit)
    t3 = time()
    print("Temps de résolution : "+str(t3-t2))
    RESULTS_FC[it]=(t3-t2,nbr_nodes,nbr_fails,br_time,ac_time,fc_time)
    
    # --- FC + AC de temps en temps
    branching_strat = 2
    var_strat = 1
    search_strat = 1
    look_ahead_strat = 3
    dynamic_search=False
    t2 = time()
    sol, nb_col, nbr_nodes,nbr_fails,br_time,ac_time,fc_time = solve(I,branching_strat,var_strat,
                                                                     search_strat,look_ahead_strat,dynamic_search,time_limit)
    t3 = time()
    print("Temps de résolution : "+str(t3-t2))
    RESULTS_FC_AC[it]=(t3-t2,nbr_nodes,nbr_fails,br_time,ac_time,fc_time)
    
    # --- FC + AC avec aléa
    branching_strat = 1
    var_strat = 2
    search_strat = 2
    look_ahead_strat = 3
    dynamic_search=False
    t2 = time()
    sol, nb_col, nbr_nodes,nbr_fails,br_time,ac_time,fc_time = solve(I,branching_strat,var_strat,
                                                                     search_strat,look_ahead_strat,dynamic_search,time_limit)
    t3 = time()
    print("Temps de résolution : "+str(t3-t2))
    RESULTS_FC_AC_alea[it]=(t3-t2,nbr_nodes,nbr_fails,br_time,ac_time,fc_time)
    
    # --- dynamic search
    dynamic_search=True
    t2 = time()
    sol, nb_col, nbr_nodes,nbr_fails,br_time,ac_time,fc_time = solve(I,branching_strat,var_strat,
                                                                     search_strat,look_ahead_strat,dynamic_search,time_limit)
    t3 = time()
    print("Temps de résolution : "+str(t3-t2))
    RESULTS_FC_AC_alea[it]=(t3-t2,nbr_nodes,nbr_fails,br_time,ac_time,fc_time)
    
    # --- FC avec aléa
    branching_strat = 1
    var_strat = 2
    search_strat = 2
    look_ahead_strat = 1
    dynamic_search=False
    t2 = time()
    sol, nb_col, nbr_nodes,nbr_fails,br_time,ac_time,fc_time = solve(I,branching_strat,var_strat,
                                                                     search_strat,look_ahead_strat,dynamic_search,time_limit)
    t3 = time()
    print("Temps de résolution : "+str(t3-t2))
    RESULTS_FC_alea[it]=(t3-t2,nbr_nodes,nbr_fails,br_time,ac_time,fc_time)
    
    
    
    DF_RESULTS_FC = pd.DataFrame()
    DF_RESULTS_FC_AC = pd.DataFrame()
    DF_RESULTS_FC_AC_alea = pd.DataFrame()
    DF_RESULTS_DS = pd.DataFrame()
    DF_RESULTS_FC_alea = pd.DataFrame()
    
    DF_RESULTS_FC = (DF_RESULTS_FC.from_dict(RESULTS_FC)).T
    DF_RESULTS_FC_AC = (DF_RESULTS_FC_AC.from_dict(RESULTS_FC_AC)).T
    DF_RESULTS_FC_AC_alea = (DF_RESULTS_FC_AC_alea.from_dict(RESULTS_FC_AC_alea)).T
    DF_RESULTS_DS = (DF_RESULTS_DS.from_dict(RESULTS_DS)).T
    DF_RESULTS_FC_alea = (DF_RESULTS_FC_alea.from_dict(RESULTS_FC_alea)).T
    
    DF_RESULTS_FC.to_csv("FC.csv")
    DF_RESULTS_FC_AC.to_csv("FC_AC.csv")
    DF_RESULTS_FC_AC_alea.to_csv("FC_AC_alea.csv")
    DF_RESULTS_DS.to_csv("DS.csv")
    DF_RESULTS_FC_alea.to_csv("FC_alea.csv")
    
    it += 1
    

# --------------------------------------- PROBLEME D'OPTIMISATION ---------------------------------------
# TO DO
# en fonction des résultats sur la satisfiabilité, utiliser seulement les meilleures méthodes

