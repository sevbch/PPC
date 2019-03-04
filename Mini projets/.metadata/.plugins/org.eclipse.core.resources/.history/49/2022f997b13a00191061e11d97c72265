/*********************************************
 * OPL 12.7.1.0 Model
 * Author: Guillaume
 * Creation Date: 22 févr. 2019 at 18:04:01
 *********************************************/

 
 using CP;
 
int N=...;
int T=ftoi(N/2);
range Joueurs=1..N;
range Jours=1..N-1;
range Periodes=1..T;
range Cases=0..(T*(N-1)-1);
 tuple Match {
  int J1;
  int J2;
 };
 
{Match} Matchs = { <J1,J2> | J1 in Joueurs, J2 in 1..J1-1};
 
 
 // Variables de décision
 
 
 dvar int tab[Matchs] in Cases;
 dvar int Factice[Joueurs] in Periodes;
    

 // Contraintes
 
 subject to{ 
 	allDifferent(tab);	
	// Tous les joueurs jouent 1 fois par jour
	
	forall(j in Joueurs){
		forall(jour in Jours){
			sum(m in Matchs : (m.J1==j || m.J2==j)) ftoi(tab[m] div T == (jour-1))==1;		
		}	
	}
	/*
	forall(m1 in Matchs){
		forall(m2 in Matchs){
			if(m1!=m2){		
				m1.J1 == m2.J1 => tab[m1] div T != tab[m2] div T;
				m1.J1 == m2.J2 => tab[m1] div T != tab[m2] div T;
				m1.J2 == m2.J1 => tab[m1] div T != tab[m2] div T;
				m1.J2 == m2.J2 => tab[m1] div T != tab[m2] div T;
			}		
		}
	}	
	*/
	// Tous les joueurs jouent 2 fois au plus par période
	/*
	forall(j in Joueurs){
		forall(m1 in Matchs){
			forall(m2 in Matchs){
				forall(m3 in Matchs){		
					if(m1!=m2 && m2!=m3 && m1!=m3){		
						if(m1.J1 == j || m1.J2==j){
							if(m2.J1 == j || m2.J2==j){
								if(m3.J1 == j || m3.J2==j){
									(tab[m1] % T != tab[m2] % T) ||
									(tab[m2] % T != tab[m3] % T);
       				}}}}									
	  								
				}		
			}
		}
	
	}
	*/
	forall(j in Joueurs){
		forall(p in Periodes){
			sum(m in Matchs : (m.J1==j || m.J2==j)) ftoi((tab[m] % T) == p-1)<=2;		
		}	
	}		
	
	forall(j in Joueurs){
		forall(p in Periodes){
			sum(m in Matchs : (m.J1==j || m.J2==j)) ftoi(tab[m] % T == p-1)==2-ftoi(Factice[j]==p);		
		}	
	}
	
	forall(p in Periodes){
		sum(j in Joueurs) ftoi(Factice[j]==p) == 2;	
	}
	
	
	
}	

execute{
for(var p in Periodes){
	for(var j in Jours){
	 	for(m in Matchs){
	 		 if(tab[m]%T==p-1 && (1+(tab[m])/T>>0)==j){
	 		 	write(m+" ");	 		 
	 		 }
 		}	 	
	}
	writeln();
}
}

/*
main  {

var f = cp.factory;
var phase1 = f.searchPhase( thisOplModel.tab, f.selectSmallest(f.domainSize()), f.selectSmallest(f.value()));  
var phase2 = f.searchPhase( thisOplModel.tab, f.selectLargest(f.domainSize()),  f.selectSmallest(f.value()));
var phase3 = f.searchPhase( thisOplModel.tab, f.selectSmallest(f.varIndex(thisOplModel.tab)),  f.selectSmallest(f.value()));
var phase4 = f.searchPhase( thisOplModel.tab, f.selectLargest(f.varIndex(thisOplModel.tab)),  f.selectSmallest(f.value()));
var phase5 = f.searchPhase( thisOplModel.tab, f.selectSmallest(f.varIndex(thisOplModel.tab)), f.selectRandomValue());
cp.setSearchPhases(phase5); 

thisOplModel.generate();
cp.solve();
for(var p in thisOplModel.Periodes){
	for(var j in thisOplModel.Jours){
	 	for(m in thisOplModel.Matchs){
	 		 if(thisOplModel.tab[m]%thisOplModel.T==p-1 && (1+(thisOplModel.tab[m])/thisOplModel.T>>0)==j){
	 		 	write(m+" ");	 		 
	 		 }
 		}	 	
	}
	writeln();
}
}

*/