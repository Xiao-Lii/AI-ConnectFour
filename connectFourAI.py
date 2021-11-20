import json
import sys
import random
import math

# We'll be utilizing dumps(dump string) & loads(load string)
# Python enumerates up to n - 1 so we don't need to subtract by 1
def valid_moves(game_dict):
    grid = game_dict['grid']        # Save the 'grid' key from our dict read from the json obj
    moves = []  # Can't initialize w/ Int 64s

    # If top of column is empyy, add to valid moves list 
    moves = [i for i, col in enumerate(grid) if col[0] == 0]
    return moves


def minimax(depth, nodeIndex, values, alpha, beta, maximizingPlayer):
    # Our terminating condition
    if depth == 3:
        return values[nodeIndex]

    if maximizingPlayer:
        value = -math.inf
        # Recurrsion for Comparing Alpa Leaf Nodes in Mini Max Algorithm
        for i in range(0, 2):
            test_value = minimax(depth + 1, nodeIndex * 2 + i, values, alpha, beta, False)
            value = max(value, test_value)
            alpha = max(alpha, value)

            # Alpha Beta Pruning - If Beta < Alpha, skip evaluation
            if beta <= alpha:
                break
        return value    # Return Large Alpha Value for these nodes
        
    else: # This will trigger for the Minimizing Player 
        value = math.inf
        # Recurrsion for Comparing Beta Leaf Nodes in Mini Max Algorithm - Saving Lowest Value
        for i in range(0, 2):
            test_value2 = minimax(depth + 1, nodeIndex * 2 + i, values, alpha, beta, True)
            value = min(value, test_value2)
            beta = min(beta, value)

            # Alpha Beta Pruning - If Alpa > Beta, skip evaluations
            if beta <= alpha:
                break
        return value    # Return Smallest Beta Value for these nodes
    


def main():
    print("Connect Four in Python", file=sys.stderr)

    for line in sys.stdin:  
        print(line, file=sys.stderr)
        game_dict = json.loads(line)        # This loads the game as a dict: grid, height, player #, width
        moves = valid_moves(game_dict)      # Returns a list of all valid moves

        # We'll utilize mini-max & alpha-beta pruning to choose the next best move
        # Player 1(AI) will be seeking a max value vs Player 2 - min value
        move = random.randint(minimax(1, 0, moves, math.inf, -math.inf, True), 5)
        action = {'move': move}

        action_json = json.dumps(action)    # Dump action dict into a json formatted str
        print(action_json, file=sys.stderr) # Write json str to file
        print(action_json, flush=True)      # Now flush the buffer


if __name__ == '__main__':
    main()