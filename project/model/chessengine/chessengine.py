

import logging
#from PySide2 import QtCore, QtWidgets
import time

#import model.chessengine.negamax as negamax
from . import negamax
from . import chessboard
#from .chesspieces import Pawn

logger = logging.getLogger(__name__)


piece_type = {chessboard.W_PAWN: 'pawn', chessboard.B_PAWN: 'pawn',
                chessboard.W_ROOK: 'rook', chessboard.B_ROOK: 'rook',
                chessboard.W_KNIGHT: 'knight', chessboard.B_KNIGHT: 'knight',
                chessboard.W_BISHOP: 'bishop', chessboard.B_BISHOP: 'bishop',
                chessboard.W_QUEEN: 'queen', chessboard.B_QUEEN: 'queen',
                chessboard.W_KING: 'king', chessboard.B_KING: 'king'}

class ChessEngine(object):

    # TD DO

    # Cleanup stuff. Consider structure of ChessBoard contra ChessEngine. Where should methods exist?
    # Fix the signalling of the current_board_representation (below) and the corresponding actions in
    # the view. Also a signal for choosing new piece when pawn converts should be implemented.

    # The evaluation function does not see the virtue of winning! It usually just draws games. A small rething
    # in that department is required.

    # A evaluation method based on only the attack_tables is really interesting. Something like, 1 point for every
    # attacked square, possibly bonus for multiple attacks, and I'm guessing a big bonus for squares which are
    # attacked more times than the opponent! This could lead to some interesting choices made by the engine!!!

    def __init__(self, parameters=None):
        super(ChessEngine, self).__init__()

        self.parameters = parameters

        self.depth = 3

        self.chessboard = chessboard.ChessBoard()

        self.game_history = []
        self.game_history.append(self.chessboard)

        self.extra_move_on_screen = None
        self.square_to_clear = None


    def current_board_representation(self):

        # Fix this. The following shall be sent to the view:
        # last_move, piece_representation, chess_flags, win_flags, draw_flags

        all_chessboard_positions = range(64)

        piece_representation = {}   # [(position, type, color), ]
        chess_flags_representation = (False, False)

        for position in all_chessboard_positions:
            piece = self.chessboard.get_piece(position)
            if piece != chessboard.NONE:
                if self.chessboard.get_color(position) == chessboard.WHITE:
                    color = 'white'
                else:
                    color = 'black'
                piece_representation[self.numeric_to_letter_position(position)] = (piece_type[piece], color)

        board_representation = (piece_representation, chess_flags_representation)
        return board_representation

    
    def get_next_move(self, literal_color):

        playing_color = self.literal_to_numeric_color(literal_color)
        
        moves_and_corresponding_nodes = self.chessboard.all_legal_moves_and_corresponding_boards(playing_color)

        idmemscore, principal_variation = negamax.iterativedeepeningalphabetamemory(self.chessboard, self.depth, playing_color)

        #if len(principal_variation) == 1:
        #    print('GAME OVER')

        self.chessboard = principal_variation[1]
        
        for move, node in moves_and_corresponding_nodes.items():
            if node.zobrist_number == principal_variation[1].zobrist_number:
                actual_move_made = move

        return self.numeric_to_letter_move(actual_move_made)





    def register_move(self, letter_move):

        numeric_move = self.letter_to_numeric_move(letter_move)

        self.chessboard.execute(numeric_move)

        self.game_history.append(self.chessboard)

        self.chessboard.draw()

        flagline = 'En passant flags: '
        for f in range(8):
            flagline += str(self.chessboard.en_passant_flag(f))

        flagline += '   Castling flags (wq, wk, bq, bk): ' 
                
        if self.chessboard.castling_queen_side_flag(chessboard.WHITE):
            flagline += '1'
        else:
            flagline += '0'
                
        if self.chessboard.castling_king_side_flag(chessboard.WHITE):
            flagline += '1'
        else:
            flagline += '0'
                   
        if self.chessboard.castling_queen_side_flag(chessboard.BLACK):
            flagline += '1'
        else:
            flagline += '0'

        if self.chessboard.castling_king_side_flag(chessboard.BLACK):
            flagline += '1'
        else:
            flagline += '0'
                    

        print(flagline)
                
        print('')



    def literal_to_numeric_color(self, literal_color):
        if literal_color == 'white':
            return chessboard.WHITE
        else:
            return chessboard.BLACK
    
    def numeric_to_literal_color(self, numeric_color):
        if numeric_color == chessboard.WHITE:
             return 'white'
        else:
            return 'black'


    def king_is_under_attack(self, literal_color):
        return self.chessboard.king_is_under_attack(self.literal_to_numeric_color(literal_color))

    def get_all_allowed_moves(self, literal_color):

        numeric_color = self.literal_to_numeric_color(literal_color)

        self.moves_and_corresponding_boards = self.chessboard.all_legal_moves_and_corresponding_boards(numeric_color)

        allowed_numeric_moves = list(self.moves_and_corresponding_boards.keys())

        allowed_letter_moves = list(map(self.numeric_to_letter_move, allowed_numeric_moves))

        return allowed_letter_moves


    def numeric_to_letter_move(self, numeric_move):
        from_position, to_position = numeric_move
        return '-'.join((self.numeric_to_letter_position(from_position), self.numeric_to_letter_position(to_position)))


    def letter_to_numeric_move(self, letter_move):
        return (self.letter_to_numeric_position(letter_move[:2]), self.letter_to_numeric_position(letter_move[3:]))


    def numeric_to_letter_position(self, numeric_position):
        letters = ('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h')
        numbers = ('8', '7', '6', '5', '4', '3', '2', '1')
        return ''.join((letters[numeric_position % 8], numbers[numeric_position // 8]))


    def letter_to_numeric_position(self, letter_position):
        return ord(letter_position[0]) - ord('a') + (7 - ord(letter_position[1]) + ord('1')) * 8