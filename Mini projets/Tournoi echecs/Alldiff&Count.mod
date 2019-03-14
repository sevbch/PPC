/*********************************************
 * OPL 12.7.1.0 Model
 * Author: Guillaume
 * Creation Date: 6 mars 2019 at 18:03:52
 *********************************************/

 using CP;
 
 int N=...;
 int T=ftoi(N/2);
 range Joueurs=1..N;
 range Jours=1..N-1;
 range Periodes=1..T;
 range Cases=1..T*(N-1);
 
 dvar int tabJ[Jours,Periodes,1..2] in Joueurs;
 dvar int IDMatch[Jours,Periodes] in Cases;
 
 subject to{ 
  	//j1<j2
	forall(p in Periodes, k in Jours){
			tabJ[k,p,1]<tabJ[k,p,2];
	}
	
	/*
	*/
	
 	// Tous les matchs sont joués
	allDifferent(IDMatch);
	forall(p in Periodes, k in Jours){
		IDMatch[k,p] == (tabJ[k,p,1]-1)*(N-tabJ[k,p,1]/2) + tabJ[k,p,2] - tabJ[k,p,1];	
	}
 	
 	
 	
 	//1 match/jour
	forall(k in Jours){
		allDifferent(all(p in Periodes, b in 1..2)tabJ[k,p,b]); 		
	}
 	
 	//2 matchs/periode
 	forall(j in Joueurs){
 		forall(p in Periodes){
 			count(all(k in Jours,b in 1..2)tabJ[k,p,b],j) <=2; 		
 		}
 	}
 	
 }
 
 execute{
 for(p in Periodes){
 	for(k in Jours){ 		
 		write(tabJ[k][p][1]);
 		write(" ");
 		write(tabJ[k][p][2]);
 		write("      "); 	
 	}
 	writeln(); 
 } 
 }
 