"""Run with: python -m unittest -v test_othello.py

Independent coordinate-based rules and unpruned minimax check the engine.
Controlled clocks make timeout tests independent of machine speed.
"""
import ast
import contextlib
import io
import json
import random
import unittest
from pathlib import Path
from unittest.mock import patch

import Othello as game

ROOT = Path(__file__).resolve().parent
SQUARES = tuple(10*r+c for r in range(1, 9) for c in range(1, 9))
DIRECTIONS = tuple((r, c) for r in (-1, 0, 1) for c in (-1, 0, 1) if r or c)
game.edge_table[:] = game.load_data(ROOT/'edge_table.txt')


def other(player):
    return 'o' if player == '@' else '@'


def oracle_moves(board, player):
    result = {}
    for square in SQUARES:
        if board[square] != '.':
            continue
        row, col = divmod(square, 10)
        flips = []
        for dr, dc in DIRECTIONS:
            r, c = row+dr, col+dc
            line = []
            while 1 <= r <= 8 and 1 <= c <= 8 and board[10*r+c] == other(player):
                line.append(10*r+c)
                r, c = r+dr, c+dc
            if line and 1 <= r <= 8 and 1 <= c <= 8 and board[10*r+c] == player:
                flips.extend(line)
        if flips:
            result[square] = flips
    return result


def child(board, player, move, flips):
    new_board = list(board)
    new_board[move] = player
    for square in flips:
        new_board[square] = player
    return new_board


def terminal(board, player):
    difference = board.count(player)-board.count(other(player))
    return float('inf') if difference > 0 else float('-inf') if difference < 0 else 0


def minimax(board, player, depth, evaluate):
    moves = oracle_moves(board, player)
    if not moves and not oracle_moves(board, other(player)):
        return terminal(board, player), set()
    if depth == 0:
        return evaluate(player, board), set()
    if not moves:
        return -minimax(board, other(player), depth-1, evaluate)[0], set()
    scores = {move: -minimax(child(board, player, move, flips), other(player), depth-1, evaluate)[0]
              for move, flips in moves.items()}
    best = max(scores.values())
    return best, {move for move, value in scores.items() if value == best}


def positions():
    states, passes = [], []
    for seed in range(20):
        rng = random.Random(seed)
        board, player, turn = game.initial_board(), '@', 1
        while True:
            states.append((list(board), player, turn))
            moves = oracle_moves(board, player)
            if not moves:
                if not oracle_moves(board, other(player)):
                    break
                passes.append((list(board), player, turn))
                player = other(player)
                moves = oracle_moves(board, player)
            move = rng.choice(sorted(moves))
            board = child(board, player, move, moves[move])
            player = other(player)
            turn += 1
    return states, passes


class EngineTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.states, cls.passes = positions()

    def setUp(self):
        game.move_number = 1

    def test_cached_square_order(self):
        expected = sorted(SQUARES, key=lambda sq: game.SQUARE_WEIGHTS[sq], reverse=True)
        self.assertEqual(tuple(expected), game.squares())
        self.assertIs(game.squares(), game.squares())

    def test_equal_player_strings(self):
        class ExternalString(str):
            pass
        for player in ('@', 'o'):
            external = ExternalString(player)
            self.assertEqual(game.opponent(external), other(player))
            self.assertEqual(game.legal_moves(external, game.initial_board()),
                             game.legal_moves(player, game.initial_board()))

    def test_rules_all_sampled_positions(self):
        child_count = 0
        for board, _, _ in self.states:
            for player in ('@', 'o'):
                moves = oracle_moves(board, player)
                self.assertEqual(set(game.legal_moves(player, board)), set(moves))
                for move, flips in moves.items():
                    self.assertEqual(game.make_move(move, player, list(board)),
                                     child(board, player, move, flips))
                    child_count += 1
        self.assertEqual(len(self.states), 1220)
        self.assertEqual(child_count, 19465)

    def test_mobility_counts(self):
        for board, _, _ in self.states[::10]:
            for player in ('@', 'o'):
                current = len(oracle_moves(board, player))
                potential = 0
                for sq in SQUARES:
                    if board[sq] != '.':
                        continue
                    row, col = divmod(sq, 10)
                    potential += any(1 <= row+dr <= 8 and 1 <= col+dc <= 8
                                     and board[10*(row+dr)+col+dc] == other(player)
                                     for dr, dc in DIRECTIONS)
                self.assertEqual(game.mobility(player, board), (current, potential))

    def test_terminal_horizon_never_uses_heuristic(self):
        for black_count in (0, 32, 64):
            board = game.initial_board()
            for index, square in enumerate(SQUARES):
                board[square] = '@' if index < black_count else 'o'
            for player in ('@', 'o'):
                def forbidden(*args):
                    self.fail('A terminal position must not use a heuristic')
                for depth in (0, 1, 3):
                    self.assertEqual(game.alphabeta(player, board, -float('inf'), float('inf'), depth, forbidden, None),
                                     (terminal(board, player), None))

    def test_reachable_early_terminal_and_cli_counts(self):
        fixture = json.loads((ROOT/'early_terminal.json').read_text())
        board = game.initial_board()
        for player, move in fixture['moves']:
            moves = oracle_moves(board, player)
            self.assertIn(move, moves)
            board = child(board, player, move, moves[move])
        self.assertEqual(''.join(board), fixture['board'])
        game.move_number = 60
        self.assertEqual(game.alphabeta('@', board, -float('inf'), float('inf'), 0, game.Iago_eval, None),
                         (-float('inf'), None))
        tree = ast.parse((ROOT/'Othello.py').read_text())
        main = next(node for node in tree.body if isinstance(node, ast.If)
                    and isinstance(node.test, ast.Compare)
                    and isinstance(node.test.left, ast.Name) and node.test.left.id == '__name__')
        scope = game.__dict__.copy()
        answers = iter(['BLACK', ''])
        scope.update(play=lambda *args: (list(board), -13),
                     create_edge_table=lambda: None, input=lambda prompt='': next(answers))
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            exec(compile(ast.Module(body=main.body, type_ignores=[]), 'CLI-block', 'exec'), scope)
        self.assertIn('Black: 25', output.getvalue())
        self.assertIn('White: 38', output.getvalue())
        self.assertEqual(scope['total'], 63)

    def test_search_against_terminal_first_minimax(self):
        cases = self.states[::max(1, len(self.states)//24)] + self.passes
        for board, player, turn in cases:
            game.move_number = turn
            for depth in (1, 2, 3):
                expected, best = minimax(board, player, depth, game.Iago_eval)
                before = list(board)
                value, move = game.alphabeta(player, board, -float('inf'), float('inf'), depth, game.Iago_eval, None)
                self.assertEqual(value, expected)
                if best:
                    self.assertIn(move, best)
                else:
                    self.assertIsNone(move)
                self.assertEqual(board, before)
        self.assertEqual(len(cases)*3, 99)

    def test_zero_budget_legal_fallback_without_evaluation(self):
        board = game.initial_board()
        def forbidden(*args):
            self.fail('Zero budget must not evaluate a leaf')
        with patch.object(game, 'perf_counter', return_value=100.0):
            move = game.alphabeta_iterative(10, forbidden, time_limit=0)(game.BLACK, board)
        self.assertEqual(move, game.legal_moves(game.BLACK, board)[0])

    def test_recursive_timeout_keeps_completed_depth_and_board(self):
        board = game.initial_board()
        before = list(board)
        clock, eval_count = [0.0], [0]
        weights = {34: 1, 43: 2, 56: 3, 65: 4}
        def static(player, b):
            return sum(weight*((b[sq] == player)-(b[sq] == other(player)))
                       for sq, weight in weights.items())
        depth_one = game.alphabeta('@', board, -float('inf'), float('inf'), 1, static, None)[1]
        self.assertEqual(depth_one, 65)
        def evaluate(player, b):
            eval_count[0] += 1
            if eval_count[0] == 6:
                clock[0] = 2.0
            return static(player, b)
        with patch.object(game, 'perf_counter', side_effect=lambda: clock[0]):
            move = game.alphabeta_iterative(10, evaluate, time_limit=1.0)('@', board)
        self.assertEqual(eval_count[0], 6)
        self.assertEqual(move, depth_one)
        self.assertEqual(board, before)
        # An interrupted search must not poison the reusable board buffers.
        expected, best = minimax(board, '@', 3, static)
        value, move = game.alphabeta('@', board, -float('inf'), float('inf'), 3, static, None)
        self.assertEqual(value, expected)
        self.assertIn(move, best)

    def test_deadline_is_reset_for_each_move(self):
        clock, deadlines = [10.0], []
        def search(player, board, alpha, beta, depth, evaluate, killer, deadline=None):
            deadlines.append(deadline)
            return 0, game.legal_moves(player, board)[0]
        strategy = game.alphabeta_iterative(1, game.score, time_limit=2.0)
        with patch.object(game, 'perf_counter', side_effect=lambda: clock[0]), patch.object(game, 'alphabeta', side_effect=search):
            strategy('@', game.initial_board())
            clock[0] = 500.0
            strategy('@', game.initial_board())
        self.assertEqual(deadlines, [12.0, 502.0])

    def test_no_deadline_never_reads_clock(self):
        with patch.object(game, 'perf_counter', side_effect=AssertionError('No deadline should read the clock')):
            move = game.Iago(3, time_limit=None)(game.BLACK, game.initial_board())
        self.assertIn(move, game.legal_moves(game.BLACK, game.initial_board()))

    def test_no_moves_returns_none(self):
        fixture = json.loads((ROOT/'early_terminal.json').read_text())
        self.assertIsNone(game.Iago(10)(game.BLACK, list(fixture['board'])))
        self.assertTrue(self.passes)
        board, player, _ = self.passes[0]
        self.assertIsNone(game.Iago(10)(player, board))

    def test_configuration_validation(self):
        for depth in (-1, 0, 40, 2.5):
            with self.assertRaises(ValueError):
                game.Iago(depth)
        with self.assertRaises(ValueError):
            game.Iago(3, time_limit=-1)


if __name__ == '__main__':
    unittest.main(verbosity=2)
