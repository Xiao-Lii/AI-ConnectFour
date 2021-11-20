import json
import sys
import random
import math
import numpy as np

PLAYER = 2
AI = 1
EMPTY = 0
AI_PIECE = 1
PLAYER_PIECE = 2
WINDOW_LENGTH = 4

def get_board(game_dict):
    grid = game_dict['grid']        # Save the 'grid' key from our dict read from the json obj
    return grid

def get_next_open_row(board, col, height):
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
def valid_moves(game_dict):
    grid = game_dict['grid']        # Save the 'grid' key from our dict read from the json obj
    moves = []  # Can't initialize w/ Int 64s

    for i, col in enumerate(grid):
        if col[0] == 0:
            moves.append(i)
    # This is the same as lines 10 - 12 that constructs an array w/ a condition
    #moves = [i for i, col in enumerate(grid) if col[0] == 0]

    return moves

def get_valid_locations(board):
	valid_locations = []
	for col in range(COLUMN_COUNT):
		if is_valid_location(board, col):
			valid_locations.append(col)
	return valid_locations

def evaluate_window(window, piece):
	score = 0
	opp_piece = PLAYER_PIECE
	if piece == PLAYER_PIECE:
		opp_piece = AI_PIECE

	if window.count(piece) == 4:
		score += 100
	elif window.count(piece) == 3 and window.count(EMPTY) == 1:
		score += 5
	elif window.count(piece) == 2 and window.count(EMPTY) == 2:
		score += 2

	if window.count(opp_piece) == 3 and window.count(EMPTY) == 1:
		score -= 4

	return score

def score_position(board, piece, col, height):
	score = 0

	## Score center column
	center_array = [int(i) for i in list(board[:, col//2])]
	center_count = center_array.count(piece)
	score += center_count * 3

	## Score Horizontal
	for r in range(height):
		row_array = [int(i) for i in list(board[r,:])]
		for c in range(col-3):
			window = row_array[c:c+WINDOW_LENGTH]
			score += evaluate_window(window, piece)

	## Score Vertical
	for c in range(col):
		col_array = [int(i) for i in list(board[:,c])]
		for r in range(height-3):
			window = col_array[r:r+WINDOW_LENGTH]
			score += evaluate_window(window, piece)

	## Score posiive sloped diagonal
	for r in range(height-3):
		for c in range(col-3):
			window = [board[r+i][c+i] for i in range(WINDOW_LENGTH)]
			score += evaluate_window(window, piece)

	for r in range(height-3):
		for c in range(col-3):
			window = [board[r+3-i][c+i] for i in range(WINDOW_LENGTH)]
			score += evaluate_window(window, piece)

	return score

def minimax(grid, depth, alpha, beta, maximizingPlayer):
	valid_locations = get_valid_locations(grid)
	is_terminal = is_terminal_node(grid)
	if depth == 0 or is_terminal:
		if is_terminal:
			if winning_move(grid, AI_PIECE):
				return (None, 100000000000000)
			elif winning_move(grid, PLAYER_PIECE):
				return (None, -10000000000000)
			else: # Game is over, no more valid moves
				return (None, 0)
		else: # Depth is zero
			return (None, score_position(grid, AI_PIECE))
	if maximizingPlayer:
		value = -math.inf
		column = random.choice(valid_locations)
		for col in valid_locations:
			row = get_next_open_row(grid, col)
			b_copy = grid.copy()
			new_score = minimax(b_copy, depth-1, alpha, beta, False)[1]
			if new_score > value:
				value = new_score
				column = col
			alpha = max(alpha, value)
			if alpha >= beta:
				break
		return column, value
    
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


def main():
    print("Connect Four in Python", file=sys.stderr)
    alpha = -math.inf
    beta = math.inf

    # This next line of code will have an intentional mistake
    for line in sys.stdin:  
        print(line, file=sys.stderr)
        game_dict = json.loads(line)        # This loads the game as a dict: grid, height, player #, width
        grid = get_board(game_dict)
        # col = get_width(game_dict)
        height = get_depth(game_dict)
        moves = valid_moves(game_dict)      # Returns a list of all valid moves

        # We'll utilize mini-max & alpha-beta pruning to choose the next best move
        # Player 1(AI) will be seeking a max value vs Player 2 - min value
        move = random.choice(moves) # Let's ignore this random move generator
        

        #row = get_next_open_row(grid, col, height)
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