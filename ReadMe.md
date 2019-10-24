# Breakthrough

The goal of this assignment is to implement an agent to play a simple 2-player zero-sum game called Breakthrough.

## Breakdown

This version of the strategy game will consider matchups between different agents depending on search type and heuristics function.
The matchups used will be:

1. Minimax (Offensive Heuristic 1) vs Alpha-beta (Offensive Heuristic 1) 
2. Alpha-beta (Offensive Heuristic 2) vs Alpha-beta (Defensive Heuristic 1) 
3. Alpha-beta (Defensive Heuristic 2) vs Alpha-beta (Offensive Heuristic 1) 
4. Alpha-beta (Offensive Heuristic 2) vs Alpha-beta (Offensive Heuristic 1) 
5. Alpha-beta (Defensive Heuristic 2) vs Alpha-beta (Defensive Heuristic 1) 
6. Alpha-beta (Offensive Heuristic 2) vs Alpha-beta (Defensive Heuristic 2) 

The Minimax search will use a depth of 3, and the Alpha-beta search will use a depth of 4.

## Heuristic Functions

The following functions were used:

<br>Offensive Heuristic 1: def offensive_function(self, turn): 2*(30-self.enemyscore(turn))+random.random()/10
<br>Defensive Heuristic 1: def defensive_function(self, turn): 2*self.myscore(turn)+random.random()/10
<br>Offensive Heuristic 2: def offensive_function_2(self, turn): 1 * self.myscore(turn) - 2 * self.enemyscore(turn)
<br>Defensive Heuristic 2: def defensive_function_2(self, turn): 2 * self.myscore(turn) - 1 * self.enemyscore(turn)

