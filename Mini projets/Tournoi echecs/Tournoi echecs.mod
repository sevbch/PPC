/*********************************************
 * OPL 12.7.1.0 Model
 * Author: Guillaume
 * Creation Date: 22 févr. 2019 at 18:04:01
 *********************************************/

 
 using CP;
 
float t1;
execute {
	var before = new Date();
	t1 = before.getTime();
	cp.param.TimeLimit = 180;
}
 
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

	// Tous les joueurs jouent 2 fois par période
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
	var after = new Date();
	writeln("Temps de calcul (s) : ", (after.getTime()-t1)/1000);
	for(var p in Periodes){
		for(var j in Jours){
		 	for(var m in Matchs){
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
var phase1 = f.searchPhase( thisOplModel.Factice, f.selectSmallest(f.domainSize()), f.selectSmallest(f.value()));  
var phase2 = f.searchPhase( thisOplModel.tab, f.selectLargest(f.domainSize()),  f.selectSmallest(f.value()));
var phase3 = f.searchPhase( thisOplModel.tab, f.selectSmallest(f.varIndex(thisOplModel.tab)),  f.selectSmallest(f.value()));
var phase4 = f.searchPhase( thisOplModel.tab, f.selectLargest(f.varIndex(thisOplModel.tab)),  f.selectSmallest(f.value()));
var phase5 = f.searchPhase( thisOplModel.tab, f.selectSmallest(f.varIndex(thisOplModel.tab)), f.selectRandomValue());
cp.setSearchPhases(phase1); 

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

