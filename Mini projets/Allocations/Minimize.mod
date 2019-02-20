/*********************************************
 * OPL 12.7.1.0 Model
 * Author: Guillaume
 * Creation Date: 15 févr. 2019 at 11:32:47
 *********************************************/

 /*********************************************
 * OPL 12.7.1.0 Model
 * Author: Guillaume
 * Creation Date: 15 févr. 2019 at 09:33:07
 *********************************************/

 using CP;
 
int max_freq=...;
 range F=1..max_freq;
int t_max=...;
range T=1..t_max;
 tuple Offsets {
  int t1;
  int t2;
  int value;
 }
 
 {Offsets} offsets=...;
 
 // Variables de décision
 
 
 dvar int alloc[T] in F;
 dvar int f in F;
    
 minimize f;
    
 // Contraintes
 constraints {
   
   // Parité
   forall (t in T) {
   if(t%2==0)   { alloc[t]%2==0;}
   else{alloc[t]%2==1;}
   	}  
   	
   	
	// Offsets
   	forall (offset in offsets)  {
		abs(alloc[offset.t1]-alloc[offset.t2])>=offset.value;
 	} 
 	
 	// Max freq
 	
 	forall(t in T){
 	alloc[t]<=f; 	
 	}

}; 