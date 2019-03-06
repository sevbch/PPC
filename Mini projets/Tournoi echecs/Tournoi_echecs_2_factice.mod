/*********************************************
 * OPL 12.8.0.0 Model
 * Author: sever
 * Creation Date: 6 mars 2019 at 13:05:29
 *********************************************/

 
 using CP;

float t1;
execute {
	var before = new Date();
	t1 = before.getTime();
	cp.param.TimeLimit = 180;
}

 int N=...;
 tuple match {
 int A;
 int B;  
};
{match} matches = {<a,b> | a in 1..N-1, b in a+1..N};
range players = 1..N;
range days = 1..N-1;
range periods = 1..N div 2;
range planning = 1..((N-1)*(N div 2));

dvar int dm[matches] in days;
dvar int pm[matches] in periods;
dvar int pm2[matches] in 1..(N-1)*(N div 2);
dvar int slot[matches] in planning;

subject to {
	// -------- pas deux matchs le même jour et à la même période ~ alldif
	allDifferent(slot);
	forall(m in matches)
		slot[m] == (pm[m]-1)*(N-1) + dm[m];
//	forall (m1 in matches, m2 in matches : m2.A != m1.A || m2.B != m1.B)
//		 pm[m1] != pm[m2] || dm[m1] != dm[m2];
	
 	// -------- chaque joueur joue une fois par jour
 	forall (d in days, a in players)
 		 count(all(m in matches : (m.A == a || m.B == a)) dm[m], d) == 1;
		 
	// -------- chaque joueur joue deux fois par période (avec un jour factice)
	forall (p in periods, a in players)
		 count(all(m in matches : (m.A == a || m.B == a)) pm[m], p) + count(all(m in matches : (m.A == a || m.B == a)) pm2[m], p) == 2;
}

execute  {
	var after = new Date();
	writeln("------------------------------- "+(N-1)+" jours ------------------------------- ")
	for(var p in periods) {
	write("Période "+p + " : ")	
		for(var d in days) {
			for(var m in matches) {
				if (dm[m] == d && pm[m] == p)
					write(m+" ");
			}
		}
		write("\n");
	}
	writeln("Temps de calcul (s) : ", (after.getTime()-t1)/1000);
}