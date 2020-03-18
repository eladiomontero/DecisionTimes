Experimental data from the paper:

"Social experiments in the mesoscale: Humans playing a spatial Prisoner's
Dilemma" PLoS ONE (in print)

In the experiment, volunteers played a 2x2 PD game with each of their eight neighbors (Moore neighborhood) taking only one action, either to cooperate (C) or to defect (D), the action being the same against all the opponents.

Two experiment were conducted and the results were stored as series of Cs and Ds, separately for each of 169 users. These result were then compressed using hexadecimal notation. We coded any C as 1 and any D as 0. For instance, if someone played (only 12 rounds) CCDCCDCDDDCD will be, in binary notation, 110110100010 and in hexadecimal DA2. As the number of rounds are 47 and 58, therefore we added 1 and 2 zeros respectively at the end of the binary number, so as to make the number of binary digits a multiple of 4 and thus converted into hexadecimal straight away. 

The other information needed to be stored are the positions of the players. This we stored as a position in the list. First hexadecimal number are the actions of the player on the player o position (1,1) in the lattice, the second is of the n the position (1,2), the 14th number is of the player on the position (2,1) etc.

Therefore, there are two files data_exp1.txt and data_exp2.txt with the actions of the players in the first experiment and second experiment respectively. Each contains the list of hexadecimal numbers with each number being the actions of the players and the positions in the list representing the position in the lattice. 



