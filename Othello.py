import os
import random

# The outside edge is marked ?, empty squares are ., black is @, and white is o.
# The black and white pieces represent the two players.
EMPTY, BLACK, WHITE, OUTER = '.', '@', 'o', '?'
PIECES = (EMPTY, BLACK, WHITE, OUTER)
PLAYERS = {BLACK: 'Black', WHITE: 'White'}

# To refer to neighbor squares we can add a direction to a square.
UP, DOWN, LEFT, RIGHT = -10, 10, -1, 1
UP_RIGHT, DOWN_RIGHT, DOWN_LEFT, UP_LEFT = -9, 11, 9, -11
DIRECTIONS = (UP, UP_RIGHT, RIGHT, DOWN_RIGHT, DOWN, DOWN_LEFT, LEFT, UP_LEFT)

# A list of square weights to be used for move ordering
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

# The number of the move to be played
move_number = 1

# Array of values for edge positions
edge_table = [0 for _ in range(3**10)]

# The four edges (with their X-squares)
edge_and_x_lists = [[22, 11, 12, 13, 14, 15, 16, 17, 18, 27],
                    [72, 81, 82, 83, 84, 85, 86, 87, 88, 77],
                    [22, 11, 21, 31, 41, 51, 61, 71, 81, 72],
                    [27, 18, 28, 38, 48, 58, 68, 78, 88, 77]]

# The top edge is the first edge in the edge_and_x_lists
top_edge = edge_and_x_lists[0]

# Corner and X-squares
corner_xsqs = [(11, 22), (18, 27), (81, 72), (88, 77)]

#                     stab  semi  un
static_edge_table = [[None, 0, -2000],  # X
                     [700, None, None], # corner
                     [1200, 200, -25],  # C
                     [1000, 200, 75],   # A
                     [1000, 200, 50],   # B
                     [1000, 200, 50],   # B
                     [1000, 200, 75],   # A
                     [1200, 200, -25],  # C
                     [700, None, None], # corner
                     [None, 0, -2000]]  # X

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

# A vector of boards to be used and reused
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
    global move_number
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
    # When depth is zero, don't examine possible moves. Just determine the value
    # of this board to the player.
    if depth == 0:
        return evaluate(player, board), None
    
    def value(board, alpha, beta, killer):
        # The value of a board is the opposite of its value to the opponent.
        val, reply = alphabeta3(opponent(player), board, -beta, -alpha, depth-1, evaluate, killer)
        return -val, reply
    
    # We want to evaluate all the legal moves by considering their implications
    # `depth` turns in advance. First, find all the legal moves, putting the
    # killer move in front of the list.
    moves = put_first(killer, legal_moves(player, board))

    # If player has no legal moves, then either:
    if not moves:
        # the game is over, so the best achievable score is victory or defeat
        if not any_legal_move(opponent(player), board):
            return final_value(player, board), None
        # or we have to pass this turn, so just find the value of this board.
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
    """
    The index counts 1 for player; 2 for opponent,
    on each square -- summed as a base 3 number.
    """
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

def init_edge_table():
    """Initialize `edge_table`, starting from the empty board."""
    # Initialize the static values
    for n_pieces in range(11):
        def fn1(board, index):
            edge_table[index] = static_edge_stability(BLACK, board)
        map_edge_n_pieces(fn1, BLACK, initial_board(), n_pieces, top_edge, 0)
    # Now iterate five times trying to improve
    for _ in range(5):
        for n_pieces in range(9, 0, -1):
            def fn2(board, index):
                edge_table[index] = possible_edge_moves_value(BLACK, board, index)
            map_edge_n_pieces(fn2, BLACK, initial_board(), n_pieces, top_edge, 0)

