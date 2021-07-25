"""
Some example strategies for people who want to create a custom, homemade bot.
And some handy classes to extend
"""

import chess
import random
from engine_wrapper import EngineWrapper


class FillerEngine:
    """
    Not meant to be an actual engine.

    This is only used to provide the property "self.engine"
    in "MinimalEngine" which extends "EngineWrapper"
    """
    def __init__(self, main_engine, name=None):
        self.id = {
            "name": name
        }
        self.name = name
        self.main_engine = main_engine

    def __getattr__(self, method_name):
        main_engine = self.main_engine

        def method(*args, **kwargs):
            nonlocal main_engine
            nonlocal method_name
            return main_engine.notify(method_name, *args, **kwargs)

        return method


class MinimalEngine(EngineWrapper):
    """
    Subclass this to prevent a few random errors

    Even though MinimalEngine extends EngineWrapper,
    you don't have to actually wrap an engine.

    At minimum, just implement `search`,
    however you can also change other methods like
    `notify`, `first_search`, `get_time_control`, etc.
    """
    def __init__(self, *args, name=None):
        super().__init__(*args)

        self.engine_name = self.__class__.__name__ if name is None else name

        self.last_move_info = []
        self.engine = FillerEngine(self, name=self.name)
        self.engine.id = {
            "name": self.engine_name
        }

    def search_with_ponder(self, board, wtime, btime, winc, binc, ponder):
        timeleft = 0
        if board.turn:
            timeleft = wtime
        else:
            timeleft = btime
        return self.search(board, timeleft, ponder)

    def search(self, board, timeleft, ponder):
        raise NotImplementedError("The search method is not implemented")

    def notify(self, method_name, *args, **kwargs):
        """
        The EngineWrapper class sometimes calls methods on "self.engine".
        "self.engine" is a filler property that notifies <self> 
        whenever an attribute is called.

        Nothing happens unless the main engine does something.

        Simply put, the following code is equivalent
        self.engine.<method_name>(<*args>, <**kwargs>)
        self.notify(<method_name>, <*args>, <**kwargs>)
        """
        pass


class ExampleEngine(MinimalEngine):
    pass

class Move(ExampleEngine):
    def piece_value(self, piece):
        if piece == None:
            return 0

        if piece.piece_type == chess.PAWN:
            return 1
        if piece.piece_type == chess.KNIGHT:
            return 3
        if piece.piece_type == chess.BISHOP:
            return 3
        if piece.piece_type == chess.ROOK:
            return 5
        if piece.piece_type == chess.QUEEN:
            return 9
        if piece.piece_type == chess.KING:
            return 1000
        
        return 0

    def evaluate_board(self, board):
        total = 0
        for square in chess.SQUARES:
            piece = board.piece_at(square)
            if not piece:
                continue
            value = self.piece_value(piece)
            total += value if piece.color == chess.WHITE else -value
        
        return total

    def minimax(self, depth, board, alpha, beta, is_maximising_player):
        if board.is_checkmate():
            return -float("inf") if is_maximising_player else float("inf")
        elif board.is_game_over():
            return 0

        if depth == 0:
            return self.evaluate_board(board)

        if is_maximising_player:
            best_move = -float("inf")
            moves = (list(board.legal_moves))
            for move in moves:
                board.push(move)
                best_move = max(
                    best_move,
                    self.minimax(depth - 1, board, alpha, beta, not is_maximising_player),
                )
                board.pop()
                alpha = max(alpha, best_move)
                if beta <= alpha:
                    return best_move
            return best_move
        else:
            best_move = float("inf")
            moves = (list(board.legal_moves))
            for move in moves:
                board.push(move)
                best_move = min(
                    best_move,
                    self.minimax(depth - 1, board, alpha, beta, not is_maximising_player),
                )
                board.pop()
                beta = min(beta, best_move)
                if beta <= alpha:
                    return best_move
            return best_move

    def minimax_root(self, depth, board):
        maximize = board.turn == chess.WHITE
        best_move = -float("inf")
        if not maximize:
            best_move = float("inf")

        moves = (list(board.legal_moves))
        best_move_found = moves[0]

        for move in moves:
            board.push(move)
            if board.can_claim_draw():
                value = 0.0
            else:
                value = self.minimax(depth - 1, board, -float("inf"), float("inf"), not maximize)
            board.pop()
            if maximize and value >= best_move:
                best_move = value
                best_move_found = move
            elif not maximize and value <= best_move:
                best_move = value
                best_move_found = move

        return best_move_found

    def search(self, board, *args):
        if board.fullmove_number < 3:
            return random.choice(list(board.legal_moves))
        return self.minimax_root(3, board)