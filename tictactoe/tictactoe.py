"""
Tic Tac Toe Player
"""
from copy import deepcopy
import math

X = "X"
O = 'O'
EMPTY = None


def initial_state():
    """
    Returns starting board of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    total_items = len([item for sublist  in board for item in sublist if item != None])
    if total_items % 2 == 0: 
        return 'X'
    elif total_items % 2 == 1: 
        return 'O'


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    
    return set((i,j) for i, sublist in enumerate(board) for j, item in enumerate(sublist) if item == None)


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    player_move = player(board)

    new_board = deepcopy(board)
    
    i,j = action

    if board[i][j] != None:
        raise Exception
    else:
        new_board[i][j] = player_move

    return new_board




def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    for y in range(3): 
        ## crossess win 
        if board[y] == ['X','X','X']: 
            return 'X' 
        if board[0][y] == 'X' and board[1][y] == 'X' and board[2][y] == 'X' :
            return 'X'
        if board[0][0] == 'X' and board[1][1] == 'X' and board[2][2] == 'X': 
            return 'X'
        if board[0][2] == 'X' and board[1][1] == 'X' and board[2][0] == 'X': 
            return 'X'
        ## noughts win 
        if board[y] == ['O','O','O']: 
            return 'O'
        if board[0][y] == 'O' and board[1][y] == 'O' and board[2][y] == 'O' :
            return 'O'
        if board[0][0] == 'O' and board[1][1] == 'O' and board[2][2] == 'O': 
            return 'O'
        if board[0][2] == 'O' and board[1][1] == 'O' and board[2][0] == 'O': 
            return 'O'
    ## draws 
    if len(actions(board)) == 0:
        return 'draw'

    else: 
        return None 
 


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    # game is won by one of the players
    if winner(board) != None:
        return True

    # moves still possible
    for row in board:
        if EMPTY in row:
            return False

    # no possible moves
    return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == 'X':
        return 1
    if winner(board) == 'O': 
        return -1 
    if winner(board) == 'draw': 
        return 0

def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """

    def max_value(board): 
        if terminal(board) == True: 
            return utility(board), None 
        else: 
            best = {'score': -1e3, 'move': None}
            for action in actions(board): 
                board_trans = result(board,action)
                v = min_value(board_trans)[0]
                if v >= best['score']: 
                    best['score'] = v 
                    best['move'] = action 
            return best['score'], best['move']

    def min_value(board): 
        if terminal(board) == True: 
            return utility(board), None 
        else: 
            best = {'score': 1e3, 'move': None}
            for action in actions(board): 
                board_trans = result(board,action)
                v = max_value(board_trans)[0]
                if v <= best['score']: 
                    best['score'] = v 
                    best['move'] = action 
            return best['score'], best['move']

    opt_player = player(board)

    if player == 'X': 
        return max_value(board)[1]
    else: 
        return min_value(board)[1]








    






            




    