def map_edge_n_pieces(fn, player, board, n, squares, index):
    """
    Call fn on all edges with n pieces.
    Index counts 1 for player, 2 for opponent
    """
    if len(squares) < n:
        return
    elif not squares:
        fn(board, index)
    else:
        index3 = index * 3
        sq = squares[0]
        map_edge_n_pieces(fn, player, board, n, squares[1:], index3)
        if n > 0 and board[sq] == EMPTY:
            board[sq] = player
            map_edge_n_pieces(fn, player, board, n-1, squares[1:], index3+1)
            board[sq] = opponent(player)
            map_edge_n_pieces(fn, player, board, n-1, squares[1:], index3+2)
            board[sq] = EMPTY

def possible_edge_moves_value(player, board, index):
    """
    Consider all possible edge moves.
    Combine their values into a single number.
    """
    x = [(1.0, edge_table[index])]
    y = [possible_edge_move(player, board, sq) for sq in top_edge if board[sq] == EMPTY]
    possibilities = x + y
    return combine_edge_moves(possibilities, player)

def possible_edge_move(player, board, sq):
    """Return a (prob, val) pair for a possible edge move."""
    num_player = 1 if player == BLACK else 2
    new_board = replace(ply_boards[num_player], board)
    make_move(sq, player, new_board)
    prob = edge_move_probability(player, board, sq)
    val = -edge_table[edge_index(opponent(player), new_board, top_edge)]
    return (prob, val)

def combine_edge_moves(possibilities, player):
    """Combine the best moves."""
    prob = 1.0
    val = 0.0
    fn = True if player == BLACK else False
    for pair in sorted(possibilities, key=lambda x: x[1], reverse=fn):
        if prob < 0.0:
            break
        val += prob * pair[0] * pair[1]
        prob -= prob * pair[0]
    return round(val)

def corner_p(sq):
    """Return the tuple which contains the corner square"""
    return next((x for x in corner_xsqs if x[0] == sq), None)

def x_square_p(sq):
    """Return the tuple which contains the x-square"""
    return next((x for x in corner_xsqs if x[1] == sq), None)

def x_square_for(corner):
    """Return the x-square for a corner square"""
    tuple = [x for x in corner_xsqs if x[0] == corner]
    return tuple[0][1] if tuple else None

def corner_for(xsq):
    """Return the corner square for an x-square"""
    tuple = [x for x in corner_xsqs if x[1] == xsq]
    return tuple[0][0] if tuple else None

def edge_move_probability(player, board, square):
    """What's the probability that player can move to this square?"""
    # X-squares
    if x_square_p(square):
        return 0.5
    # Immediate capture
    elif is_legal(square, player, board):
        return 1.0
    # Move to corner depends on X-square
    elif corner_p(square):
        x_square = x_square_for(square)
        if board[x_square] == EMPTY:
            return 0.1
        elif board[x_square] == player:
            return 0.001
        else:
            return 0.9
    else:
        val = [[.1, .4, .7],
               [.05, .3, None],
               [.01, None, None]]
        x = count_edge_neighbors(player, board, square)
        y = count_edge_neighbors(opponent(player), board, square)
        if is_legal(square, opponent(player), board):
            return val[x][y]/2
        else:
            return val[x][y]
        
def count_edge_neighbors(player, board, square):
    """Count the neighbors of this square occupied by player."""
    inc = [1, -1]
    neighbors = [board[square+i] for i in inc]
    return sum(1 for x in neighbors if x == player)

def static_edge_stability(player, board):
    """Compute this edge's static stability."""
    score = 0
    for i in range(len(top_edge)):
        sq = top_edge[i]
        if board[sq] == EMPTY:
            score += 0
        elif board[sq] == player:
            score += static_edge_table[i][piece_stability(board, sq)]
        else:
            score -= static_edge_table[i][piece_stability(board, sq)]
    return score

