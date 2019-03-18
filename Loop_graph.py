# -*- coding: utf-8 -*-
"""
Created on Tue Mar 12 20:06:55 2019

@author: sev
"""

from Solving import solve, coloring_graph
from time import time
from Graph import create_graph_instance
import pandas as pd
import os




# --------------------------------------- UNIQUEMENT PROBLEME DE SATISFIABILITE ---------------------------------------
#RESULTS_CREATION={}
#RESULTS_CREATION[0]=("Instance","Temps creation","Nb var","Nb contraintes","Max clique (lb)","ub")
#RESULTS_FC={}
#RESULTS_FC[0]=("Instance","Solution","Temps","Noeuds","Echecs","Temps BR","Temps AC","Temps FC")
RESULTS_FC_AC_sat={}
RESULTS_FC_AC_sat[0]=("Instance","Solution","Temps","Noeuds","Echecs","Temps BR","Temps AC","Temps FC")
#RESULTS_FC_AC_alea={}
#RESULTS_FC_AC_alea[0]=("Instance","Solution","Temps","Noeuds","Echecs","Temps BR","Temps AC","Temps FC")
#RESULTS_DS={}
#RESULTS_DS[0]=("Instance","Solution","Temps","Noeuds","Echecs","Temps BR","Temps AC","Temps FC")
RESULTS_FC_alea={}
RESULTS_FC_alea[0]=("Instance","Solution","Temps","Noeuds","Echecs","Temps BR","Temps AC","Temps FC")


time_limit = 120
directory = os.fsencode("./graphes/")
it = 1


for file in os.listdir(directory):
    
    filename = directory+file
    print(str(filename))
    print("fichier numéro : "+str(it))
    
    t1 = time()
    I = create_graph_instance(filename)
    
    t2 = time()
    print("Temps de création : "+str(t2-t1))
#    RESULTS_CREATION[it] = (file,t2-t1,I.N, I.M, I.lb, I.d_max)
    
#    # --- uniquement FC
#    branching_strat = 2
#    var_strat = 1
#    search_strat = 1
#    look_ahead_strat = 1
#    dynamic_search = False
#    sol, nb_col, nbr_nodes,nbr_fails,br_time,ac_time,fc_time = solve(I,branching_strat,var_strat,
#                                                                     search_strat,look_ahead_strat,dynamic_search,time_limit)
#    t3 = time()
#    print("Temps de résolution FC : "+str(t3-t2))
#    RESULTS_FC[it]=(file,nb_col,t3-t2,nbr_nodes,nbr_fails,br_time,ac_time,fc_time)
    
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
    print("Temps de résolution FC + AC de temps en temps : "+str(t3-t2))
    RESULTS_FC_AC_sat[it]=(file,nb_col,t3-t2,nbr_nodes,nbr_fails,br_time,ac_time,fc_time)
    
    # --- FC + AC avec aléa
#    branching_strat = 1
#    var_strat = 2
#    search_strat = 2
#    look_ahead_strat = 3
#    dynamic_search=False
#    t2 = time()
#    sol, nb_col, nbr_nodes,nbr_fails,br_time,ac_time,fc_time = solve(I,branching_strat,var_strat,
#                                                                     search_strat,look_ahead_strat,dynamic_search,time_limit)
#    t3 = time()
#    print("Temps de résolution FC + AC avec aléa : "+str(t3-t2))
#    RESULTS_FC_AC_alea[it]=(file,nb_col,t3-t2,nbr_nodes,nbr_fails,br_time,ac_time,fc_time)
    
     # --- dynamic search
#    dynamic_search=True
#    t2 = time()
#    sol, nb_col, nbr_nodes,nbr_fails,br_time,ac_time,fc_time = solve(I,branching_strat,var_strat,
#                                                                     search_strat,look_ahead_strat,dynamic_search,time_limit)
#    t3 = time()
#    print("Temps de résolution dynamic search : "+str(t3-t2))
#    RESULTS_DS[it]=(file,nb_col,t3-t2,nbr_nodes,nbr_fails,br_time,ac_time,fc_time)
    
    # --- FC avec aléa
    branching_strat = 1
    var_strat = 1
    search_strat = 2
    look_ahead_strat = 1
    dynamic_search=False
    t2 = time()
    sol, nb_col, nbr_nodes,nbr_fails,br_time,ac_time,fc_time = solve(I,branching_strat,var_strat,
                                                                     search_strat,look_ahead_strat,dynamic_search,time_limit)
    t3 = time()
    print("Temps de résolution FC avec aléa : "+str(t3-t2))
    RESULTS_FC_alea[it]=(file,nb_col,t3-t2,nbr_nodes,nbr_fails,br_time,ac_time,fc_time)
    
    
#    DF_RESULTS_CREATION = pd.DataFrame()
#    DF_RESULTS_FC = pd.DataFrame()
    DF_RESULTS_FC_AC_sat = pd.DataFrame()
