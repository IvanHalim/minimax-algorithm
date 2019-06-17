EMPTY, BLACK, WHITE, OUTER = '.', '@', 'o', '?'
PIECES = (EMPTY, BLACK, WHITE, OUTER)
PLAYERS = {BLACK: 'Black', WHITE: 'White'}

UP, DOWN, LEFT, RIGHT = -10, 10, -1, 1
UP_RIGHT, DOWN_RIGHT, DOWN_LEFT, UP_LEFT = -9, 11, 9, -11
DIRECTIONS = (UP, UP_RIGHT, RIGHT, DOWN_RIGHT, DOWN, DOWN_LEFT, LEFT, UP_LEFT)

SQUARE_WEIGHTS = [
    0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
    0, 120, -20,  20,   5,   5,  20, -20, 120,   0,
    0, -20, -40,  -5,  -5,  -5,  -5, -40, -20,   0,
    0,  20,  -5,  15,   3,   3,  15,  -5,  20,   0,
    0,   5,  -5,   3,   3,   3,   3,  -5,   5,   0,
    0,   5,  -5,   3,   3,   3,   3,  -5,   5,   0,
    0,  20,  -5,  15,   3,   3,  15,  -5,  20,   0,
    0, -20, -40,  -5,  -5,  -5,  -5, -40, -20,   0,
    0, 120, -20,  20,   5,   5,  20, -20, 120,   0,
    0,   0,   0,   0,   0,   0,   0,   0,   0,   0
]

# Values for endgame boards are big constants
MAX_VALUE = float('inf')
MIN_VALUE = float('-inf')

move_number = 1 # The number of the move to be played

# Load data from file
def load_data(filename):
    with open(filename) as f:
        dataset = [int(x) for x in next(f).split()]
    return dataset

# Array of values for edge positions
edge_table = load_data('edge_table.txt')

# The four edges (with their X-squares)/
edge_and_x_lists = [[22, 11, 12, 13, 14, 15, 16, 17, 18, 27],
                    [72, 81, 82, 83, 84, 85, 86, 87, 88, 77],
                    [22, 11, 21, 31, 41, 51, 61, 71, 81, 72],
                    [27, 18, 28, 38, 48, 58, 68, 78, 88, 77]]

def squares():
    """
    List all the valid squares on the board
    sorted from highest to lowest weight.
    """
    return sorted([i for i in range(11, 89) if 1 <= (i % 10) <= 8], key=lambda sq: SQUARE_WEIGHTS[sq], reverse=True)

def initial_board():
    """Create a new board with the initial black and white positions filled"""
    board = [OUTER] * 100
    for i in squares():
        board[i] = EMPTY
    # The middle four squares should hold the initial piece positions.
    board[44], board[45] = WHITE, BLACK
    board[54], board[55] = BLACK, WHITE
    return board

ply_boards = [initial_board() for _ in range(40)]

class IllegalMoveError(Exception):
    def __init__(self, player, move, board):
        self.player = player
        self.move = move
        self.board = board
        
    def __str__(self):
        return '{0} cannot move to square {1}'.format(PLAYERS[self.player], self.move)

def print_board(board):
    """Get a string representation of the board."""
    rep = ''
    rep += '  {0}\n'.format(' '.join(map(str, range(1, 9))))
    for row in range(1, 9):
        begin, end = 10*row + 1, 10*row + 9
        rep += '{0} {1}\n'.format(row, ' '.join(board[begin:end]))
    return rep

def is_valid(move):
    """Is move a square on the board?"""
    return isinstance(move, int) and move in squares()

def opponent(player):
    """Get player's opponent piece."""
    return BLACK if player is WHITE else WHITE

def find_bracket(square, player, board, direction):
    """
    Find a square that forms a bracket with `square` for `player` in the given
    `direction`. Returns None if no such squares exists.
    """
    bracket = square + direction
    if board[bracket] == player:
        return None
    opp = opponent(player)
    while board[bracket] == opp:
        bracket += direction
    return None if board[bracket] in (OUTER, EMPTY) else bracket

def is_legal(move, player, board):
    """Is this a legal move for the player?"""
    hasbracket = lambda direction: find_bracket(move, player, board, direction)
    return board[move] == EMPTY and any(map(hasbracket, DIRECTIONS))

def make_move(move, player, board):
    """Update the board to reflect the move by the specified player."""
    board[move] = player
    for d in DIRECTIONS:
        make_flips(move, player, board, d)
    return board

def make_flips(move, player, board, direction):
    """Flip pieces in the given direction as a result of the move by player."""
    bracket = find_bracket(move, player, board, direction)
    if not bracket:
        return
    square = move + direction
    while square != bracket:
        board[square] = player
        square += direction
    
def legal_moves(player, board):
    """Get a list of all legal moves for player."""
    return [sq for sq in squares() if is_legal(sq, player, board)]

def any_legal_move(player, board):
    """Can player make any moves?"""
    return any(is_legal(sq, player, board) for sq in squares())

def play(black_strategy, white_strategy):
    """Play a game of Othello and return the final board and score."""
    board = initial_board()
    player = BLACK
    strategy = lambda who: black_strategy if who == BLACK else white_strategy
    move_number = 1
    while player is not None:
        move = get_move(strategy(player), player, board)
        make_move(move, player, board)
        player = next_player(board, player)
        move_number += 1
    return board, score(BLACK, board)

