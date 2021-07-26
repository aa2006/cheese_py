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
    pawnWhiteTable = [
        0,  0,  0,  0,  0,  0,  0,  0,
        50, 50, 50, 50, 50, 50, 50, 50,
        10, 10, 20, 30, 30, 20, 10, 10,
        5,  5, 10, 25, 25, 10,  5,  5,
        0,  0,  0, 20, 20,  0,  0,  0,
        5, -5,-10,  0,  0,-10, -5,  5,
        5, 10, 10,-20,-20, 10, 10,  5,
        0,  0,  0,  0,  0,  0,  0,  0
    ]
    pawnBlackTable = list(reversed(pawnWhiteTable))

    knightWhiteTable = [
        -50,-40,-30,-30,-30,-30,-40,-50,
        -40,-20,  0,  0,  0,  0,-20,-40,
        -30,  0, 10, 15, 15, 10,  0,-30,
        -30,  5, 15, 20, 20, 15,  5,-30,
        -30,  0, 15, 20, 20, 15,  0,-30,
        -30,  5, 10, 15, 15, 10,  5,-30,
        -40,-20,  0,  5,  5,  0,-20,-40,
        -50,-40,-30,-30,-30,-30,-40,-50
    ]
    knightBlackTable = list(reversed(knightWhiteTable))

    bishopWhiteTable = [
        -20,-10,-10,-10,-10,-10,-10,-20,
        -10,  0,  0,  0,  0,  0,  0,-10,
        -10,  0,  5, 10, 10,  5,  0,-10,
        -10,  5,  5, 10, 10,  5,  5,-10,
        -10,  0, 10, 10, 10, 10,  0,-10,
        -10, 10, 10, 10, 10, 10, 10,-10,
        -10,  5,  0,  0,  0,  0,  5,-10,
        -20,-10,-10,-10,-10,-10,-10,-20
    ]
    bishopBlackTable = list(reversed(bishopWhiteTable))

    rookWhiteTable = [
        0,  0,  0,  0,  0,  0,  0,  0,
        5, 10, 10, 10, 10, 10, 10,  5,
        -5,  0,  0,  0,  0,  0,  0, -5,
        -5,  0,  0,  0,  0,  0,  0, -5,
        -5,  0,  0,  0,  0,  0,  0, -5,
        -5,  0,  0,  0,  0,  0,  0, -5,
        -5,  0,  0,  0,  0,  0,  0, -5,
        0,  0,  0,  5,  5,  0,  0,  0
    ]
    rookBlackTable = list(reversed(rookWhiteTable))

    queenWhiteTable = [
        -20,-10,-10, -5, -5,-10,-10,-20,
        -10,  0,  0,  0,  0,  0,  0,-10,
        -10,  0,  5,  5,  5,  5,  0,-10,
        -5,  0,  5,  5,  5,  5,  0, -5,
        0,  0,  5,  5,  5,  5,  0, -5,
        -10,  5,  5,  5,  5,  5,  0,-10,
        -10,  0,  5,  0,  0,  0,  0,-10,
        -20,-10,-10, -5, -5,-10,-10,-20
    ]
    queenBlackTable = list(reversed(queenWhiteTable))

    kingWhiteMiddlegameTable = [
        -30,-40,-40,-50,-50,-40,-40,-30,
        -30,-40,-40,-50,-50,-40,-40,-30,
        -30,-40,-40,-50,-50,-40,-40,-30,
        -30,-40,-40,-50,-50,-40,-40,-30,
        -20,-30,-30,-40,-40,-30,-30,-20,
        -10,-20,-20,-20,-20,-20,-20,-10,
        20, 20,  0,  0,  0,  0, 20, 20,
        20, 30, 10,  0,  0, 10, 30, 20
    ]
    kingBlackMiddlegameTable = list(reversed(kingWhiteMiddlegameTable))

    kingWhiteEndgameTable = [
        -50,-40,-30,-20,-20,-30,-40,-50,
        -30,-20,-10,  0,  0,-10,-20,-30,
        -30,-10, 20, 30, 30, 20,-10,-30,
        -30,-10, 30, 40, 40, 30,-10,-30,
        -30,-10, 30, 40, 40, 30,-10,-30,
        -30,-10, 20, 30, 30, 20,-10,-30,
        -30,-30,  0,  0,  0,  0,-30,-30,
        -50,-30,-30,-30,-30,-30,-30,-50
    ]
    kingBlackEndgameTable = list(reversed(kingWhiteEndgameTable))

    def check_end_game(self, board):
        queens = 0
        minors = 0

        for square in chess.SQUARES:
            piece = board.piece_at(square)
            if piece and piece.piece_type == chess.QUEEN:
                queens += 1
            if piece and (piece.piece_type == chess.BISHOP or piece.piece_type == chess.KNIGHT):
                minors += 1

        if queens == 0 or (queens == 2 and minors <= 1):
            return True

        return False

    def piece_value(self, piece):
        if piece == None:
            return 0

        if piece.piece_type == chess.PAWN:
            return 100
        if piece.piece_type == chess.KNIGHT:
            return 320
        if piece.piece_type == chess.BISHOP:
            return 330
        if piece.piece_type == chess.ROOK:
            return 500
        if piece.piece_type == chess.QUEEN:
            return 900
        if piece.piece_type == chess.KING:
            return 200000
        
        return 0

    def eval_piece(self, piece, square, endgame):
        if piece == None:
            return 0

        mapping = []

        if piece.piece_type == chess.PAWN:
            mapping = self.pawnWhiteTable if piece.color == chess.WHITE else self.pawnBlackTable
        if piece.piece_type == chess.KNIGHT:
            mapping = self.knightWhiteTable if piece.color == chess.WHITE else self.knightBlackTable
        if piece.piece_type == chess.BISHOP:
            mapping = self.bishopWhiteTable if piece.color == chess.WHITE else self.bishopBlackTable
        if piece.piece_type == chess.ROOK:
            mapping = self.rookWhiteTable if piece.color == chess.WHITE else self.rookBlackTable
        if piece.piece_type == chess.QUEEN:
            mapping = self.queenWhiteTable if piece.color == chess.WHITE else self.queenBlackTable
        if piece.piece_type == chess.KING:
            if endgame:
                mapping = (
                    self.kingWhiteEndgameTable if piece.color == chess.WHITE else self.kingBlackEndgameTable
                )
            else:
                mapping = self.kingWhiteMiddlegameTable if piece.color == chess.WHITE else self.kingBlackMiddlegameTable
        
        return mapping[square]

    def evaluate_board(self, board):
        total = 0

        for square in chess.SQUARES:
            piece = board.piece_at(square)
            if not piece:
                continue
            
            endgame = self.check_end_game(board)
            value = self.piece_value(piece) + self.eval_piece(piece, square, endgame)
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
        return self.minimax_root(2, board)