def piece_stability(board, sq):
    """Evaluate whether a square is stable, unstable or semi-stable"""
    stable, semi_stable, unstable = 0, 1, 2
    if corner_p(sq):
        return stable
    elif x_square_p(sq):
        if board[corner_for(sq)] == EMPTY:
            return unstable
        else:
            return semi_stable
    else:
        player = board[sq]
        opp = opponent(player)
        p1 = next(p for p in board[sq:20] if p != player)
        p2 = next(p for p in board[sq-1:9:-1] if p != player)
        
        # Unstable pieces can be captured immediately
        # by playing in the empty square
        if (p1 == EMPTY and p2 == opp) or (p2 == EMPTY and p1 == opp):
            return unstable
        
        # Semi-stable pieces might be captured
        elif p1 == opp and p2 == opp and next((p for p in board[11:19] if p == EMPTY), None):
            return semi_stable
        elif p1 == EMPTY and p2 == EMPTY:
            return semi_stable
        
        # Stable pieces can never be captured
        else:
            return stable

def save_data(filename, data):
    """Save data into a file."""
    with open(filename, 'w') as f:
        f.write(' '.join(str(x) for x in data))

def load_data(filename):
    """Load data from file."""
    with open(filename) as f:
        dataset = [int(x) for x in next(f).split()]
    return dataset

def create_edge_table():
    """
    Create edge_table.txt if it doesn't exist.
    Otherwise load data from edge_table.txt.
    """
    if not os.path.exists('edge_table.txt'):
        print('Creating \'edge_table.txt\'...')
        init_edge_table()
        save_data('edge_table.txt', edge_table)
        print('\'edge_table.txt\' created')
    else:
        edge_table[:] = load_data('edge_table.txt')
        print('\'edge_table.txt\' loaded')

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
    valid_input = [str(x) for x in legal_moves(player, board)]
    move = ''
    while move not in valid_input:
        move = input('{0} to move: '.format(PLAYERS[player]))
    return int(move)

def win_message():
    message = ['Well done!',
               'Outstanding!',
               'Impressive!',
               'Excellent!',
               'Superb!',
               'Hurrah!',
               'Noice.',
               'PagChomp',
               'INCREDIBILIS!!!',
               'VI VON ZULUL',
               'He knows da wae',
               'I\'m reporting your for cheating!',
               'NANI!?']
    return random.choice(message)

def lose_message():
    message = ['Feel the wrath of Shao Kahn!',
               'Feel the power of TOASTY!',
               'That was pathetic!',
               'You weak pathetic fool!',
               'Is that your best?',
               'All too easy!',
               'You\'re still trying to win?',
               'Game Over!',
               'Your soul is mine!',
               'It\'s official. You suck!',
               'SHAMEFUR DISPRAY!',
               'VI LOST ZULUL',
               'PepeHands',
               'He doesn\'t know PepeLaugh',
               'Just win looool 4Head',
               'Weebs DansGame',
               'Never lucky BabyRage',
               'P R OMEGALUL',
               'All your base are belong to us',
               'SO BAD LULW SO MAD LULW',
               'Stop it. Get some help.',
               'Jebaited!',
               'Omae wa mou shindeiru']
    return random.choice(message)

if __name__ == '__main__':

    create_edge_table()

    print()
    print(print_board(initial_board()))
    valid_input = ['BLACK', 'WHITE', '1', '2', '@', 'O']
    player = ''
    while player not in valid_input:
        player = input('Do you want to play as BLACK (@) or WHITE (o)? ').upper()

    if player == 'BLACK' or player == '@':
        player = 1
    elif player == 'WHITE' or player == 'O':
        player = 2
    else:
        player = int(player)

    if player == 1:
        board, score = play(user_input, Iago(3))
    else:
        board, score = play(Iago(3), user_input)

    total = len([sq for sq in squares() if sq != EMPTY])
    black = int((total + score) / 2)
    white = total - black

    print()
    print(print_board(board))
    print('Black: {0}'.format(black))
    print('White: {0}\n'.format(white))

    if abs(score) == total:
        print('FLAWLESS VICTORY')
    if abs(score) >= 20:
        print('FATALITY')

    if score == 0:
        print('Draw!')
    elif score > 0:
        print('Black Wins!')
    else:
        print('White Wins!')

    if (score > 0 and player == 1) or (score < 0 and player == 2):
        print(win_message())
    elif score != 0:
        print(lose_message())
    
    input('\nPress [enter] to continue . . . ')
