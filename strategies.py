"""
Some example strategies for people who want to create a custom, homemade bot.
And some handy classes to extend
"""

import chess
import random
from engine_wrapper import EngineWrapper
from model import Game


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

    def is_equivalent(self, fen, board2):
        board1 = chess.Board(fen)
        for square in chess.SQUARES :
            if board1.piece_at(square) != board2.piece_at(square):
                return False
        return True

    def move_from_book(self, board):
        tscp_op = [['g1f3', 'g8f6', 'c2c4', 'b7b6', 'g2g3'], ['g1f3', 'g8f6', 'c2c4', 'c7c5', 'b1c3', 'b8c6'], ['g1f3', 'g8f6', 'c2c4', 'c7c5', 'b1c3', 'e7e6', 'g2g3', 'b7b6', 'f1g2', 'c8b7', 'e1g1', 'f8e7'], ['g1f3', 'g8f6', 'c2c4', 'c7c5', 'g2g3'], ['g1f3', 'g8f6', 'c2c4', 'e7e6', 'b1c3', 'd7d5', 'd2d4', 'b8d7'], ['g1f3', 'g8f6', 'c2c4', 'e7e6', 'b1c3', 'd7d5', 'd2d4', 'f8e7', 'c1f4', 'e8g8', 'e2e3'], ['g1f3', 'g8f6', 'c2c4', 'e7e6', 'b1c3', 'd7d5', 'd2d4', 'f8e7', 'c1g5', 'h7h6', 'g5h4', 'e8g8', 'e2e3', 'b7b6'], ['g1f3', 'g8f6', 'c2c4', 'e7e6', 'b1c3', 'd7d5', 'd2d4', 'f8e7', 'c1g5', 'e8g8', 'e2e3', 'h7h6'], ['g1f3', 'g8f6', 'c2c4', 'e7e6', 'b1c3', 'd7d5', 'd2d4', 'f8b4'], ['g1f3', 'g8f6', 'c2c4', 'e7e6', 'b1c3', 'd7d5', 'd2d4', 'c7c6', 'c1g5'], ['g1f3', 'g8f6', 'c2c4', 'e7e6', 'b1c3', 'd7d5', 'd2d4', 'c7c6', 'e2e3', 'b8d7', 'd1c2', 'f8d6'], ['g1f3', 'g8f6', 'c2c4', 'e7e6', 'b1c3', 'd7d5', 'd2d4', 'c7c6', 'e2e3', 'b8d7', 'f1d3', 'd5c4', 'd3c4', 'b7b5', 'c4d3'], ['g1f3', 'g8f6', 'c2c4', 'e7e6', 'b1c3', 'd7d5', 'd2d4', 'c7c5'], ['g1f3', 'g8f6', 'c2c4', 'e7e6', 'g2g3', 'd7d5', 'f1g2', 'f8e7'], ['g1f3', 'g8f6', 'c2c4', 'g7g6', 'b1c3', 'f8g7', 'e2e4'], ['g1f3', 'g8f6', 'c2c4', 'g7g6', 'g2g3', 'f8g7', 'f1g2', 'e8g8'], ['g1f3', 'g8f6', 'd2d4', 'c7c5'], ['g1f3', 'g8f6', 'd2d4', 'd7d5', 'c2c4', 'c7c6', 'b1c3', 'd5c4', 'a2a4', 'c8f5', 'e2e3', 'e7e6', 'f1c4'], ['g1f3', 'g8f6', 'd2d4', 'd7d5', 'c2c4', 'c7c6', 'b1c3', 'e7e6', 'c1g5'], ['g1f3', 'g8f6', 'd2d4', 'd7d5', 'c2c4', 'c7c6', 'b1c3', 'e7e6', 'e2e3', 'b8d7', 'd1c2', 'f8d6'], ['g1f3', 'g8f6', 'd2d4', 'd7d5', 'c2c4', 'c7c6', 'b1c3', 'e7e6', 'e2e3', 'b8d7', 'f1d3', 'd5c4', 'd3c4', 'b7b5', 'c4d3'], ['g1f3', 'g8f6', 'd2d4', 'd7d5', 'c2c4', 'c7c6', 'e2e3'], ['g1f3', 'g8f6', 'd2d4', 'd7d5', 'c2c4', 'd5c4', 'e2e3', 'e7e6', 'f1c4', 'c7c5', 'e1g1', 'a7a6'], ['g1f3', 'g8f6', 'd2d4', 'd7d5', 'c2c4', 'e7e6', 'b1c3', 'b8d7'], ['g1f3', 'g8f6', 'd2d4', 'd7d5', 'c2c4', 'e7e6', 'b1c3', 'f8e7', 'c1f4', 'e8g8', 'e2e3'], ['g1f3', 'g8f6', 'd2d4', 'd7d5', 'c2c4', 'e7e6', 'b1c3', 'f8e7', 'c1g5', 'h7h6', 'g5h4', 'e8g8', 'e2e3', 'b7b6'], ['g1f3', 'g8f6', 'd2d4', 'd7d5', 'c2c4', 'e7e6', 'b1c3', 'f8e7', 'c1g5', 'e8g8', 'e2e3', 'h7h6'], ['g1f3', 'g8f6', 'd2d4', 'd7d5', 'c2c4', 'e7e6', 'b1c3', 'f8b4'], ['g1f3', 'g8f6', 'd2d4', 'd7d5', 'c2c4', 'e7e6', 'b1c3', 'c7c6', 'c1g5'], ['g1f3', 'g8f6', 'd2d4', 'd7d5', 'c2c4', 'e7e6', 'b1c3', 'c7c6', 'e2e3', 'b8d7', 'd1c2', 'f8d6'], ['g1f3', 'g8f6', 'd2d4', 'd7d5', 'c2c4', 'e7e6', 'b1c3', 'c7c6', 'e2e3', 'b8d7', 'f1d3', 'd5c4', 'd3c4', 'b7b5', 'c4d3'], ['g1f3', 'g8f6', 'd2d4', 'd7d5', 'c2c4', 'e7e6', 'b1c3', 'c7c5'], ['g1f3', 'g8f6', 'd2d4', 'd7d5', 'c2c4', 'e7e6', 'c1g5'], ['g1f3', 'g8f6', 'd2d4', 'd7d5', 'c2c4', 'e7e6', 'g2g3'], ['g1f3', 'g8f6', 'd2d4', 'e7e6', 'c1g5'], ['g1f3', 'g8f6', 'd2d4', 'e7e6', 'c2c4', 'f8b4', 'b1d2'], ['g1f3', 'g8f6', 'd2d4', 'e7e6', 'c2c4', 'f8b4', 'c1d2'], ['g1f3', 'g8f6', 'd2d4', 'e7e6', 'c2c4', 'b7b6', 'b1c3', 'c8b7', 'a2a3', 'd7d5', 'c4d5', 'f6d5'], ['g1f3', 'g8f6', 'd2d4', 'e7e6', 'c2c4', 'b7b6', 'b1c3', 'f8b4'], ['g1f3', 'g8f6', 'd2d4', 'e7e6', 'c2c4', 'b7b6', 'a2a3', 'c8b7', 'b1c3', 'd7d5', 'c4d5', 'f6d5'], ['g1f3', 'g8f6', 'd2d4', 'e7e6', 'c2c4', 'b7b6', 'g2g3', 'c8b7', 'f1g2', 'f8e7', 'e1g1', 'e8g8', 'b1c3', 'f6e4', 'd1c2', 'e4c3', 'c2c3'], ['g1f3', 'g8f6', 'd2d4', 'e7e6', 'c2c4', 'b7b6', 'g2g3', 'c8a6', 'b2b3', 'f8b4', 'c1d2', 'b4e7'], ['g1f3', 'g8f6', 'd2d4', 'e7e6', 'c2c4', 'c7c5', 'd4d5', 'e6d5', 'c4d5', 'd7d6', 'b1c3', 'g7g6'], ['g1f3', 'g8f6', 'd2d4', 'e7e6', 'c2c4', 'd7d5', 'b1c3', 'b8d7'], ['g1f3', 'g8f6', 'd2d4', 'e7e6', 'c2c4', 'd7d5', 'b1c3', 'f8e7', 'c1f4', 'e8g8', 'e2e3'], ['g1f3', 'g8f6', 'd2d4', 'e7e6', 'c2c4', 'd7d5', 'b1c3', 'f8e7', 'c1g5', 'h7h6', 'g5h4', 'e8g8', 'e2e3', 'b7b6'], ['g1f3', 'g8f6', 'd2d4', 'e7e6', 'c2c4', 'd7d5', 'b1c3', 'f8e7', 'c1g5', 'e8g8', 'e2e3', 'h7h6'], ['g1f3', 'g8f6', 'd2d4', 'e7e6', 'c2c4', 'd7d5', 'b1c3', 'f8b4'], ['g1f3', 'g8f6', 'd2d4', 'e7e6', 'c2c4', 'd7d5', 'b1c3', 'c7c6', 'c1g5'], ['g1f3', 'g8f6', 'd2d4', 'e7e6', 'c2c4', 'd7d5', 'b1c3', 'c7c6', 'e2e3', 'b8d7', 'd1c2', 'f8d6'], ['g1f3', 'g8f6', 'd2d4', 'e7e6', 'c2c4', 'd7d5', 'b1c3', 'c7c6', 'e2e3', 'b8d7', 'f1d3', 'd5c4', 'd3c4', 'b7b5', 'c4d3'], ['g1f3', 'g8f6', 'd2d4', 'e7e6', 'c2c4', 'd7d5', 'b1c3', 'c7c5'], ['g1f3', 'g8f6', 'd2d4', 'e7e6', 'c2c4', 'd7d5', 'c1g5'], ['g1f3', 'g8f6', 'd2d4', 'e7e6', 'c2c4', 'd7d5', 'g2g3'], ['g1f3', 'g8f6', 'd2d4', 'e7e6', 'g2g3'], ['g1f3', 'g8f6', 'd2d4', 'g7g6', 'c1g5'], ['g1f3', 'g8f6', 'd2d4', 'g7g6', 'c2c4', 'f8g7', 'b1c3', 'e8g8', 'e2e4', 'd7d6', 'f1e2', 'e7e5', 'e1g1', 'b8c6', 'd4d5', 'c6e7', 'f3e1', 'f6d7'], ['g1f3', 'g8f6', 'd2d4', 'g7g6', 'c2c4', 'f8g7', 'g2g3', 'e8g8', 'f1g2', 'd7d6', 'e1g1'], ['g1f3', 'g8f6', 'd2d4', 'g7g6', 'g2g3', 'f8g7', 'f1g2', 'e8g8'], ['g1f3', 'g8f6', 'g2g3', 'g7g6'], ['g1f3', 'c7c5', 'c2c4', 'b8c6'], ['g1f3', 'c7c5', 'c2c4', 'g8f6', 'b1c3', 'b8c6'], ['g1f3', 'c7c5', 'c2c4', 'g8f6', 'b1c3', 'e7e6', 'g2g3', 'b7b6', 'f1g2', 'c8b7', 'e1g1', 'f8e7'], ['g1f3', 'c7c5', 'c2c4', 'g8f6', 'g2g3'], ['g1f3', 'd7d5', 'c2c4'], ['g1f3', 'd7d5', 'd2d4', 'g8f6', 'c2c4', 'c7c6', 'b1c3', 'd5c4', 'a2a4', 'c8f5', 'e2e3', 'e7e6', 'f1c4'], ['g1f3', 'd7d5', 'd2d4', 'g8f6', 'c2c4', 'c7c6', 'b1c3', 'e7e6', 'c1g5'], ['g1f3', 'd7d5', 'd2d4', 'g8f6', 'c2c4', 'c7c6', 'b1c3', 'e7e6', 'e2e3', 'b8d7', 'd1c2', 'f8d6'], ['g1f3', 'd7d5', 'd2d4', 'g8f6', 'c2c4', 'c7c6', 'b1c3', 'e7e6', 'e2e3', 'b8d7', 'f1d3', 'd5c4', 'd3c4', 'b7b5', 'c4d3'], ['g1f3', 'd7d5', 'd2d4', 'g8f6', 'c2c4', 'c7c6', 'e2e3'], ['g1f3', 'd7d5', 'd2d4', 'g8f6', 'c2c4', 'd5c4', 'e2e3', 'e7e6', 'f1c4', 'c7c5', 'e1g1', 'a7a6'], ['g1f3', 'd7d5', 'd2d4', 'g8f6', 'c2c4', 'e7e6', 'b1c3', 'b8d7'], ['g1f3', 'd7d5', 'd2d4', 'g8f6', 'c2c4', 'e7e6', 'b1c3', 'f8e7', 'c1f4', 'e8g8', 'e2e3'], ['g1f3', 'd7d5', 'd2d4', 'g8f6', 'c2c4', 'e7e6', 'b1c3', 'f8e7', 'c1g5', 'h7h6', 'g5h4', 'e8g8', 'e2e3', 'b7b6'], ['g1f3', 'd7d5', 'd2d4', 'g8f6', 'c2c4', 'e7e6', 'b1c3', 'f8e7', 'c1g5', 'e8g8', 'e2e3', 'h7h6'], ['g1f3', 'd7d5', 'd2d4', 'g8f6', 'c2c4', 'e7e6', 'b1c3', 'f8b4'], ['g1f3', 'd7d5', 'd2d4', 'g8f6', 'c2c4', 'e7e6', 'b1c3', 'c7c6', 'c1g5'], ['g1f3', 'd7d5', 'd2d4', 'g8f6', 'c2c4', 'e7e6', 'b1c3', 'c7c6', 'e2e3', 'b8d7', 'd1c2', 'f8d6'], ['g1f3', 'd7d5', 'd2d4', 'g8f6', 'c2c4', 'e7e6', 'b1c3', 'c7c6', 'e2e3', 'b8d7', 'f1d3', 'd5c4', 'd3c4', 'b7b5', 'c4d3'], ['g1f3', 'd7d5', 'd2d4', 'g8f6', 'c2c4', 'e7e6', 'b1c3', 'c7c5'], ['g1f3', 'd7d5', 'd2d4', 'g8f6', 'c2c4', 'e7e6', 'c1g5'], ['g1f3', 'd7d5', 'd2d4', 'g8f6', 'c2c4', 'e7e6', 'g2g3'], ['g1f3', 'd7d5', 'g2g3'], ['g1f3', 'g7g6'], ['c2c4', 'g8f6', 'b1c3', 'c7c5'], ['c2c4', 'g8f6', 'b1c3', 'e7e6', 'g1f3', 'd7d5', 'd2d4', 'b8d7'], ['c2c4', 'g8f6', 'b1c3', 'e7e6', 'g1f3', 'd7d5', 'd2d4', 'f8e7', 'c1f4', 'e8g8', 'e2e3'], ['c2c4', 'g8f6', 'b1c3', 'e7e6', 'g1f3', 'd7d5', 'd2d4', 'f8e7', 'c1g5', 'h7h6', 'g5h4', 'e8g8', 'e2e3', 'b7b6'], ['c2c4', 'g8f6', 'b1c3', 'e7e6', 'g1f3', 'd7d5', 'd2d4', 'f8e7', 'c1g5', 'e8g8', 'e2e3', 'h7h6'], ['c2c4', 'g8f6', 'b1c3', 'e7e6', 'g1f3', 'd7d5', 'd2d4', 'f8b4'], ['c2c4', 'g8f6', 'b1c3', 'e7e6', 'g1f3', 'd7d5', 'd2d4', 'c7c6', 'c1g5'], ['c2c4', 'g8f6', 'b1c3', 'e7e6', 'g1f3', 'd7d5', 'd2d4', 'c7c6', 'e2e3', 'b8d7', 'd1c2', 'f8d6'], ['c2c4', 'g8f6', 'b1c3', 'e7e6', 'g1f3', 'd7d5', 'd2d4', 'c7c6', 'e2e3', 'b8d7', 'f1d3', 'd5c4', 'd3c4', 'b7b5', 'c4d3'], ['c2c4', 'g8f6', 'b1c3', 'e7e6', 'g1f3', 'd7d5', 'd2d4', 'c7c5'], ['c2c4', 'g8f6', 'b1c3', 'e7e5', 'g1f3', 'b8c6', 'g2g3'], ['c2c4', 'g8f6', 'b1c3', 'g7g6'], ['c2c4', 'g8f6', 'g1f3', 'b7b6', 'g2g3'], ['c2c4', 'g8f6', 'g1f3', 'c7c5', 'b1c3', 'b8c6'], ['c2c4', 'g8f6', 'g1f3', 'c7c5', 'b1c3', 'e7e6', 'g2g3', 'b7b6', 'f1g2', 'c8b7', 'e1g1', 'f8e7'], ['c2c4', 'g8f6', 'g1f3', 'c7c5', 'g2g3'], ['c2c4', 'g8f6', 'g1f3', 'e7e6', 'b1c3', 'd7d5', 'd2d4', 'b8d7'], ['c2c4', 'g8f6', 'g1f3', 'e7e6', 'b1c3', 'd7d5', 'd2d4', 'f8e7', 'c1f4', 'e8g8', 'e2e3'], ['c2c4', 'g8f6', 'g1f3', 'e7e6', 'b1c3', 'd7d5', 'd2d4', 'f8e7', 'c1g5', 'h7h6', 'g5h4', 'e8g8', 'e2e3', 'b7b6'], ['c2c4', 'g8f6', 'g1f3', 'e7e6', 'b1c3', 'd7d5', 'd2d4', 'f8e7', 'c1g5', 'e8g8', 'e2e3', 'h7h6'], ['c2c4', 'g8f6', 'g1f3', 'e7e6', 'b1c3', 'd7d5', 'd2d4', 'f8b4'], ['c2c4', 'g8f6', 'g1f3', 'e7e6', 'b1c3', 'd7d5', 'd2d4', 'c7c6', 'c1g5'], ['c2c4', 'g8f6', 'g1f3', 'e7e6', 'b1c3', 'd7d5', 'd2d4', 'c7c6', 'e2e3', 'b8d7', 'd1c2', 'f8d6'], ['c2c4', 'g8f6', 'g1f3', 'e7e6', 'b1c3', 'd7d5', 'd2d4', 'c7c6', 'e2e3', 'b8d7', 'f1d3', 'd5c4', 'd3c4', 'b7b5', 'c4d3'], ['c2c4', 'g8f6', 'g1f3', 'e7e6', 'b1c3', 'd7d5', 'd2d4', 'c7c5'], ['c2c4', 'g8f6', 'g1f3', 'e7e6', 'g2g3', 'd7d5', 'f1g2', 'f8e7'], ['c2c4', 'g8f6', 'g1f3', 'g7g6', 'b1c3', 'f8g7', 'e2e4'], ['c2c4', 'g8f6', 'g1f3', 'g7g6', 'g2g3', 'f8g7', 'f1g2', 'e8g8'], ['c2c4', 'c7c6'], ['c2c4', 'c7c5', 'g1f3', 'b8c6'], ['c2c4', 'c7c5', 'g1f3', 'g8f6', 'b1c3', 'b8c6'], ['c2c4', 'c7c5', 'g1f3', 'g8f6', 'b1c3', 'e7e6', 'g2g3', 'b7b6', 'f1g2', 'c8b7', 'e1g1', 'f8e7'], ['c2c4', 'c7c5', 'g1f3', 'g8f6', 'g2g3'], ['c2c4', 'e7e6', 'b1c3', 'd7d5', 'd2d4', 'f8e7', 'g1f3', 'g8f6', 'c1f4', 'e8g8', 'e2e3'], ['c2c4', 'e7e6', 'b1c3', 'd7d5', 'd2d4', 'f8e7', 'g1f3', 'g8f6', 'c1g5', 'h7h6', 'g5h4', 'e8g8', 'e2e3', 'b7b6'], ['c2c4', 'e7e6', 'b1c3', 'd7d5', 'd2d4', 'f8e7', 'g1f3', 'g8f6', 'c1g5', 'e8g8', 'e2e3', 'h7h6'], ['c2c4', 'e7e6', 'b1c3', 'd7d5', 'd2d4', 'g8f6', 'c1g5', 'f8e7', 'e2e3'], ['c2c4', 'e7e6', 'b1c3', 'd7d5', 'd2d4', 'g8f6', 'g1f3', 'b8d7'], ['c2c4', 'e7e6', 'b1c3', 'd7d5', 'd2d4', 'g8f6', 'g1f3', 'f8e7', 'c1f4', 'e8g8', 'e2e3'], ['c2c4', 'e7e6', 'b1c3', 'd7d5', 'd2d4', 'g8f6', 'g1f3', 'f8e7', 'c1g5', 'h7h6', 'g5h4', 'e8g8', 'e2e3', 'b7b6'], ['c2c4', 'e7e6', 'b1c3', 'd7d5', 'd2d4', 'g8f6', 'g1f3', 'f8e7', 'c1g5', 'e8g8', 'e2e3', 'h7h6'], ['c2c4', 'e7e6', 'b1c3', 'd7d5', 'd2d4', 'g8f6', 'g1f3', 'f8b4'], ['c2c4', 'e7e6', 'b1c3', 'd7d5', 'd2d4', 'g8f6', 'g1f3', 'c7c6', 'c1g5'], ['c2c4', 'e7e6', 'b1c3', 'd7d5', 'd2d4', 'g8f6', 'g1f3', 'c7c6', 'e2e3', 'b8d7', 'd1c2', 'f8d6'], ['c2c4', 'e7e6', 'b1c3', 'd7d5', 'd2d4', 'g8f6', 'g1f3', 'c7c6',
        'e2e3', 'b8d7', 'f1d3', 'd5c4', 'd3c4', 'b7b5', 'c4d3'], ['c2c4', 'e7e6', 'b1c3', 'd7d5', 'd2d4', 'g8f6', 'g1f3', 'c7c5'], ['c2c4', 'e7e6', 'b1c3', 'd7d5', 'd2d4', 'g8f6', 'c4d5', 'e6d5', 'c1g5'], ['c2c4', 'e7e6', 'b1c3', 'd7d5', 'd2d4', 'c7c6'], ['c2c4', 'e7e6', 'g1f3'], ['c2c4', 'e7e5', 'b1c3', 'b8c6'], ['c2c4', 'e7e5', 'b1c3', 'g8f6', 'g1f3', 'b8c6', 'g2g3'], ['c2c4', 'e7e5', 'g2g3'], ['c2c4', 'g7g6', 'b1c3'], ['d2d4', 'g8f6', 'c1g5'], ['d2d4', 'g8f6', 'g1f3', 'c7c5'], ['d2d4', 'g8f6', 'g1f3', 'd7d5', 'c2c4', 'c7c6', 'b1c3', 'd5c4', 'a2a4', 'c8f5', 'e2e3', 'e7e6', 'f1c4'], ['d2d4', 'g8f6', 'g1f3', 'd7d5', 'c2c4', 'c7c6', 'b1c3', 'e7e6', 'c1g5'], ['d2d4', 'g8f6', 'g1f3', 'd7d5', 'c2c4', 'c7c6', 'b1c3', 'e7e6', 'e2e3', 'b8d7', 'd1c2', 'f8d6'], ['d2d4', 'g8f6', 'g1f3', 'd7d5', 'c2c4', 'c7c6', 'b1c3', 'e7e6', 'e2e3', 'b8d7', 'f1d3', 'd5c4', 'd3c4', 'b7b5', 'c4d3'], ['d2d4', 'g8f6', 'g1f3', 'd7d5', 'c2c4', 'c7c6', 'e2e3'], ['d2d4', 'g8f6', 'g1f3', 'd7d5', 'c2c4', 'd5c4', 'e2e3', 'e7e6', 'f1c4', 'c7c5', 'e1g1', 'a7a6'], ['d2d4', 'g8f6', 'g1f3', 'd7d5', 'c2c4', 'e7e6', 'b1c3', 'b8d7'], ['d2d4', 'g8f6', 'g1f3', 'd7d5', 'c2c4', 'e7e6', 'b1c3', 'f8e7', 'c1f4', 'e8g8', 'e2e3'], ['d2d4', 'g8f6', 'g1f3', 'd7d5', 'c2c4', 'e7e6', 'b1c3', 'f8e7', 'c1g5', 'h7h6', 'g5h4', 'e8g8', 'e2e3', 'b7b6'], ['d2d4', 'g8f6', 'g1f3', 'd7d5', 'c2c4', 'e7e6', 'b1c3', 'f8e7', 'c1g5', 'e8g8', 'e2e3', 'h7h6'], ['d2d4', 'g8f6', 'g1f3', 'd7d5', 'c2c4', 'e7e6', 'b1c3', 'f8b4'], ['d2d4', 'g8f6', 'g1f3', 'd7d5', 'c2c4', 'e7e6', 'b1c3', 'c7c6', 'c1g5'], ['d2d4', 'g8f6', 'g1f3', 'd7d5', 'c2c4', 'e7e6', 'b1c3', 'c7c6', 'e2e3', 'b8d7', 'd1c2', 'f8d6'], ['d2d4', 'g8f6', 'g1f3', 'd7d5', 'c2c4', 'e7e6', 'b1c3', 'c7c6', 'e2e3', 'b8d7', 'f1d3', 'd5c4', 'd3c4', 'b7b5', 'c4d3'], ['d2d4', 'g8f6', 'g1f3', 'd7d5', 'c2c4', 'e7e6', 'b1c3', 'c7c5'], ['d2d4', 'g8f6', 'g1f3', 'd7d5', 'c2c4', 'e7e6', 'c1g5'], ['d2d4', 'g8f6', 'g1f3', 'd7d5', 'c2c4', 'e7e6', 'g2g3'], ['d2d4', 'g8f6', 'g1f3', 'e7e6', 'c1g5'], ['d2d4', 'g8f6', 'g1f3', 'e7e6', 'c2c4', 'f8b4', 'b1d2'], ['d2d4', 'g8f6', 'g1f3', 'e7e6', 'c2c4', 'f8b4', 'c1d2'], ['d2d4', 'g8f6', 'g1f3', 'e7e6', 'c2c4', 'b7b6', 'b1c3', 'c8b7', 'a2a3', 'd7d5', 'c4d5', 'f6d5'], ['d2d4', 'g8f6', 'g1f3', 'e7e6', 'c2c4', 'b7b6', 'b1c3', 'f8b4'], ['d2d4', 'g8f6', 'g1f3', 'e7e6', 'c2c4', 'b7b6', 'a2a3', 'c8b7', 'b1c3', 'd7d5', 'c4d5', 'f6d5'], ['d2d4', 'g8f6', 'g1f3', 'e7e6', 'c2c4', 'b7b6', 'g2g3', 'c8b7', 'f1g2', 'f8e7', 'e1g1', 'e8g8', 'b1c3', 'f6e4', 'd1c2', 'e4c3', 'c2c3'], ['d2d4', 'g8f6', 'g1f3', 'e7e6', 'c2c4', 'b7b6', 'g2g3', 'c8a6', 'b2b3', 'f8b4', 'c1d2', 'b4e7'], ['d2d4', 'g8f6', 'g1f3', 'e7e6', 'c2c4', 'c7c5', 'd4d5', 'e6d5', 'c4d5', 'd7d6', 'b1c3', 'g7g6'], ['d2d4', 'g8f6', 'g1f3', 'e7e6', 'c2c4', 'd7d5', 'b1c3', 'b8d7'], ['d2d4', 'g8f6', 'g1f3', 'e7e6', 'c2c4', 'd7d5', 'b1c3', 'f8e7', 'c1f4', 'e8g8', 'e2e3'], ['d2d4', 'g8f6', 'g1f3', 'e7e6', 'c2c4', 'd7d5', 'b1c3', 'f8e7', 'c1g5', 'h7h6', 'g5h4', 'e8g8', 'e2e3', 'b7b6'], ['d2d4', 'g8f6', 'g1f3', 'e7e6', 'c2c4', 'd7d5', 'b1c3', 'f8e7', 'c1g5', 'e8g8', 'e2e3', 'h7h6'], ['d2d4', 'g8f6', 'g1f3', 'e7e6', 'c2c4', 'd7d5', 'b1c3', 'f8b4'], ['d2d4', 'g8f6', 'g1f3', 'e7e6', 'c2c4', 'd7d5', 'b1c3', 'c7c6', 'c1g5'], ['d2d4', 'g8f6', 'g1f3', 'e7e6', 'c2c4', 'd7d5', 'b1c3', 'c7c6', 'e2e3', 'b8d7', 'd1c2', 'f8d6'], ['d2d4', 'g8f6', 'g1f3', 'e7e6', 'c2c4', 'd7d5', 'b1c3', 'c7c6', 'e2e3', 'b8d7', 'f1d3', 'd5c4', 'd3c4', 'b7b5', 'c4d3'], ['d2d4', 'g8f6', 'g1f3', 'e7e6', 'c2c4', 'd7d5', 'b1c3', 'c7c5'], ['d2d4', 'g8f6', 'g1f3', 'e7e6', 'c2c4', 'd7d5', 'c1g5'], ['d2d4', 'g8f6', 'g1f3', 'e7e6', 'c2c4', 'd7d5', 'g2g3'], ['d2d4', 'g8f6', 'g1f3', 'e7e6', 'g2g3'], ['d2d4', 'g8f6', 'g1f3', 'g7g6', 'c1g5'], ['d2d4', 'g8f6', 'g1f3', 'g7g6', 'c2c4', 'f8g7', 'b1c3', 'e8g8', 'e2e4', 'd7d6', 'f1e2', 'e7e5', 'e1g1', 'b8c6', 'd4d5', 'c6e7', 'f3e1', 'f6d7'], ['d2d4', 'g8f6', 'g1f3', 'g7g6', 'c2c4', 'f8g7', 'g2g3', 'e8g8', 'f1g2', 'd7d6', 'e1g1'], ['d2d4', 'g8f6', 'g1f3', 'g7g6', 'g2g3', 'f8g7', 'f1g2', 'e8g8'], ['d2d4', 'g8f6', 'c2c4', 'c7c5', 'd4d5', 'b7b5', 'c4b5', 'a7a6'], ['d2d4', 'g8f6', 'c2c4', 'c7c5', 'd4d5', 'e7e6', 'b1c3', 'e6d5', 'c4d5', 'd7d6'], ['d2d4', 'g8f6', 'c2c4', 'd7d6', 'b1c3'], ['d2d4', 'g8f6', 'c2c4', 'e7e6', 'b1c3', 'f8b4', 'd1c2', 'e8g8'], ['d2d4', 'g8f6', 'c2c4', 'e7e6', 'b1c3', 'f8b4', 'g1f3'], ['d2d4', 'g8f6', 'c2c4', 'e7e6', 'b1c3', 'f8b4', 'e2e3', 'b7b6'], ['d2d4', 'g8f6', 'c2c4', 'e7e6', 'b1c3', 'f8b4', 'e2e3', 'c7c5', 'f1d3'], ['d2d4', 'g8f6', 'c2c4', 'e7e6', 'b1c3', 'f8b4', 'e2e3', 'e8g8', 'f1d3', 'd7d5', 'g1f3'], ['d2d4', 'g8f6', 'c2c4', 'e7e6', 'b1c3', 'd7d5', 'c1g5', 'f8e7', 'e2e3'], ['d2d4', 'g8f6', 'c2c4', 'e7e6', 'b1c3', 'd7d5', 'g1f3', 'b8d7'], ['d2d4', 'g8f6', 'c2c4', 'e7e6', 'b1c3', 'd7d5', 'g1f3', 'f8e7', 'c1f4', 'e8g8', 'e2e3'], ['d2d4', 'g8f6', 'c2c4', 'e7e6', 'b1c3', 'd7d5', 'g1f3', 'f8e7', 'c1g5', 'h7h6', 'g5h4', 'e8g8', 'e2e3', 'b7b6'], ['d2d4', 'g8f6', 'c2c4', 'e7e6', 'b1c3', 'd7d5', 'g1f3', 'f8e7', 'c1g5', 'e8g8', 'e2e3', 'h7h6'], ['d2d4', 'g8f6', 'c2c4', 'e7e6', 'b1c3', 'd7d5', 'g1f3', 'f8b4'], ['d2d4', 'g8f6', 'c2c4', 'e7e6', 'b1c3', 'd7d5', 'g1f3', 'c7c6', 'c1g5'], ['d2d4', 'g8f6', 'c2c4', 'e7e6', 'b1c3', 'd7d5', 'g1f3', 'c7c6', 'e2e3', 'b8d7', 'd1c2', 'f8d6'], ['d2d4', 'g8f6', 'c2c4', 'e7e6', 'b1c3', 'd7d5', 'g1f3', 'c7c6', 'e2e3', 'b8d7', 'f1d3', 'd5c4', 'd3c4', 'b7b5', 'c4d3'], ['d2d4', 'g8f6', 'c2c4', 'e7e6', 'b1c3', 'd7d5', 'g1f3', 'c7c5'], ['d2d4', 'g8f6', 'c2c4', 'e7e6', 'b1c3', 'd7d5', 'c4d5', 'e6d5', 'c1g5'], ['d2d4', 'g8f6', 'c2c4', 'e7e6', 'g1f3', 'f8b4', 'b1d2'], ['d2d4', 'g8f6', 'c2c4', 'e7e6', 'g1f3', 'f8b4', 'c1d2'], ['d2d4', 'g8f6', 'c2c4', 'e7e6', 'g1f3', 'b7b6', 'b1c3', 'c8b7', 'a2a3', 'd7d5', 'c4d5', 'f6d5'], ['d2d4', 'g8f6', 'c2c4', 'e7e6', 'g1f3', 'b7b6', 'b1c3', 'f8b4'], ['d2d4', 'g8f6', 'c2c4', 'e7e6', 'g1f3', 'b7b6', 'a2a3', 'c8b7', 'b1c3', 'd7d5', 'c4d5', 'f6d5'], ['d2d4', 'g8f6', 'c2c4', 'e7e6', 'g1f3', 'b7b6', 'g2g3', 'c8b7', 'f1g2', 'f8e7', 'e1g1', 'e8g8', 'b1c3', 'f6e4', 'd1c2', 'e4c3', 'c2c3'], ['d2d4', 'g8f6', 'c2c4', 'e7e6', 'g1f3', 'b7b6', 'g2g3', 'c8a6', 'b2b3', 'f8b4', 'c1d2', 'b4e7'], ['d2d4', 'g8f6', 'c2c4', 'e7e6', 'g1f3', 'c7c5', 'd4d5', 'e6d5', 'c4d5', 'd7d6', 'b1c3', 'g7g6'], ['d2d4', 'g8f6', 'c2c4', 'e7e6', 'g1f3', 'd7d5', 'b1c3', 'b8d7'], ['d2d4', 'g8f6', 'c2c4', 'e7e6', 'g1f3', 'd7d5', 'b1c3', 'f8e7', 'c1f4', 'e8g8', 'e2e3'], ['d2d4', 'g8f6', 'c2c4', 'e7e6', 'g1f3', 'd7d5', 'b1c3', 'f8e7', 'c1g5', 'h7h6', 'g5h4', 'e8g8', 'e2e3', 'b7b6'], ['d2d4', 'g8f6', 'c2c4', 'e7e6', 'g1f3', 'd7d5', 'b1c3', 'f8e7', 'c1g5', 'e8g8', 'e2e3', 'h7h6'], ['d2d4', 'g8f6', 'c2c4', 'e7e6', 'g1f3', 'd7d5', 'b1c3', 'f8b4'], ['d2d4', 'g8f6', 'c2c4', 'e7e6', 'g1f3', 'd7d5', 'b1c3', 'c7c6', 'c1g5'], ['d2d4', 'g8f6', 'c2c4', 'e7e6', 'g1f3', 'd7d5', 'b1c3', 'c7c6', 'e2e3', 'b8d7', 'd1c2', 'f8d6'], ['d2d4', 'g8f6', 'c2c4', 'e7e6', 'g1f3', 'd7d5', 'b1c3', 'c7c6', 'e2e3', 'b8d7', 'f1d3', 'd5c4', 'd3c4', 'b7b5', 'c4d3'], ['d2d4', 'g8f6', 'c2c4', 'e7e6', 'g1f3', 'd7d5', 'b1c3', 'c7c5'], ['d2d4', 'g8f6', 'c2c4', 'e7e6', 'g1f3', 'd7d5', 'c1g5'], ['d2d4', 'g8f6', 'c2c4', 'e7e6', 'g1f3', 'd7d5', 'g2g3'], ['d2d4', 'g8f6', 'c2c4', 'e7e6', 'g2g3', 'd7d5', 'f1g2'], ['d2d4', 'g8f6', 'c2c4', 'g7g6', 'b1c3', 'f8g7', 'e2e4', 'd7d6', 'f1e2', 'e8g8', 'c1g5'], ['d2d4', 'g8f6', 'c2c4', 'g7g6', 'b1c3', 'f8g7', 'e2e4', 'd7d6', 'f1e2', 'e8g8', 'g1f3', 'e7e5', 'e1g1', 'b8c6', 'd4d5', 'c6e7', 'f3e1', 'f6d7'], ['d2d4', 'g8f6', 'c2c4', 'g7g6', 'b1c3', 'f8g7', 'e2e4', 'd7d6', 'g1f3', 'e8g8', 'f1e2', 'e7e5', 'e1g1', 'b8c6', 'd4d5', 'c6e7', 'f3e1', 'f6d7'], ['d2d4', 'g8f6', 'c2c4', 'g7g6', 'b1c3', 'f8g7', 'e2e4', 'd7d6', 'f2f3', 'e8g8', 'c1e3'], ['d2d4', 'g8f6', 'c2c4', 'g7g6', 'b1c3', 'd7d5', 'g1f3', 'f8g7', 'd1b3', 'd5c4', 'b3c4'], ['d2d4', 'g8f6', 'c2c4', 'g7g6', 'b1c3', 'd7d5', 'c4d5', 'f6d5', 'e2e4', 'd5c3', 'b2c3', 'f8g7', 'f1c4'], ['d2d4', 'g8f6', 'c2c4', 'g7g6', 'g1f3', 'f8g7', 'b1c3', 'e8g8', 'e2e4', 'd7d6', 'f1e2', 'e7e5', 'e1g1', 'b8c6', 'd4d5', 'c6e7', 'f3e1', 'f6d7'], ['d2d4', 'g8f6', 'c2c4', 'g7g6', 'g1f3', 'f8g7', 'g2g3', 'e8g8', 'f1g2', 'd7d6', 'e1g1'], ['d2d4', 'g8f6', 'c2c4', 'g7g6', 'g2g3', 'f8g7', 'f1g2', 'e8g8'], ['d2d4', 'd7d6', 'e2e4', 'g8f6', 'b1c3', 'g7g6', 'f2f4', 'f8g7', 'g1f3'], ['d2d4', 'd7d6', 'e2e4', 'g7g6'], ['d2d4', 'd7d5', 'g1f3', 'g8f6', 'c2c4', 'c7c6', 'b1c3', 'd5c4', 'a2a4', 'c8f5', 'e2e3', 'e7e6', 'f1c4'], ['d2d4', 'd7d5', 'g1f3', 'g8f6', 'c2c4', 'c7c6', 'b1c3', 'e7e6', 'c1g5'], ['d2d4', 'd7d5', 'g1f3', 'g8f6', 'c2c4', 'c7c6', 'b1c3', 'e7e6', 'e2e3', 'b8d7', 'd1c2', 'f8d6'], ['d2d4', 'd7d5', 'g1f3', 'g8f6', 'c2c4', 'c7c6', 'b1c3', 'e7e6', 'e2e3', 'b8d7', 'f1d3', 'd5c4', 'd3c4', 'b7b5', 'c4d3'], ['d2d4', 'd7d5', 'g1f3', 'g8f6', 'c2c4', 'c7c6', 'e2e3'], ['d2d4', 'd7d5', 'g1f3', 'g8f6', 'c2c4', 'd5c4', 'e2e3', 'e7e6', 'f1c4', 'c7c5', 'e1g1', 'a7a6'], ['d2d4', 'd7d5', 'g1f3', 'g8f6', 'c2c4', 'e7e6', 'b1c3', 'b8d7'], ['d2d4', 'd7d5', 'g1f3', 'g8f6', 'c2c4', 'e7e6', 'b1c3', 'f8e7', 'c1f4', 'e8g8', 'e2e3'], ['d2d4', 'd7d5', 'g1f3', 'g8f6', 'c2c4', 'e7e6', 'b1c3', 'f8e7', 'c1g5', 'h7h6', 'g5h4', 'e8g8', 'e2e3', 'b7b6'], ['d2d4', 'd7d5', 'g1f3', 'g8f6', 'c2c4', 'e7e6', 'b1c3', 'f8e7', 'c1g5', 'e8g8', 'e2e3', 'h7h6'], ['d2d4', 'd7d5', 'g1f3', 'g8f6', 'c2c4', 'e7e6', 'b1c3', 'f8b4'], ['d2d4', 'd7d5', 'g1f3', 'g8f6', 'c2c4', 'e7e6', 'b1c3', 'c7c6', 'c1g5'], ['d2d4', 'd7d5', 'g1f3', 'g8f6', 'c2c4', 'e7e6', 'b1c3', 'c7c6', 'e2e3', 'b8d7', 'd1c2', 'f8d6'], ['d2d4', 'd7d5', 'g1f3', 'g8f6', 'c2c4', 'e7e6', 'b1c3', 'c7c6', 'e2e3', 'b8d7', 'f1d3', 'd5c4', 'd3c4', 'b7b5', 'c4d3'], ['d2d4', 'd7d5', 'g1f3', 'g8f6', 'c2c4', 'e7e6', 'b1c3', 'c7c5'], ['d2d4', 'd7d5', 'g1f3', 'g8f6', 'c2c4', 'e7e6', 'c1g5'], ['d2d4', 'd7d5', 'g1f3', 'g8f6', 'c2c4', 'e7e6', 'g2g3'], ['d2d4', 'd7d5', 'c2c4', 'c7c6', 'b1c3', 'g8f6', 'g1f3', 'd5c4', 'a2a4', 'c8f5', 'e2e3', 'e7e6', 'f1c4'], ['d2d4', 'd7d5', 'c2c4', 'c7c6', 'b1c3', 'g8f6', 'g1f3', 'e7e6', 'c1g5'], ['d2d4', 'd7d5', 'c2c4', 'c7c6', 'b1c3', 'g8f6', 'g1f3', 'e7e6', 'e2e3', 'b8d7', 'd1c2', 'f8d6'], ['d2d4',
        'd7d5', 'c2c4', 'c7c6', 'b1c3', 'g8f6', 'g1f3', 'e7e6', 'e2e3', 'b8d7', 'f1d3', 'd5c4', 'd3c4', 'b7b5', 'c4d3'], ['d2d4', 'd7d5', 'c2c4', 'c7c6', 'b1c3', 'g8f6', 'e2e3'], ['d2d4', 'd7d5', 'c2c4', 'c7c6', 'g1f3', 'g8f6', 'b1c3', 'd5c4', 'a2a4', 'c8f5', 'e2e3', 'e7e6', 'f1c4'], ['d2d4', 'd7d5', 'c2c4', 'c7c6', 'g1f3', 'g8f6', 'b1c3', 'e7e6', 'c1g5'], ['d2d4', 'd7d5', 'c2c4', 'c7c6', 'g1f3', 'g8f6', 'b1c3', 'e7e6', 'e2e3', 'b8d7', 'd1c2', 'f8d6'], ['d2d4', 'd7d5', 'c2c4', 'c7c6', 'g1f3', 'g8f6', 'b1c3', 'e7e6', 'e2e3', 'b8d7', 'f1d3', 'd5c4', 'd3c4', 'b7b5', 'c4d3'], ['d2d4', 'd7d5', 'c2c4', 'c7c6', 'g1f3', 'g8f6', 'e2e3'], ['d2d4', 'd7d5', 'c2c4', 'd5c4', 'g1f3', 'g8f6', 'e2e3', 'e7e6', 'f1c4', 'c7c5', 'e1g1', 'a7a6'], ['d2d4', 'd7d5', 'c2c4', 'e7e6', 'b1c3', 'f8e7', 'g1f3', 'g8f6', 'c1f4', 'e8g8', 'e2e3'], ['d2d4', 'd7d5', 'c2c4', 'e7e6', 'b1c3', 'f8e7', 'g1f3', 'g8f6', 'c1g5', 'h7h6', 'g5h4', 'e8g8', 'e2e3', 'b7b6'], ['d2d4', 'd7d5', 'c2c4', 'e7e6', 'b1c3', 'f8e7', 'g1f3', 'g8f6', 'c1g5', 'e8g8', 'e2e3', 'h7h6'], ['d2d4', 'd7d5', 'c2c4', 'e7e6', 'b1c3', 'g8f6', 'c1g5', 'f8e7', 'e2e3'], ['d2d4', 'd7d5', 'c2c4', 'e7e6', 'b1c3', 'g8f6', 'g1f3', 'b8d7'], ['d2d4', 'd7d5', 'c2c4', 'e7e6', 'b1c3', 'g8f6', 'g1f3', 'f8e7', 'c1f4', 'e8g8', 'e2e3'], ['d2d4', 'd7d5', 'c2c4', 'e7e6', 'b1c3', 'g8f6', 'g1f3', 'f8e7', 'c1g5', 'h7h6', 'g5h4', 'e8g8', 'e2e3', 'b7b6'], ['d2d4', 'd7d5', 'c2c4', 'e7e6', 'b1c3', 'g8f6', 'g1f3', 'f8e7', 'c1g5', 'e8g8', 'e2e3', 'h7h6'], ['d2d4', 'd7d5', 'c2c4', 'e7e6', 'b1c3', 'g8f6', 'g1f3', 'f8b4'], ['d2d4', 'd7d5', 'c2c4', 'e7e6', 'b1c3', 'g8f6', 'g1f3', 'c7c6', 'c1g5'], ['d2d4', 'd7d5', 'c2c4', 'e7e6', 'b1c3', 'g8f6', 'g1f3', 'c7c6', 'e2e3', 'b8d7', 'd1c2', 'f8d6'], ['d2d4', 'd7d5', 'c2c4', 'e7e6', 'b1c3', 'g8f6', 'g1f3', 'c7c6', 'e2e3', 'b8d7', 'f1d3', 'd5c4', 'd3c4', 'b7b5', 'c4d3'], ['d2d4', 'd7d5', 'c2c4', 'e7e6', 'b1c3', 'g8f6', 'g1f3', 'c7c5'], ['d2d4', 'd7d5', 'c2c4', 'e7e6', 'b1c3', 'g8f6', 'c4d5', 'e6d5', 'c1g5'], ['d2d4', 'd7d5', 'c2c4', 'e7e6', 'b1c3', 'c7c6'], ['d2d4', 'd7d5', 'c2c4', 'e7e6', 'g1f3', 'g8f6', 'b1c3', 'b8d7'], ['d2d4', 'd7d5', 'c2c4', 'e7e6', 'g1f3', 'g8f6', 'b1c3', 'f8e7', 'c1f4', 'e8g8', 'e2e3'], ['d2d4', 'd7d5', 'c2c4', 'e7e6', 'g1f3', 'g8f6', 'b1c3', 'f8e7', 'c1g5', 'h7h6', 'g5h4', 'e8g8', 'e2e3', 'b7b6'], ['d2d4', 'd7d5', 'c2c4', 'e7e6', 'g1f3', 'g8f6', 'b1c3', 'f8e7', 'c1g5', 'e8g8', 'e2e3', 'h7h6'], ['d2d4', 'd7d5', 'c2c4', 'e7e6', 'g1f3', 'g8f6', 'b1c3', 'f8b4'], ['d2d4', 'd7d5', 'c2c4', 'e7e6', 'g1f3', 'g8f6', 'b1c3', 'c7c6', 'c1g5'], ['d2d4', 'd7d5', 'c2c4', 'e7e6', 'g1f3', 'g8f6', 'b1c3', 'c7c6', 'e2e3', 'b8d7', 'd1c2', 'f8d6'], ['d2d4', 'd7d5', 'c2c4', 'e7e6', 'g1f3', 'g8f6', 'b1c3', 'c7c6', 'e2e3', 'b8d7', 'f1d3', 'd5c4', 'd3c4', 'b7b5', 'c4d3'], ['d2d4', 'd7d5', 'c2c4', 'e7e6', 'g1f3', 'g8f6', 'b1c3', 'c7c5'], ['d2d4', 'd7d5', 'c2c4', 'e7e6', 'g1f3', 'g8f6', 'c1g5'], ['d2d4', 'd7d5', 'c2c4', 'e7e6', 'g1f3', 'g8f6', 'g2g3'], ['d2d4', 'e7e6', 'c2c4', 'g8f6', 'b1c3', 'f8b4', 'd1c2', 'e8g8'], ['d2d4', 'e7e6', 'c2c4', 'g8f6', 'b1c3', 'f8b4', 'g1f3'], ['d2d4', 'e7e6', 'c2c4', 'g8f6', 'b1c3', 'f8b4', 'e2e3', 'b7b6'], ['d2d4', 'e7e6', 'c2c4', 'g8f6', 'b1c3', 'f8b4', 'e2e3', 'c7c5', 'f1d3'], ['d2d4', 'e7e6', 'c2c4', 'g8f6', 'b1c3', 'f8b4', 'e2e3', 'e8g8', 'f1d3', 'd7d5', 'g1f3'], ['d2d4', 'e7e6', 'c2c4', 'g8f6', 'b1c3', 'd7d5', 'c1g5', 'f8e7', 'e2e3'], ['d2d4', 'e7e6', 'c2c4', 'g8f6', 'b1c3', 'd7d5', 'g1f3', 'b8d7'], ['d2d4', 'e7e6', 'c2c4', 'g8f6', 'b1c3', 'd7d5', 'g1f3', 'f8e7', 'c1f4', 'e8g8', 'e2e3'], ['d2d4', 'e7e6', 'c2c4', 'g8f6', 'b1c3', 'd7d5', 'g1f3', 'f8e7', 'c1g5', 'h7h6', 'g5h4', 'e8g8', 'e2e3', 'b7b6'], ['d2d4', 'e7e6', 'c2c4', 'g8f6', 'b1c3', 'd7d5', 'g1f3', 'f8e7', 'c1g5', 'e8g8', 'e2e3', 'h7h6'], ['d2d4', 'e7e6', 'c2c4', 'g8f6', 'b1c3', 'd7d5', 'g1f3', 'f8b4'], ['d2d4', 'e7e6', 'c2c4', 'g8f6', 'b1c3', 'd7d5', 'g1f3', 'c7c6', 'c1g5'], ['d2d4', 'e7e6', 'c2c4', 'g8f6', 'b1c3', 'd7d5', 'g1f3', 'c7c6', 'e2e3', 'b8d7', 'd1c2', 'f8d6'], ['d2d4', 'e7e6', 'c2c4', 'g8f6', 'b1c3', 'd7d5', 'g1f3', 'c7c6', 'e2e3', 'b8d7', 'f1d3', 'd5c4', 'd3c4', 'b7b5', 'c4d3'], ['d2d4', 'e7e6', 'c2c4', 'g8f6', 'b1c3', 'd7d5', 'g1f3', 'c7c5'], ['d2d4', 'e7e6', 'c2c4', 'g8f6', 'b1c3', 'd7d5', 'c4d5', 'e6d5', 'c1g5'], ['d2d4', 'e7e6', 'c2c4', 'g8f6', 'g1f3', 'f8b4', 'b1d2'], ['d2d4', 'e7e6', 'c2c4', 'g8f6', 'g1f3', 'f8b4', 'c1d2'], ['d2d4', 'e7e6', 'c2c4', 'g8f6', 'g1f3', 'b7b6', 'b1c3', 'c8b7', 'a2a3', 'd7d5', 'c4d5', 'f6d5'], ['d2d4', 'e7e6', 'c2c4', 'g8f6', 'g1f3', 'b7b6', 'b1c3', 'f8b4'], ['d2d4', 'e7e6', 'c2c4', 'g8f6', 'g1f3', 'b7b6', 'a2a3', 'c8b7', 'b1c3', 'd7d5', 'c4d5', 'f6d5'], ['d2d4', 'e7e6', 'c2c4', 'g8f6', 'g1f3', 'b7b6', 'g2g3', 'c8b7', 'f1g2', 'f8e7', 'e1g1', 'e8g8', 'b1c3', 'f6e4', 'd1c2', 'e4c3', 'c2c3'], ['d2d4', 'e7e6', 'c2c4', 'g8f6', 'g1f3', 'b7b6', 'g2g3', 'c8a6', 'b2b3', 'f8b4', 'c1d2', 'b4e7'], ['d2d4', 'e7e6', 'c2c4', 'g8f6', 'g1f3', 'c7c5', 'd4d5', 'e6d5', 'c4d5', 'd7d6', 'b1c3', 'g7g6'], ['d2d4', 'e7e6', 'c2c4', 'g8f6', 'g1f3', 'd7d5', 'b1c3', 'b8d7'], ['d2d4', 'e7e6', 'c2c4', 'g8f6', 'g1f3', 'd7d5', 'b1c3', 'f8e7', 'c1f4', 'e8g8', 'e2e3'], ['d2d4', 'e7e6', 'c2c4', 'g8f6', 'g1f3', 'd7d5', 'b1c3', 'f8e7', 'c1g5', 'h7h6', 'g5h4', 'e8g8', 'e2e3', 'b7b6'], ['d2d4', 'e7e6', 'c2c4', 'g8f6', 'g1f3', 'd7d5', 'b1c3', 'f8e7', 'c1g5', 'e8g8', 'e2e3', 'h7h6'], ['d2d4', 'e7e6', 'c2c4', 'g8f6', 'g1f3', 'd7d5', 'b1c3', 'f8b4'], ['d2d4', 'e7e6', 'c2c4', 'g8f6', 'g1f3', 'd7d5', 'b1c3', 'c7c6', 'c1g5'], ['d2d4', 'e7e6', 'c2c4', 'g8f6', 'g1f3', 'd7d5', 'b1c3', 'c7c6', 'e2e3', 'b8d7', 'd1c2', 'f8d6'], ['d2d4', 'e7e6', 'c2c4', 'g8f6', 'g1f3', 'd7d5', 'b1c3', 'c7c6', 'e2e3', 'b8d7', 'f1d3', 'd5c4', 'd3c4', 'b7b5', 'c4d3'], ['d2d4', 'e7e6', 'c2c4', 'g8f6', 'g1f3', 'd7d5', 'b1c3', 'c7c5'], ['d2d4', 'e7e6', 'c2c4', 'g8f6', 'g1f3', 'd7d5', 'c1g5'], ['d2d4', 'e7e6', 'c2c4', 'g8f6', 'g1f3', 'd7d5', 'g2g3'], ['d2d4', 'e7e6', 'c2c4', 'g8f6', 'g2g3', 'd7d5', 'f1g2'], ['d2d4', 'f7f5'], ['d2d4', 'g7g6'], ['e2e4', 'g8f6', 'e4e5', 'f6d5', 'd2d4', 'd7d6', 'g1f3'], ['e2e4', 'c7c6', 'd2d4', 'd7d5', 'b1c3', 'd5e4', 'c3e4', 'b8d7'], ['e2e4', 'c7c6', 'd2d4', 'd7d5', 'b1c3', 'd5e4', 'c3e4', 'c8f5', 'e4g3', 'f5g6', 'h2h4', 'h7h6'], ['e2e4', 'c7c6', 'd2d4', 'd7d5', 'b1d2', 'd5e4', 'd2e4', 'b8d7'], ['e2e4', 'c7c6', 'd2d4', 'd7d5', 'b1d2', 'd5e4', 'd2e4', 'c8f5', 'e4g3', 'f5g6', 'h2h4', 'h7h6'], ['e2e4', 'c7c6', 'd2d4', 'd7d5', 'e4d5', 'c6d5', 'c2c4', 'g8f6', 'b1c3', 'e7e6', 'g1f3'], ['e2e4', 'c7c6', 'd2d4', 'd7d5', 'e4e5', 'c8f5'], ['e2e4', 'c7c5', 'b1c3', 'b8c6', 'g2g3', 'g7g6', 'f1g2', 'f8g7'], ['e2e4', 'c7c5', 'g1f3', 'b8c6', 'f1b5'], ['e2e4', 'c7c5', 'g1f3', 'b8c6', 'd2d4', 'c5d4', 'f3d4', 'g8f6', 'b1c3', 'd7d6', 'c1g5', 'e7e6', 'd1d2', 'f8e7', 'e1c1', 'e8g8'], ['e2e4', 'c7c5', 'g1f3', 'b8c6', 'd2d4', 'c5d4', 'f3d4', 'g8f6', 'b1c3', 'd7d6', 'c1g5', 'e7e6', 'd1d2', 'a7a6', 'e1c1', 'h7h6'], ['e2e4', 'c7c5', 'g1f3', 'b8c6', 'd2d4', 'c5d4', 'f3d4', 'g8f6', 'b1c3', 'd7d6', 'f1c4'], ['e2e4', 'c7c5', 'g1f3', 'b8c6', 'd2d4', 'c5d4', 'f3d4', 'g8f6', 'b1c3', 'e7e5', 'd4b5', 'd7d6'], ['e2e4', 'c7c5', 'g1f3', 'b8c6', 'd2d4', 'c5d4', 'f3d4', 'e7e6', 'b1c3', 'd8c7'], ['e2e4', 'c7c5', 'g1f3', 'b8c6', 'd2d4', 'c5d4', 'f3d4', 'e7e6', 'b1c3', 'a7a6'], ['e2e4', 'c7c5', 'g1f3', 'b8c6', 'd2d4', 'c5d4', 'f3d4', 'g7g6'], ['e2e4', 'c7c5', 'g1f3', 'd7d6', 'f1b5'], ['e2e4', 'c7c5', 'g1f3', 'd7d6', 'd2d4', 'c5d4', 'f3d4', 'g8f6', 'b1c3', 'b8c6', 'c1g5', 'e7e6', 'd1d2', 'f8e7', 'e1c1', 'e8g8'], ['e2e4', 'c7c5', 'g1f3', 'd7d6', 'd2d4', 'c5d4', 'f3d4', 'g8f6', 'b1c3', 'b8c6', 'c1g5', 'e7e6', 'd1d2', 'a7a6', 'e1c1', 'h7h6'], ['e2e4', 'c7c5', 'g1f3', 'd7d6', 'd2d4', 'c5d4', 'f3d4', 'g8f6', 'b1c3', 'b8c6', 'f1c4'], ['e2e4', 'c7c5', 'g1f3', 'd7d6', 'd2d4', 'c5d4', 'f3d4', 'g8f6', 'b1c3', 'a7a6', 'c1e3'], ['e2e4', 'c7c5', 'g1f3', 'd7d6', 'd2d4', 'c5d4', 'f3d4', 'g8f6', 'b1c3', 'a7a6', 'c1g5', 'e7e6', 'f2f4'], ['e2e4', 'c7c5', 'g1f3', 'd7d6', 'd2d4', 'c5d4', 'f3d4', 'g8f6', 'b1c3', 'a7a6', 'f1e2', 'e7e5', 'd4b3', 'f8e7'], ['e2e4', 'c7c5', 'g1f3', 'd7d6', 'd2d4', 'c5d4', 'f3d4', 'g8f6', 'b1c3', 'a7a6', 'f2f4'], ['e2e4', 'c7c5', 'g1f3', 'd7d6', 'd2d4', 'c5d4', 'f3d4', 'g8f6', 'b1c3', 'e7e6', 'f1e2'], ['e2e4', 'c7c5', 'g1f3', 'd7d6', 'd2d4', 'c5d4', 'f3d4', 'g8f6', 'b1c3', 'e7e6', 'g2g4'], ['e2e4', 'c7c5', 'g1f3', 'd7d6', 'd2d4', 'c5d4', 'f3d4', 'g8f6', 'b1c3', 'g7g6', 'c1e3', 'f8g7', 'f2f3'], ['e2e4', 'c7c5', 'g1f3', 'e7e6', 'b1c3'], ['e2e4', 'c7c5', 'g1f3', 'e7e6', 'd2d4', 'c5d4', 'f3d4', 'b8c6', 'b1c3', 'd8c7'], ['e2e4', 'c7c5', 'g1f3', 'e7e6', 'd2d4', 'c5d4', 'f3d4', 'b8c6', 'b1c3', 'a7a6'], ['e2e4', 'c7c5', 'g1f3', 'e7e6', 'd2d4', 'c5d4', 'f3d4', 'g8f6', 'b1c3', 'd7d6', 'f1e2'], ['e2e4', 'c7c5', 'g1f3', 'e7e6', 'd2d4', 'c5d4', 'f3d4', 'g8f6', 'b1c3', 'd7d6', 'g2g4'], ['e2e4', 'c7c5', 'g1f3', 'e7e6', 'd2d4', 'c5d4', 'f3d4', 'a7a6', 'f1d3'], ['e2e4', 'c7c5', 'c2c3'], ['e2e4', 'd7d6', 'd2d4', 'g8f6', 'b1c3', 'g7g6', 'f2f4', 'f8g7', 'g1f3'], ['e2e4', 'd7d6', 'd2d4', 'g7g6'], ['e2e4', 'd7d5', 'e4d5'], ['e2e4', 'e7e6', 'd2d4', 'd7d5', 'b1c3', 'f8b4', 'e4e5', 'c7c5', 'a2a3', 'b4c3', 'b2c3', 'g8e7'], ['e2e4', 'e7e6', 'd2d4', 'd7d5', 'b1c3', 'g8f6', 'c1g5'], ['e2e4', 'e7e6', 'd2d4', 'd7d5', 'b1d2', 'g8f6', 'e4e5'], ['e2e4', 'e7e6', 'd2d4', 'd7d5', 'b1d2', 'c7c5', 'g1f3'], ['e2e4', 'e7e6', 'd2d4', 'd7d5', 'b1d2', 'c7c5', 'e4d5', 'e6d5'], ['e2e4', 'e7e6', 'd2d4', 'd7d5', 'e4e5', 'c7c5', 'c2c3', 'b8c6', 'g1f3'], ['e2e4', 'e7e5', 'b1c3'], ['e2e4', 'e7e5', 'g1f3', 'b8c6', 'b1c3', 'g8f6', 'f1b5'], ['e2e4', 'e7e5', 'g1f3', 'b8c6', 'f1c4', 'f8c5'], ['e2e4', 'e7e5', 'g1f3', 'b8c6', 'f1c4', 'g8f6'], ['e2e4', 'e7e5', 'g1f3', 'b8c6', 'f1b5', 'g8f6', 'e1g1'], ['e2e4', 'e7e5', 'g1f3', 'b8c6', 'f1b5', 'a7a6', 'b5c6', 'd7c6', 'e1g1'], ['e2e4', 'e7e5', 'g1f3', 'b8c6', 'f1b5', 'a7a6', 'b5a4', 'g8f6', 'e1g1', 'f8e7', 'f1e1', 'b7b5', 'a4b3', 'd7d6', 'c2c3', 'e8g8', 'h2h3', 'c6b8', 'd2d4', 'b8d7'], ['e2e4', 'e7e5', 'g1f3', 'b8c6', 'f1b5', 'a7a6', 'b5a4', 'g8f6', 'e1g1', 'f8e7', 'f1e1', 'b7b5', 'a4b3', 'd7d6', 'c2c3', 'e8g8', 'h2h3', 'c6a5',
        'b3c2', 'c7c5', 'd2d4', 'd8c7', 'b1d2'], ['e2e4', 'e7e5', 'g1f3', 'b8c6', 'f1b5', 'a7a6', 'b5a4', 'g8f6', 'e1g1', 'f8e7', 'f1e1', 'b7b5', 'a4b3', 'd7d6', 'c2c3', 'e8g8', 'h2h3', 'c8b7', 'd2d4', 'f8e8'], ['e2e4', 'e7e5', 'g1f3', 'b8c6', 'f1b5', 'a7a6', 'b5a4', 'g8f6', 'e1g1', 'f8e7', 'f1e1', 'b7b5', 'a4b3', 'e8g8', 'c2c3', 'd7d6', 'h2h3', 'c6b8', 'd2d4', 'b8d7'], ['e2e4', 'e7e5', 'g1f3', 'b8c6', 'f1b5', 'a7a6', 'b5a4', 'g8f6', 'e1g1', 'f8e7', 'f1e1', 'b7b5', 'a4b3', 'e8g8', 'c2c3', 'd7d6', 'h2h3', 'c6a5', 'b3c2', 'c7c5', 'd2d4', 'd8c7', 'b1d2'], ['e2e4', 'e7e5', 'g1f3', 'b8c6', 'f1b5', 'a7a6', 'b5a4', 'g8f6', 'e1g1', 'f8e7', 'f1e1', 'b7b5', 'a4b3', 'e8g8', 'c2c3', 'd7d6', 'h2h3', 'c8b7', 'd2d4', 'f8e8'], ['e2e4', 'e7e5', 'g1f3', 'b8c6', 'f1b5', 'a7a6', 'b5a4', 'g8f6', 'e1g1', 'f6e4', 'd2d4', 'b7b5', 'a4b3', 'd7d5', 'd4e5', 'c8e6', 'c2c3'], ['e2e4', 'e7e5', 'g1f3', 'b8c6', 'f1b5', 'a7a6', 'b5a4', 'd7d6'], ['e2e4', 'e7e5', 'g1f3', 'b8c6', 'd2d4', 'e5d4', 'f3d4'], ['e2e4', 'e7e5', 'g1f3', 'g8f6', 'f3e5', 'd7d6', 'e5f3', 'f6e4', 'd2d4'], ['e2e4', 'e7e5', 'f2f4'], ['e2e4', 'g7g6', 'd2d4', 'f8g7', 'b1c3', 'd7d6'], ['g2g3']]

        book = [[[chess.Board().fen(), 'e2e4']]]
        for openning in tscp_op :
            board = chess.Board()
            Openning = []
            for move in openning :
                board.push(chess.Move.from_uci(move))
                a = board.fen()
                try :
                    Move = openning[openning.index(move)+1]
                except Exception :
                    Move = None
                Openning.append([a, Move])
            book.append(Openning)

        liste = []
        for start in book :
            for couple in start :
                if self.is_equivalent(couple[0], board):
                    liste.append(couple[1])
        try :
            return random.choice(liste)
        except Exception :
            return None

    def search(self, board, *args):
        move = self.move_from_book(board)
        if move != None:
            return move 
        else:
            return self.minimax_root(3, board)