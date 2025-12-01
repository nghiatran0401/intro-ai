"""
Tic Tac Toe Player
"""

import math

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    x_count = sum(row.count(X) for row in board)
    o_count = sum(row.count(O) for row in board)
    return X if x_count == o_count else O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    empty_cells = set()
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                empty_cells.add((i, j))
    return empty_cells


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    i, j = action
    if board[i][j] is not EMPTY:
        raise ValueError("Invalid action: cell is not empty.")
    new_board = [row.copy() for row in board]
    new_board[i][j] = player(board)
    return new_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # Check rows and columns
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] and board[i][0] is not None:
            return board[i][0]
        if board[0][i] == board[1][i] == board[2][i] and board[0][i] is not None:
            return board[0][i]
    # Check diagonals
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] is not None:
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] is not None:
        return board[0][2]
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    return winner(board) is not None or all(cell is not EMPTY for row in board for cell in row)


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    win = winner(board)
    if win == X:
        return 1
    elif win == O:
        return -1
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None

    current = player(board)

    def max_value(state, alpha, beta):
        if terminal(state):
            return utility(state), None
        v = -math.inf
        best_action = None
        for action in actions(state):
            min_v, _ = min_value(result(state, action), alpha, beta)
            if min_v > v:
                v = min_v
                best_action = action
            alpha = max(alpha, v)
            if beta <= alpha:
                break  # Beta cut-off
        return v, best_action

    def min_value(state, alpha, beta):
        if terminal(state):
            return utility(state), None
        v = math.inf
        best_action = None
        for action in actions(state):
            max_v, _ = max_value(result(state, action), alpha, beta)
            if max_v < v:
                v = max_v
                best_action = action
            beta = min(beta, v)
            if beta <= alpha:
                break  # Alpha cut-off
        return v, best_action

    if current == X:
        _, action = max_value(board, -math.inf, math.inf)
    else:
        _, action = min_value(board, -math.inf, math.inf)
    return action
