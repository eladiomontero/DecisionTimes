Experimental data from the paper:

"Social experiments in the mesoscale: Humans playing a spatial Prisoner's
Dilemma" PLoS ONE (in print)


The experiment had 3 parts conducted in secunce, Exp1, Control and Exp2.
This dhe data form the Control part.


In the experiment, volunteers played a 2x2 PD game with each of their eight neighbors (Moore neighborhood) taking only one action, either to cooperate (C) or to defect (D), the action being the same against all the opponents.

After each round the players were shuffled and assigned a new position on the
network and new 8 neighbours. They are shown the actions and payoffs of the
neigbours of their previous round, not the actions and payoffs of the
neigbour they are playing with at the moment.

The results were stored as series of Cs and Ds, separately for each of 169 users. These result were then compressed using hexadecimal notation. We coded any C as 1 and any D as 0. For instance, if someone played (only 12 rounds) CCDCCDCDDDCD will be, in binary notation, 110110100010 and in hexadecimal DA2.
The number of rounds was 60, a multiple of 4 and thus converted into hexadecimal straight away
(wothout adding any zeros like in the other two parts). 

The other information needed to be stored are the positions of the players.
The position of the players is changing in every round, therefore we store
the positions of the players for every round in the separate files named
userlist_r??. The order of the hexadecimal numbers coresponds to the order
of the players in the round 1, recored in the file userlist_r1. First player
in the file userlist_r1 (usuario166) is in the round 1 on the position (1,1) in the lattice, the second is of the player on the position (1,2), the 14th number is of the player on the position (2,1) etc. 

Therefore, there is a file data_control.txt files with the actions of the players in the
control experiment in the order of round 1, as represented in the file
userlist_r1. Apart from that there 60 files with the positions of players in
each 60 rounds.



