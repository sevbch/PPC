/*********************************************
 * OPL 12.8.0.0 Model
 * Author: sev
 * Creation Date: 6 mars 2019 at 14:51:03
 *********************************************/

using CP;

float t1;
execute {
	var before = new Date();
	t1 = before.getTime();
	cp.param.TimeLimit = 180;
}


int N=...;
tuple slot {
	int d;
	int p; 
};
range players = 1..N;
range days = 1..N-1;
range periods = 1..N div 2;
{slot} slots = {<d,p> | d in days, p in periods};
range planning = 1..((N*(N-1)) div 2);

dvar int player1[slots] in 1..N-1;
dvar int player2[slots] in 2..N;
dvar int matches[slots] in planning;

subject to {
	// -------- player1 vs player2 = player2 vs player1
	forall(s in slots)
		player1[s] < player2[s];
		
	// -------- on ne joue pas le m�me match deux fois
	allDifferent(matches);
	forall(s in slots)
		matches[s] == N*(player1[s]-1) - ((player1[s]*(player1[s]-1)) div 2) + player2[s] - player1[s];
//	forall(s1 in slots, s2 in slots : s1.d != s2.d || s1.p != s2.p)
//		player1[s1] != player1[s2] || player2[s1] != player2[s2];

	// -------- chaque joueur joue une fois par jour
	forall(day in days, player in players)
		count(all (s in slots : s.d == day) player1[s], player) + count(all (s in slots : s.d == day) player2[s], player) == 1;
	
	// -------- chaque joueur joue au plus deux fois par p�riode
	forall(period in periods, player in players)
		count(all (s in slots : s.p == period) player1[s], player) + count(all (s in slots : s.p == period) player2[s], player) <= 2;
}



execute  {
	var after = new Date();
	writeln("------------------------------- "+(N-1)+" jours ------------------------------- ")
	for(var p in periods) {
	write("P�riode "+p + " : ")	
		for(var d in days) {
			for(var s in slots) {
				if (s.p == p && s.d == d)
					write(player1[s]+","+player2[s]+"   ");
			}
		}
		write("\n");
	}
	writeln("Temps de calcul (s) : ", (after.getTime()-t1)/1000);
}