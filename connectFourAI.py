import json
import sys
import random

# We'll be utilizing dumps(dump string) & loads(load string)
# Python enumerates up to n - 1 so we don't need to subtract by 1
def valid_moves(precept):
    grid = precept['grid']
    moves = []  # Can't initialize w/ Int 64s
    for i, col in enumerate(grid):
        if col[0] == 0:
            moves.append(i)
    # This is the same as lines 10 - 12 that constructs an array 
    # With a condition
    #moves = [i for i, col in enumerate(grid) if col[0] == 0]
    return moves

def main():
    print("Connect Four in Python", file=sys.stderr)

    # This next line of code will have an intentional mistake
    for line in sys.stdin:  
        print(line, file=sys.stderr)
        precept = json.loads(line)      # This loads precept as a dict
        moves = valid_moves(precept)    # Returns a list of all valid moves
        move = random.choice(moves) 
        action = {'move': move}
        action_json = json.dumps(action)
        print(action_json, file=sys.stderr)
        print(action_json, flush=True)  # Stdout is default for python 
        

if __name__ == '__main__':
    main()