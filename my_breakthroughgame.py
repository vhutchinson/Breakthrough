####################################################################################
#	CSC 412 - Programming Assignment 1
#
#	my_breakthroughgame.py holds main and the BreakthroughGame class. 
#   The Breakthrough class includes board and piece information, as well as the steps to run different games of breakthrough.
#
#	Contributors: Virginia Hutchinson and Ian Phillips
####################################################################################

import pygame
# from pygame.locals import *
import sys, os, math
from minimax_agent import *
from model import *
from alpha_beta_agent import *
import time

class BreakthroughGame:

    def __init__(self):
        """ _init_ initializes all variables for the game, including declaring board dimensions, piece placement, and setting metrics to zero. The game clock is also started."""
        
        pygame.init()
        
        # Set board dimensions for an 8x8 board
        self.width, self.height = 700, 560
        self.sizeofcell = int(560/8)
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.screen.fill([255, 255, 255])
        self.board = 0
        self.blackchess = 0
        self.whitechess = 0
        self.outline = 0
        self.reset = 0
        self.winner = 0

        # Position of pieces, with 0 - empty, 1 - black, 2 - white
        self.boardmatrix = [[1, 1, 1, 1, 1, 1, 1, 1],
                            [1, 1, 1, 1, 1, 1, 1, 1],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [2, 2, 2, 2, 2, 2, 2, 2],
                            [2, 2, 2, 2, 2, 2, 2, 2]]

        # Set status to origin
        # Turn 1: black (starts first), 2: white
        self.status = 0
        self.turn = 1
        # Variables for moving along the x and y planes
        self.ori_x = 0
        self.ori_y = 0
        self.new_x = 0
        self.new_y = 0

        # The metrics below keep track of:
        # Nodes expanded
        self.total_nodes_1 = 0
        self.total_nodes_2 = 0
        # Time for moves
        self.total_time_1 = 0
        self.total_time_2 = 0
        # Steps taken by pieces
        self.total_step_1 = 0
        self.total_step_2 = 0
        # Number of pieces eaten
        self.eat_piece = 0

        # Pygame caption
        pygame.display.set_caption("My Breakthrough Game")

        # Start pygame clock and load graphics
        self.clock = pygame.time.Clock()
        self.initgraphics()

    def run(self):
        """Run the game"""

        # Update game clock and set max number of framerates per second"
        self.clock.tick(90)

        # Clear the screen
        self.screen.fill([255, 255, 255])

        # For each matchup move
        if self.status in  [5,6,7,8,9,10]:
            # Default search type is alpha-beta
            player1search = 2
            player2search = 2

            # Matchup 1: Minimax (Offensive Heuristic 1) vs Alpha-beta (Offensive Heuristic 1)
            if self.status == 5:
                player1search = 1
                player1heur = 1
                player2heur = 1
            # Matchup 2: Alpha-beta (Offensive Heuristic 2) vs Alpha-beta (Defensive Heuristic 1)
            elif self.status == 6:
                player1heur = 3
                player2heur = 2
            # Matchup 3: Alpha-beta (Defensive Heuristic 2) vs Alpha-beta (Offensive Heuristic 1) 
            elif self.status == 7:
                player1heur = 4
                player2heur = 1
            # Matchup 4: Alpha-beta (Offensive Heuristic 2) vs Alpha-beta (Offensive Heuristic 1
            elif self.status == 8:
                player1heur = 3
                player2heur = 1
            # Matchup 5: Alpha-beta (Defensive Heuristic 2) vs Alpha-beta (Defensive Heuristic 1)
            elif self.status == 9:
                player1heur = 4
                player2heur = 2
            # Matchup 6: Alpha-beta (Offensive Heuristic 2) vs Alpha-beta (Defensive Heuristic 2) 
            elif self.status == 10:
                player1heur = 3
                player2heur = 4

            # Black piece
            if self.turn == 1:
                start = time.clock()
                self.ai_move(player1search, player1heur)
                #self.ai_move(2, 1)
                self.total_time_1 += (time.clock() - start)
                self.total_step_1 += 1
                print('Player 1 total steps = ', self.total_step_1,
                        'Player 1 total nodes traversed = ', self.total_nodes_1, "\n",
                        'Player 1 nodes traversed per move = ', self.total_nodes_1 / self.total_step_1,
                        'Player 1 time per step = ', self.total_time_1 / self.total_step_1, "\n",
                        'Player 1 has eaten = ', self.eat_piece)
            # White piece
            elif self.turn == 2:
                start = time.clock()
                self.ai_move(player2search, player2heur)
                #self.ai_move(2, 2)
                self.total_time_2 += (time.clock() - start)
                self.total_step_2 += 1
                print('Player 2 total steps = ', self.total_step_2,
                        'Player 2 total nodes traversed = ', self.total_nodes_2, "\n",
                        'Player 2 nodes traversed per move = ', self.total_nodes_2 / self.total_step_2,
                        'Player 2 time per step = ', self.total_time_2 / self.total_step_2, "\n",
                        'Player 2 has eaten: ', self.eat_piece)

        # Events accepting
        for event in pygame.event.get():
            # Quit if window closed
            if event.type == pygame.QUIT:
                exit()
            # Reset button pressed
            elif event.type == pygame.MOUSEBUTTONDOWN and self.isreset(event.pos):  
                # Reset board and reinitialize status and turn
                self.boardmatrix = [[1, 1, 1, 1, 1, 1, 1, 1],
                            [1, 1, 1, 1, 1, 1, 1, 1],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [2, 2, 2, 2, 2, 2, 2, 2],
                            [2, 2, 2, 2, 2, 2, 2, 2]]
                self.turn = 1
                self.status = 0

			# Status is one of the six matchup types:
            elif event.type == pygame.MOUSEBUTTONDOWN and self.ismatchup(1, event.pos):
                self.status = 5
            elif event.type == pygame.MOUSEBUTTONDOWN and self.ismatchup(2, event.pos):
                self.status = 6
            elif event.type == pygame.MOUSEBUTTONDOWN and self.ismatchup(3, event.pos):
                self.status = 7
            elif event.type == pygame.MOUSEBUTTONDOWN and self.ismatchup(4, event.pos):
                self.status = 8
            elif event.type == pygame.MOUSEBUTTONDOWN and self.ismatchup(5, event.pos):
                self.status = 9
            elif event.type == pygame.MOUSEBUTTONDOWN and self.ismatchup(6, event.pos):
                self.status = 10

        # Display the board and pieces
        self.display()
        # Update the screen
        pygame.display.flip()

    # Load the graphics and rescale them
    def initgraphics(self):
        self.board = pygame.image.load_extended(os.path.join('src', 'chessboard.jpg'))
        self.board = pygame.transform.scale(self.board, (560, 560))
        self.blackchess = pygame.image.load_extended(os.path.join('src', 'blackchess.png'))
        self.blackchess = pygame.transform.scale(self.blackchess, (self.sizeofcell- 20, self.sizeofcell - 20))
        self.whitechess = pygame.image.load_extended(os.path.join('src', 'whitechess.png'))
        self.whitechess = pygame.transform.scale(self.whitechess, (self.sizeofcell - 20, self.sizeofcell - 20))
        self.outline = pygame.image.load_extended(os.path.join('src', 'square-outline.png'))
        self.outline = pygame.transform.scale(self.outline, (self.sizeofcell, self.sizeofcell))
        self.reset = pygame.image.load_extended(os.path.join('src', 'reset.jpg'))
        self.reset = pygame.transform.scale(self.reset, (80, 80))
        self.winner = pygame.image.load_extended(os.path.join('src', 'winner.png'))
        self.winner = pygame.transform.scale(self.winner, (250, 250))
        self.matchup1 = pygame.image.load_extended(os.path.join('src', 'matchup1.png'))
        self.matchup1 = pygame.transform.scale(self.matchup1, (90, 70))
        self.matchup2 = pygame.image.load_extended(os.path.join('src', 'matchup2.png'))
        self.matchup2 = pygame.transform.scale(self.matchup2, (90, 70))
        self.matchup3 = pygame.image.load_extended(os.path.join('src', 'matchup3.png'))
        self.matchup3 = pygame.transform.scale(self.matchup3, (90, 70))
        self.matchup4 = pygame.image.load_extended(os.path.join('src', 'matchup4.png'))
        self.matchup4 = pygame.transform.scale(self.matchup4, (90, 70))
        self.matchup5 = pygame.image.load_extended(os.path.join('src', 'matchup5.png'))
        self.matchup5 = pygame.transform.scale(self.matchup5, (90, 70))
        self.matchup6 = pygame.image.load_extended(os.path.join('src', 'matchup6.png'))
        self.matchup6 = pygame.transform.scale(self.matchup6, (90, 70))

    # Display the graphics in the window
    def display(self):
        self.screen.blit(self.board, (0, 0))
        self.screen.blit(self.reset, (590, 20))
        self.screen.blit(self.matchup1, (587, 100))
        self.screen.blit(self.matchup2, (587, 175))
        self.screen.blit(self.matchup3, (587, 250))
        self.screen.blit(self.matchup4, (587, 325))
        self.screen.blit(self.matchup5, (587, 400))
        self.screen.blit(self.matchup6, (587, 475))

        # Place black and white pieces based off of board matrix locations
        for i in range(8):
            for j in range(8):
                if self.boardmatrix[i][j] == 1:
                    self.screen.blit(self.blackchess, (self.sizeofcell * j + 10, self.sizeofcell * i + 10))
                elif self.boardmatrix[i][j] == 2:
                    self.screen.blit(self.whitechess, (self.sizeofcell * j + 10, self.sizeofcell * i + 10))

        # Action status: Ready to move
        if self.status == 1:
            # Player 1 moves downward
            if self.boardmatrix[self.ori_x][self.ori_y] == 1:
                # Three possible moves:
                x1 = self.ori_x + 1
                y1 = self.ori_y - 1
                x2 = self.ori_x + 1
                y2 = self.ori_y + 1
                x3 = self.ori_x + 1
                y3 = self.ori_y
                # Down and left
                if y1 >= 0 and self.boardmatrix[x1][y1] != 1:
                    self.screen.blit(self.outline,
                                     (self.sizeofcell * y1, self.sizeofcell * x1))
                # Down and right
                if y2 <= 7 and self.boardmatrix[x2][y2] != 1:
                    self.screen.blit(self.outline,
                                     (self.sizeofcell * y2, self.sizeofcell * x2))
                # Straight down
                if x3 <= 7 and self.boardmatrix[x3][y3] == 0:
                    self.screen.blit(self.outline,
                                     (self.sizeofcell * y3, self.sizeofcell * x3))

            # Player 2 moves upward
            if self.boardmatrix[self.ori_x][self.ori_y] == 2:
                # Three possible moves:
                x1 = self.ori_x - 1
                y1 = self.ori_y - 1
                x2 = self.ori_x - 1
                y2 = self.ori_y + 1
                x3 = self.ori_x - 1
                y3 = self.ori_y
                # Up and left
                if y1 >= 0 and self.boardmatrix[x1][y1] != 2:
                    self.screen.blit(self.outline,
                                     (self.sizeofcell * y1, self.sizeofcell * x1))
                # Up and right
                if y2 <= 7 and self.boardmatrix[x2][y2] != 2:
                    self.screen.blit(self.outline,
                                     (self.sizeofcell * y2, self.sizeofcell * x2))
                # Straight up
                if x3 >= 0 and self.boardmatrix[x3][y3] == 0:
                    self.screen.blit(self.outline,
                                     (self.sizeofcell * y3, self.sizeofcell * x3))

        # Action status: Game won
        if self.status == 3:
            # Display win picture and text announcing winning player
            self.screen.blit(self.winner, (100, 100))

            font = pygame.font.Font('freesansbold.ttf', 32)

            if self.turn == 1:
                color = "White"
            elif self.turn == 2:
                color = "Black"
            content = color + " player wins!"
            text = font.render(content, True, (0, 0, 0), (255, 255, 255)) 
            textRect = text.get_rect() 
            textRect.center = (self.width // 3, self.height // 2)
            self.screen.blit(text, textRect)

    # Reset button pixel range
    def isreset(self, pos):
        x, y = pos
        if 670 >= x >= 590 and 20 <= y <= 100:
            return True
        return False

    # Matchup buttons pixel range (dynamic)
    def ismatchup(self, matchup, pos):
        x, y = pos
        if 587 <= x <= 677 and (100 + ((matchup - 1) * 70)) <= y <= (175 + ((matchup - 1) * 70)):
            return True
        return False

    # Move based on input search type and heuristic function
    def ai_move(self, searchtype, evaluation):
        if searchtype == 1:
            return self.ai_move_minimax(evaluation)
        elif searchtype == 2:
            return self.ai_move_alphabeta(evaluation)

    # Calls the minimax agent using a search depth of 3
    def ai_move_minimax(self, function_type):
        board, nodes, piece = MinimaxAgent(self.boardmatrix, self.turn, 3, function_type).minimax_decision()
        self.boardmatrix = board.getMatrix()
        if self.turn == 1:
            self.total_nodes_1 += nodes
            self.turn = 2
        elif self.turn == 2:
            self.total_nodes_2 += nodes
            self.turn = 1
        self.eat_piece = 16 - piece
        if self.isgoalstate():
            self.status = 3

    # Calls the alpha-beta agent using a search depth of 4
    def ai_move_alphabeta(self, function_type):
        board, nodes, piece = AlphaBetaAgent(self.boardmatrix, self.turn, 4, function_type).alpha_beta_decision()
        self.boardmatrix = board.getMatrix()
        if self.turn == 1:
            self.total_nodes_1 += nodes
            self.turn = 2
        elif self.turn == 2:
            self.total_nodes_2 += nodes
            self.turn = 1
        self.eat_piece = 16 - piece
        if self.isgoalstate():
            self.status = 3

    # Evaluates to True or False depending on if a player has made it to the opposite side of the board
    def isgoalstate(self, base=0):
        if base == 0:
            if 2 in self.boardmatrix[0] or 1 in self.boardmatrix[7]:
                return True
            else:
                for line in self.boardmatrix:
                    if 1 in line or 2 in line:
                        return False
            return True
        else:
            count = 0
            for i in self.boardmatrix[0]:
                if i == 2:
                    count += 1
            if count == 3:
                return True
            count = 0
            for i in self.boardmatrix[7]:
                if i == 1:
                    count += 1
            if count == 3:
                return True
            count1 = 0
            count2 = 0
            for line in self.boardmatrix:
                for i in line:
                    if i == 1:
                        count1 += 1
                    elif i == 2:
                        count2 += 1
            if count1 <= 2 or count2 <= 2:
                return True
        return False

def main():
    game = BreakthroughGame()
    while 1:
        game.run()
    while 0:
        print("La Fin")

if __name__ == '__main__': 
    main()