def next_player(board, prev_player):
    """Which player should move next? Returns None if no legal moves exist."""
    opp = opponent(prev_player)
    if any_legal_move(opp, board):
        return opp
    elif any_legal_move(prev_player, board):
        return prev_player
    return None

def get_move(strategy, player, board):
    """Call strategy(player, board) to get a move."""
    copy = board[:] # copy the board to prevent cheating
    move = strategy(player, copy)
    if not is_valid(move) or not is_legal(move, player, board):
        raise IllegalMoveError(player, move, copy)
    return move

def score(player, board):
    """Compute player's score (number of player's pieces minus opponent's)."""
    mine, theirs = 0, 0
    opp = opponent(player)
    for sq in squares():
        piece = board[sq]
        if piece == player:
            mine += 1
        elif piece == opp:
            theirs += 1
    return mine - theirs

def final_value(player, board):
    """The game is over. Find the value of this board to player."""
    diff = score(player, board)
    if diff < 0:
        return MIN_VALUE
    elif diff > 0:
        return MAX_VALUE
    return diff

def alphabeta3(player, board, alpha, beta, depth, evaluate, killer):
    """
    Alphabeta search, putting killer move first.
    """
    if depth == 0:
        return evaluate(player, board), None
    
    def value(board, alpha, beta, killer):
        val, reply = alphabeta3(opponent(player), board, -beta, -alpha, depth-1, evaluate, killer)
        return -val, reply
    
    moves = put_first(killer, legal_moves(player, board))
    if not moves:
        if not any_legal_move(opponent(player), board):
            return final_value(player, board), None
        return value(board, alpha, beta, None)[0], None
    
    best_move = moves[0]
    new_board = ply_boards[depth]
    killer2 = None
    killer2_val = MAX_VALUE
    for move in moves:
        if alpha >= beta:
            # If one of the legal moves leads to a better score than beta, then
            # the opponent will avoid this branch, so we can quit looking.
            break
        val, reply = value(make_move(move, player, replace(new_board, board)), alpha, beta, killer2)
        if val > alpha:
            # If one of the moves leads to a better score than the current best
            # achievable score, then replace it with this one.
            alpha = val
            best_move = move
        if reply is not None and val < killer2_val:
            # If one of the moves leads to a reply that is worse than our worst
            # case scenario killer2, then replace it with this one.
            killer2 = reply
            killer2_val = val
    return alpha, best_move

def put_first(killer, moves):
    """
    Move the killer move to the front of moves,
    if the killer move is in fact a legal move.
    """
    if killer in moves:
        moves.insert(0, moves.pop(moves.index(killer)))
    return moves

def replace(seq1, seq2):
    """Copies one sequence into another"""
    seq1[:] = seq2
    return seq1
    
def alphabeta_searcher3(depth, evaluate):
    """Return a strategy that does Alphabeta search with killer moves"""
    def strategy(player, board):
        return alphabeta3(player, board, MIN_VALUE, MAX_VALUE, depth, evaluate, None)[1]
    return strategy

def adj(square):
    """List all the neighbors of a square."""
    return [square + d for d in DIRECTIONS]

def mobility(player, board):
    """
    Current mobility is the number of legal moves.
    Potential mobility is the number of blank squares
    adjacent to an opponent that are not legal moves.
    Returns current and potential mobility for player.
    """
    opp = opponent(player)
    current, potential = 0, 0
    for sq in squares():
        if board[sq] == EMPTY:
            if sq in legal_moves(player, board):
                current += 1
            elif any(board[neighbor] == opp for neighbor in adj(sq)):
                potential += 1
    return current, (current + potential)

def edge_index(player, board, squares):
    """The index counts 1 for player; 2 for opponent,
    on each square -- summed as a base 3 number."""
    opp = opponent(player)
    index = 0
    for sq in squares:
        index *= 3
        if board[sq] == player:
            index += 1
        elif board[sq] == opp:
            index += 2
    return index

def edge_stability(player, board):
    """Total edge evaluation for player"""
    score = sum(edge_table[edge_index(player, board, edge)] for edge in edge_and_x_lists)
    return score

def Iago_eval(player, board):
    """
    Combine edge stability, current mobility and
    potential mobility to arrive at an evaluation.
    """
    # The three factors are multiplied by coefficients
    # that vary by move number
    c_edg = 312000 + 6240 * move_number
    if move_number < 25:
        c_cur = 50000 + 2000 * move_number
    else:
        c_cur = 75000 + 1000 * move_number
    c_pot = 20000
    
    p_cur, p_pot = mobility(player, board)
    o_cur, o_pot = mobility(opponent(player), board)
    
    score1 = round(c_edg * edge_stability(player, board) / 32000)
    score2 = round(c_cur * (p_cur - o_cur) / (p_cur + o_cur + 2))
    score3 = round(c_pot * (p_pot - o_pot) / (p_pot + o_pot + 2))
    
    score = score1 + score2 + score3
    return score

def Iago(depth):
    """Use an approximation of Iago's evaluation function."""
    return alphabeta_searcher3(depth, Iago_eval)

def user_input(player, board):
    """Get input move from user"""
    print()
    print(print_board(board))
    move = input('{0} to move: '.format(PLAYERS[player]))
    return int(move)

if __name__ == '__main__':
    play(user_input, Iago(3))
