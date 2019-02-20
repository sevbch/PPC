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

}; 

main {
   var model = thisOplModel;
   model.generate();
   var f = model.max_freq-1;
   var data = model.dataElements;
   var count=0;
   while(cp.solve()){
   	   if(count==0){   	   
   	  	   write("Solution allocation " + "["); 
	       for (var i in model.alloc) write(model.alloc[i]+  ",");
	       writeln("]");  }
   	   else{
	       write("Solution allocation " + "["); 
	       for (var i in updatedmodel.alloc) write(updatedmodel.alloc[i]+  ",");
       	   writeln("]");}   
	   data.max_freq = f;
	   var def = model.modelDefinition;
	   var updatedmodel = new IloOplModel(def,cp);
	   updatedmodel.addDataSource(data);
	   updatedmodel.generate();
	   var f = updatedmodel.max_freq-1;
	   var data = updatedmodel.dataElements;
	   count+=1;
}	
   
}


 