#    DF_RESULTS_FC_AC_alea = pd.DataFrame()
#    DF_RESULTS_DS = pd.DataFrame()
    DF_RESULTS_FC_alea = pd.DataFrame()
    
#    DF_RESULTS_CREATION = (DF_RESULTS_CREATION.from_dict(RESULTS_CREATION)).T
#    DF_RESULTS_FC = (DF_RESULTS_FC.from_dict(RESULTS_FC)).T
    DF_RESULTS_FC_AC_sat = (DF_RESULTS_FC_AC_sat.from_dict(RESULTS_FC_AC_sat)).T
#    DF_RESULTS_FC_AC_alea = (DF_RESULTS_FC_AC_alea.from_dict(RESULTS_FC_AC_alea)).T
#    DF_RESULTS_DS = (DF_RESULTS_DS.from_dict(RESULTS_DS)).T
    DF_RESULTS_FC_alea = (DF_RESULTS_FC_alea.from_dict(RESULTS_FC_alea)).T
    
#    DF_RESULTS_CREATION.to_csv("CREATION.csv")
#    DF_RESULTS_FC.to_csv("FC.csv")
    DF_RESULTS_FC_AC_sat.to_csv("FC_AC_sat.csv")
#    DF_RESULTS_FC_AC_alea.to_csv("FC_AC_alea.csv")
#    DF_RESULTS_DS.to_csv("DS.csv")
    DF_RESULTS_FC_alea.to_csv("FC_alea.csv")
    
    it += 1

# --------------------------------------- PROBLEME D'OPTIMISATION ---------------------------------------


#RESULTS_FC={}
#RESULTS_FC[0]=("Instance","Solution","Temps","Itérations","Temps par itération","Couleurs par itération","Noeuds par itération")
RESULTS_FC_AC={}
RESULTS_FC_AC[0]=("Instance","Solution","Temps","Itérations","Temps par itération","Couleurs par itération","Noeuds par itération")
#RESULTS_DS={}
#RESULTS_DS[0]=("Instance","Solution","Temps","Itérations","Temps par itération","Couleurs par itération","Noeuds par itération")

#col, time()-t_ini, it, time_it, col_it

time_limit_int = 600 # temps limite pour une résolution lors d'une itération de coloring_graph
time_limit_tot = 1200 # temps limite total de coloring_graph
directory = os.fsencode("./graphes/")
it = 1


for file in os.listdir(directory):
    
    filename = directory+file
    print(str(filename))
    print("fichier numéro : "+str(it))
    
    
    # --- uniquement FC
#    branching_strat = 2
#    var_strat = 1
#    search_strat = 1
#    look_ahead_strat = 1
#    dynamic_search = False
#    t2 = time()
#    col, time_tot, nbr_it, time_it, col_it, nb_nodes_it = coloring_graph(filename,branching_strat,var_strat,search_strat,look_ahead_strat,
#                                                       dynamic_search,time_limit_int,time_limit_tot)
#    t3 = time()
#    print("Temps de résolution FC : "+str(t3-t2))
#    RESULTS_FC[it]=(file, col,time_tot, nbr_it, time_it, col_it)
    
    # --- FC + AC de temps en temps
    branching_strat = 2
    var_strat = 1
    search_strat = 1
    look_ahead_strat = 3
    dynamic_search=False
    t2 = time()
    col, time_tot, nbr_it, time_it, col_it, nb_nodes_it = coloring_graph(filename,branching_strat,var_strat,search_strat,look_ahead_strat,
                                                       dynamic_search,time_limit_int,time_limit_tot)
    t3 = time()
    print("Temps de résolution FC + AC de temps en temps : "+str(t3-t2))
    RESULTS_FC_AC[it]=(file,col,time_tot, nbr_it, time_it, col_it)
    
    # --- dynamic search
#    dynamic_search=True
#    t2 = time()
#    col, time_tot, nbr_it, time_it, col_it, nb_nodes_it = coloring_graph(filename,branching_strat,var_strat,search_strat,look_ahead_strat,
#                                                       dynamic_search,time_limit_int,time_limit_tot)
#    t3 = time()
#    print("Temps de résolution dynamic search : "+str(t3-t2))
#    RESULTS_DS[it]=(file,col,time_tot, nbr_it, time_it, col_it)
    
#    DF_RESULTS_FC = pd.DataFrame()
    DF_RESULTS_FC_AC = pd.DataFrame()
#    DF_RESULTS_DS = pd.DataFrame()
    
#    DF_RESULTS_FC = (DF_RESULTS_FC.from_dict(RESULTS_FC)).T
    DF_RESULTS_FC_AC = (DF_RESULTS_FC_AC.from_dict(RESULTS_FC_AC)).T
#    DF_RESULTS_DS = (DF_RESULTS_DS.from_dict(RESULTS_DS)).T
    
#    DF_RESULTS_FC.to_csv("FC.csv")
    DF_RESULTS_FC_AC.to_csv("FC_AC.csv")
#    DF_RESULTS_DS.to_csv("DS.csv")
    
    it += 1
