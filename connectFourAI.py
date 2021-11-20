from _typeshed import NoneType
import json
import sys
import random
import math
from typing import get_args
import numpy as np


def get_board(game_dict):
    grid = game_dict['grid']        # Save the 'grid' key from our dict read from the json obj
    return grid


def find_next_row(board, col, height):
	for row in range(height):
		if board[row][col] == 0:
			return row


def get_depth(game_dict):
    depth = game_dict['height']
    return depth


def get_width(game_dict):
    width = game_dict['width']
    return width    


def get_player(game_dict):
    player = game_dict['player']    
    return player


# We'll be utilizing dumps(dump string) & loads(load string)
# Python enumerates up to n - 1 so we don't need to subtract by 1
def valid_col(game_dict):
    grid = game_dict['grid']        # Save the 'grid' key from our dict read from the json obj
    moves = []  # Can't initialize w/ Int 64s

    for i, col in enumerate(grid):
        if col[0] == 0:
            moves.append(i)
    # This is the same as lines 10 - 12 that constructs an array w/ a condition
    #moves = [i for i, col in enumerate(grid) if col[0] == 0]
    return moves


def valid_opts(grid):
    moves = [i for i, col in enumerate(grid) if col[0] == 0]
    return moves


def minimax(grid, depth, alpha, beta, maximizingPlayer):
	valid_locations = valid_opts(grid)
        
	if maximizingPlayer:
		maxValue = -math.inf
		column = random.choice(valid_locations)
		for col in valid_locations:
			row = find_next_row(grid, col)
			grid_copy = grid.copy()
			new_score = minimax(grid_copy, depth-1, alpha, beta, 1)[1]
			if new_score > maxValue:
				maxValue = new_score
				column = col
			alpha = max(alpha, maxValue)
			if beta <= alpha:
				break
		return column

# def minimax(position, depth, alpha, beta, maximizingPlayer):
#     if depth == 0 or game over in position:
#         return static evalutation of position

#     if maximizingPlayer:
#         maxEval = -math.inf
#         for each child of position:
#             eval = minimax(child, depth - 1, alpha, beta, False)
#             maxEval = max(maxEval, eval)
#             alpha = max(alpha, eval)
#             if beta <= alpha:
#                 break;
#             return maxEval
#     else:
#         minEval = math.inf
#         for each child of position:
#             eval = minimax(child, depth - 1, alpha, beta, True)
#             minEval = min(minEval, eval)
#             beta = min(beta, eval)
#             if beta <= alpha:
#                 break;
#             return minEval

def create_board(game_dict):
	board = np.zeros((game_dict['height'],game_dict['width']))
    
	return board

def main():
    print("Connect Four in Python", file=sys.stderr)

    # This next line of code will have an intentional mistake
    for line in sys.stdin:  
        print(line, file=sys.stderr)
        game_dict = json.loads(line)        # This loads the game as a dict: grid, height, player #, width
        grid = get_board(game_dict)
        height = get_depth(game_dict)
        width = get_width(game_dict)

        # board = create_board(game_dict)
        # print(board, file=sys.stderr)

        moves = valid_col(game_dict)      # Returns a list of all valid moves
        test_moves = valid_opts(grid)
        print(moves, file=sys.stderr)
        print(test_moves, file=sys.stderr)
        # col = minimax(grid, height, -math.inf, math.inf, 1)
        # print(col, file=sys.stderr)

        # col = test_minimax(game_dict, moves, -math.inf, math.inf)

        # We'll utilize mini-max & alpha-beta pruning to choose the next best move
        # Player 1(AI) will be seeking a max value vs Player 2 - min value
        # col = minimax(grid, width, height, -math.inf, math.inf, 1)

        # if valid_moves(grid, col, width):
        #     row = find_next_row(grid, col, height)

        # action = {'move': col}

        move = random.choice(moves) # Let's ignore this random move generator
        action = {'move': move}

        action_json = json.dumps(action)
        print(action_json, file=sys.stderr)
        print(action_json, flush=True)  # Stdout is default for python 

        """
        if turn == AI and not game_over:				
            col, minimax_score = minimax(board, 5, -math.inf, math.inf, True)

            if is_valid_location(board, col):
                #pygame.time.wait(500)
                row = get_next_open_row(board, col)
                drop_piece(board, row, col, AI_PIECE)
        """

if __name__ == '__main__':
    main()