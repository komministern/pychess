#!/usr/bin/env python
# -*- coding: utf-8 -*-

#import time
#import copy, array #, random

#from chesspieces import Pawn, Rook, Knight, Bishop, Queen, King

#import zobrist

import numpy as np
import time
import copy, array #, random

from . import zobrist

from . import evaluation

from .chesspieces import Pawn, Rook, Knight, Bishop, Queen, King



WHITE = 1
BLACK = -1

# pieces

NONE = 0

W_PAWN = 1      # 0b0001
W_ROOK = 2      # 0b0010
W_KNIGHT = 3
W_BISHOP = 4
W_QUEEN = 5
W_KING = 6      # 0b0110

WHITE_BLACK_SEPARATOR = 7

B_PAWN = 9      # 0b1001
B_ROOK = 10     # 0b1010
B_KNIGHT = 11
B_BISHOP = 12
B_QUEEN = 13
B_KING = 14     # 0b1110

# piece-class

PIECECLASSES = {W_PAWN: Pawn, B_PAWN: Pawn,
                W_ROOK: Rook, B_ROOK: Rook,
                W_KNIGHT: Knight, B_KNIGHT: Knight,
                W_BISHOP: Bishop, B_BISHOP: Bishop,
                W_QUEEN: Queen, B_QUEEN: Queen,
                W_KING: King, B_KING: King, NONE: None}

# vectors

E = 1
W = -1
S = 8
N = -8

NE = N+E
SE = S+E
NW = N+W
SW = S+W

# board positions

a8 = 0*8 + 0
b8 = 0*8 + 1
c8 = 0*8 + 2
d8 = 0*8 + 3
e8 = 0*8 + 4
f8 = 0*8 + 5
g8 = 0*8 + 6
h8 = 0*8 + 7

a7 = 1*8 + 0
b7 = 1*8 + 1
c7 = 1*8 + 2
d7 = 1*8 + 3
e7 = 1*8 + 4
f7 = 1*8 + 5
g7 = 1*8 + 6
h7 = 1*8 + 7

a6 = 2*8 + 0
b6 = 2*8 + 1
c6 = 2*8 + 2
d6 = 2*8 + 3
e6 = 2*8 + 4
f6 = 2*8 + 5
g6 = 2*8 + 6
h6 = 2*8 + 7

a5 = 3*8 + 0
b5 = 3*8 + 1
c5 = 3*8 + 2
d5 = 3*8 + 3
e5 = 3*8 + 4
f5 = 3*8 + 5
g5 = 3*8 + 6
h5 = 3*8 + 7

a4 = 4*8 + 0
b4 = 4*8 + 1
c4 = 4*8 + 2
d4 = 4*8 + 3
e4 = 4*8 + 4
f4 = 4*8 + 5
g4 = 4*8 + 6
h4 = 4*8 + 7

a3 = 5*8 + 0
b3 = 5*8 + 1
c3 = 5*8 + 2
d3 = 5*8 + 3
e3 = 5*8 + 4
f3 = 5*8 + 5
g3 = 5*8 + 6
h3 = 5*8 + 7

a2 = 6*8 + 0
b2 = 6*8 + 1
c2 = 6*8 + 2
d2 = 6*8 + 3
e2 = 6*8 + 4
f2 = 6*8 + 5
g2 = 6*8 + 6
h2 = 6*8 + 7

a1 = 7*8 + 0
b1 = 7*8 + 1
c1 = 7*8 + 2
d1 = 7*8 + 3
e1 = 7*8 + 4
f1 = 7*8 + 5
g1 = 7*8 + 6
h1 = 7*8 + 7

# en passant flags

EN_PASSANT_FILE_0 = 64
EN_PASSANT_FILE_1 = 65
EN_PASSANT_FILE_2 = 66
EN_PASSANT_FILE_3 = 67
EN_PASSANT_FILE_4 = 68
EN_PASSANT_FILE_5 = 69
EN_PASSANT_FILE_6 = 70
EN_PASSANT_FILE_7 = 71

# castling flags

CASTLING_W_Q = 72
CASTLING_W_K = 73
CASTLING_B_Q = 74
CASTLING_B_K = 75

# flag indicating whos move it is

BLACK_TO_MOVE = 76


# TO DO:

# Many of the less privitive methods of the ChessBoard class should be moved to the
# GameEngine class instead. It is more natural(?). The ChessBoard object should be small enough to
# save in memory in lots of versions. The evaluate method must have access to the previously played 
# boards though (or at least the 6 (?) latest boards, for DRAW purposes). Hmmmmm........

# The evaluate method must have access to the attack_boards. But should they be properties in the ChessBoard class??? No!?!


class Illegal_Move(Exception):
    def __init__(self, arg):
        self.arg = arg


zobrist_table = zobrist.Zobrist()


class ChessBoard(object):

    def __init__(self, templateboard = None):

        if not templateboard:
            self._board = array.array('B', [NONE]*(64 + 8 + 4 + 1))     # NONE denotes an empty square
            self._zobrist_number = 0

            self.setup_board()
        else:
            self._board = copy.copy(templateboard.board)
            self._zobrist_number = templateboard.zobrist_number

        # 64 bytes for the board, 8 bytes for indicating En passants,
        # and 4 bytes for castling rights.

        self.bb = np.array([0]*8, dtype = np.uint64)
        #np.uint64(self.slask)

        #self.attack_table_already_calculated = {WHITE: False, BLACK: False}
        self.attack_table = {WHITE: array.array('B', [NONE]*64), BLACK: array.array('B', [NONE]*64)}
        #self.enemy_attack_table = array.array('B', [NONE]*64)
        #self.attack_table = array.array('B', [NONE]*64)
        


#   PROPERTIES

    @property
    def zobrist_number(self):
        return self._zobrist_number

    @zobrist_number.setter
    def zobrist_number(self, number):
        self._zobrist_number = number

    @property
    def board(self):
        return self._board


#   For sorting purposes etc

    def __eq__(self, other_chessboard):
        if hasattr(other_chessboard, '_zobrist_number'):
            return self.zobrist_number == other_chessboard.zobrist_number
        else:
            return False


#   METHODS


#   ZOBRIST

    def update_zobrist_number(self, key):
        self.zobrist_number = self.zobrist_number ^ zobrist_table.zobrist_number(key)


#   BOARD MOVEMENT AND HELP METHODS

    def remove_piece(self, piece, position):
        self.board[position] = NONE
        self.update_zobrist_number( (piece, position ) )

    def place_piece(self, piece, position):
        self.board[position] = piece
        self.update_zobrist_number( (piece, position) )

    def get_piece_class(self, position):
        return PIECECLASSES[self.board[position]]

    def get_piece(self, position):
        return self.board[position]

    def square_contains_enemy(self, position, friendly_color):
        if self.empty_square(position):
            return False
        elif friendly_color == WHITE:
            return self.board[position] > WHITE_BLACK_SEPARATOR
        else:
            return self.board[position] < WHITE_BLACK_SEPARATOR

    def square_contains_friend(self, position, friendly_color):
        if self.empty_square(position):
            return False
        elif friendly_color == WHITE:
            return self.board[position] < WHITE_BLACK_SEPARATOR
        else:
            return self.board[position] > WHITE_BLACK_SEPARATOR
    
    

    def empty_square(self, position):
        #print(position)
        return self.board[position] == 0

    def get_file(self, position):
        return position % 8

    def get_rank(self, position):
        return position // 8
        #return position / 8

    def on_board(self, rank, file):
        return ( (0 <= rank) and (rank < 8) and (0 <= file) and (file < 8) )
        #return 

    def get_color(self, position):      # Returns WHITE if square empty
        if self.board[position] < WHITE_BLACK_SEPARATOR:
            return WHITE
        else:
            return BLACK


#   CASTLING FLAGS

    def castling_queen_side_flag(self, color):
        if color == WHITE:
            return self.board[CASTLING_W_Q] == 1
        else:
            return self.board[CASTLING_B_Q] == 1

    def castling_king_side_flag(self, color):
        if color == WHITE:
            return self.board[CASTLING_W_K] == 1
        else:
            return self.board[CASTLING_B_K] == 1

    def set_castling_king_side_flag(self, color):
        if color == WHITE:
            self.board[CASTLING_W_K] = 1
            self.update_zobrist_number(CASTLING_W_K)
        else:
            self.board[CASTLING_B_K] = 1
            self.update_zobrist_number(CASTLING_B_K)

    def clear_castling_king_side_flag(self, color):
        if color == WHITE:
            self.board[CASTLING_W_K] = 0
            self.update_zobrist_number(CASTLING_W_K)
        else:
            self.board[CASTLING_B_K] = 0
            self.update_zobrist_number(CASTLING_B_K)

    def set_castling_queen_side_flag(self, color):
        if color == WHITE:
            self.board[CASTLING_W_Q] = 1
            self.update_zobrist_number(CASTLING_W_Q)
        else:
            self.board[CASTLING_B_Q] = 1
            self.update_zobrist_number(CASTLING_B_Q)

    def clear_castling_queen_side_flag(self, color):
        if color == WHITE:
            self.board[CASTLING_W_Q] = 0
            self.update_zobrist_number(CASTLING_W_Q)
        else:
            self.board[CASTLING_B_Q] = 0
            self.update_zobrist_number(CASTLING_B_Q)

    def set_all_castling_flags(self, color):
        self.set_castling_king_side_flag(color)
        self.set_castling_queen_side_flag(color)

    def clear_all_castling_flags(self, color):  
        if self.castling_queen_side_flag(color):
            self.clear_castling_queen_side_flag(color)
        if self.castling_king_side_flag(color):
            self.clear_castling_king_side_flag(color)

        
#   EN PASSANT FLAGS

    def en_passant_flag(self, file):         # en passant is zero if not existing
        return self.board[EN_PASSANT_FILE_0 + file]

    def set_en_passant_flag(self, file):
        self.board[EN_PASSANT_FILE_0 + file] = 1
        self.update_zobrist_number(EN_PASSANT_FILE_0 + file)

    def clear_en_passant_flag(self, file):
        self.board[EN_PASSANT_FILE_0 + file] = 0
        self.update_zobrist_number(EN_PASSANT_FILE_0 + file)

    def clear_all_en_passant_flags(self):
        for file in range(8):
            if self.en_passant_flag(file):
                self.clear_en_passant_flag(file)

    def forcibly_clear_all_en_passant_flags(self):
        for file in range(8):
            self.clear_en_passant_flag(file)



#   BLACK TO MOVE
    
    def toggle_color_to_move(self):
        
        if self.board[BLACK_TO_MOVE] == 1:
            self.board[BLACK_TO_MOVE] = 0
        else:
            self.board[BLACK_TO_MOVE] = 1
  
        self.update_zobrist_number(BLACK_TO_MOVE)


    # Methods for search algorithms

    def evaluate_node(self):
        return self.evaluate()

    def all_possible_nodes(self, color):
        if color == WHITE:

            #nodes = self.all_possible_new_boards(WHITE)
            nodes = list(self.all_legal_moves_and_corresponding_boards(WHITE).values())
            #print(nodes)
            
        else:

            #nodes = self.all_possible_new_boards(BLACK)
            nodes = list(self.all_legal_moves_and_corresponding_boards(BLACK).values())
            #print(nodes)

        return nodes
            







    def evaluate(self):  # Heuristically evaluate chessboard from WHITES point of view
        
        white_strength = 0
        black_strength = 0

        for position in range(64):

            if PIECECLASSES[self.board[position] ] == None:

                pass

            elif PIECECLASSES[ self.board[position] ] == Pawn:
                
                if self.get_color(position) == WHITE:
                    
                    white_strength += evaluation.P + evaluation.w_pawn_mid[self.get_rank(position)][self.get_file(position)]
                
                else:

                    black_strength += evaluation.P + evaluation.b_pawn_mid[self.get_rank(position)][self.get_file(position)]


            elif PIECECLASSES[ self.board[position] ] == Knight:
                
                if self.get_color(position) == WHITE:
                    
                    white_strength += evaluation.Kn + evaluation.w_knight_mid[self.get_rank(position)][self.get_file(position)]
                
                else:

                    black_strength += evaluation.Kn + evaluation.b_knight_mid[self.get_rank(position)][self.get_file(position)]


            elif PIECECLASSES[ self.board[position] ] == Bishop:
                
                if self.get_color(position) == WHITE:
                    
                    white_strength += evaluation.B + evaluation.w_bishop_mid[self.get_rank(position)][self.get_file(position)]
                
                else:

                    black_strength += evaluation.B + evaluation.b_bishop_mid[self.get_rank(position)][self.get_file(position)]


            elif PIECECLASSES[ self.board[position] ] == Rook:
                
                if self.get_color(position) == WHITE:
                    
                    white_strength += evaluation.R + evaluation.w_rook_mid[self.get_rank(position)][self.get_file(position)]
                
                else:

                    black_strength += evaluation.R + evaluation.b_rook_mid[self.get_rank(position)][self.get_file(position)]


            elif PIECECLASSES[ self.board[position] ] == Queen:
                
                if self.get_color(position) == WHITE:
                    
                    white_strength += evaluation.Q + evaluation.w_queen_mid[self.get_rank(position)][self.get_file(position)]
                
                else:

                    black_strength += evaluation.Q + evaluation.b_queen_mid[self.get_rank(position)][self.get_file(position)]


            elif PIECECLASSES[ self.board[position] ] == King:
                
                if self.get_color(position) == WHITE:
                    
                    white_strength += evaluation.K + evaluation.w_king_mid[self.get_rank(position)][self.get_file(position)]
                
                else:

                    black_strength += evaluation.K + evaluation.b_king_mid[self.get_rank(position)][self.get_file(position)]
            
            else: 
                print('Something is horribly wrong.')

        return white_strength - black_strength



    def get_complement_color(self, color):
        if color == WHITE:
            return BLACK
        else:
            return WHITE


    def execute(self, move):
        
        original_position, new_position = move

        moving_color = self.get_color(original_position)
        opponent_color = self.get_complement_color(moving_color)

        
        
        if not self.empty_square(new_position):     # First, remove destroyed piece, if it exists
            self.remove_piece(self.get_piece(new_position), new_position)



        if self.get_piece_class(original_position) == Pawn:

            # Conversion to Queen (choice should be implemented here!!!!)

            if self.get_rank(new_position) == 0:

                self.place_piece(W_QUEEN, new_position)   
                self.remove_piece(W_PAWN, original_position)   

                self.clear_all_en_passant_flags()

            elif self.get_rank(new_position) == 7:

                self.place_piece(B_QUEEN, new_position)   
                self.remove_piece(B_PAWN, original_position)

                # Clear all en passant flags
                self.clear_all_en_passant_flags()
            
            # Two steps forward, set en passant flag
            elif abs(self.get_rank(new_position) - self.get_rank(original_position)) == 2:

                self.place_piece(self.get_piece(original_position), new_position)   
                self.remove_piece(self.get_piece(original_position), original_position)

                # Clear all en passant flags
                self.clear_all_en_passant_flags()

                # Set en passant flag
                self.set_en_passant_flag(self.get_file(original_position))

            # En passant catch
            elif self.en_passant_flag(self.get_file(new_position)):
            
                if self.get_rank(new_position) == 2 and moving_color == WHITE:
                    
                    self.remove_piece(self.get_piece(new_position + S), new_position + S)

                elif self.get_rank(new_position) == 5 and moving_color == BLACK:

                    self.remove_piece(self.get_piece(new_position + N), new_position + N)

                self.place_piece(self.get_piece(original_position), new_position)
                self.remove_piece(self.get_piece(original_position), original_position)

                # Clear all en passant flags
                self.clear_all_en_passant_flags()

            else:

                self.place_piece(self.get_piece(original_position), new_position)
                self.remove_piece(self.get_piece(original_position), original_position)

                # Clear all en passant flags
                self.clear_all_en_passant_flags()

            # Do some analysis of which pieces are under attack, and also by how many pieces!!!
            # This can be used to determine if king is under attack. But could also perhaps be an 
            # integral part of the evaluation of the node!!!!!


        elif self.get_piece_class(original_position) == Rook:

            # Clear castling flags according to moving rook
            if self.get_file(original_position) == 0 and self.castling_queen_side_flag(moving_color):
                self.clear_castling_queen_side_flag(moving_color)
            
            if self.get_file(original_position) == 7 and self.castling_king_side_flag(moving_color):
                self.clear_castling_king_side_flag(moving_color)

            self.place_piece(self.get_piece(original_position), new_position)
            self.remove_piece(self.get_piece(original_position), original_position)

            # Clear all en passant flags
            self.clear_all_en_passant_flags()

        
        elif self.get_piece_class(original_position) == King:

            self.calculate_attacking_table(opponent_color)

            # Castling
            if new_position == original_position + 2*E:

                if not (self.is_under_attack(original_position, moving_color) or 
                        self.is_under_attack(original_position + E, moving_color) or
                        self.is_under_attack(original_position + 2*E, moving_color)):

                    # Move king
                    self.place_piece(self.get_piece(original_position), new_position)   
                    self.remove_piece(self.get_piece(original_position), original_position)

                    # Move rook
                    self.place_piece(self.get_piece(original_position + 3*E), original_position + E)
                    self.remove_piece(self.get_piece(original_position + 3*E), original_position + 3*E)

            elif new_position == original_position + 2*W:

                if not (self.is_under_attack(original_position, moving_color) or 
                        self.is_under_attack(original_position + W, moving_color) or
                        self.is_under_attack(original_position + 2*W, moving_color)):

                    # Move king
                    self.place_piece(self.get_piece(original_position), new_position)
                    self.remove_piece(self.get_piece(original_position), original_position)

                    # Move rook
                    self.place_piece(self.get_piece(original_position + 4*W), original_position + W)
                    self.remove_piece(self.get_piece(original_position + 4*W), original_position + 4*W)

            else:

                self.place_piece(self.get_piece(original_position), new_position)
                self.remove_piece(self.get_piece(original_position), original_position)

            # Clear all en passant flags
            self.clear_all_en_passant_flags()

            # Clear all castling flags due to king move
            self.clear_all_castling_flags(moving_color)

        else:

            # If nothing special, move accordingly

            self.place_piece(self.get_piece(original_position), new_position)
            self.remove_piece(self.get_piece(original_position), original_position)

            # Clear all en passant flags
            self.clear_all_en_passant_flags()

        # Calculate attack_tables
        self.calculate_attacking_table(moving_color)
        self.calculate_attacking_table(opponent_color)

        #for position in range(64):
        #    if self.square_contains_enemy(position, moving_color):
        #        enemy_moves = self.get_piece_class(position).possible_moves(self, position, enemy_color)
        #        for move in enemy_moves:
        #            from_position, to_position = move
        #            self.attack_table[enemy_color][to_position] += 1

        self.toggle_color_to_move()

        #print('hepp')


    def calculate_attacking_table(self, color):
        #if not self.attack_table_already_calculated[color]:
        for position in range(64):
            self.attack_table[color][position] = 0
        for position in range(64):
            if self.square_contains_friend(position, color):
                moves = self.get_piece_class(position).possible_moves(self, position, color)
                for move in moves:
                    from_position, to_position = move
                    self.attack_table[color][to_position] += 1
            #self.attack_table_already_calculated[color] = True


    def king_is_under_attack(self, color):

        if color == WHITE:
        
            position = 0
            while self.get_piece(position) != W_KING:
                position += 1
            
            #return self.is_under_attack(position, WHITE)
            #if self.attack_table[BLACK][position] > 0:
            #    return True
            #else:
            #    return False

        elif color == BLACK:
        
            position = 0
            while self.get_piece(position) != B_KING:
                position += 1

        return self.is_under_attack(position, color)
            
            #if self.attack_table[WHITE][position] > 0:
            #    return True
            #else:
            #    return False


    def is_under_attack(self, position, color):
        attackers_color = self.get_complement_color(color)
        if self.attack_table[attackers_color][position] > 0:
            return True
        else:
            return False



            


        


    def all_legal_moves_and_corresponding_boards(self, color):

        possible_moves = []

        for position in range(64):  

            #print(position)

            if self.square_contains_friend(position, color):
                possible_moves += self.get_piece_class(position).possible_moves(self, position, color)

        # HERE!!!! Count attack!!!!

        # If new position was empty, is attacked by enemy, and not defended, it probably is a bad move
        # If moving color is checked after move, move is not allowed

        #legal_boards = []
        #legal_moves = []
        legal_moves_and_corresponding_boards = {}

        #print('fita')

        for move in possible_moves:

            new_board = ChessBoard(self)        # 16 times more efficient than deepcopy (!!!!!)

            #try:
            new_board.execute(move)

            #print('fiiiiita')

            #except Illegal_Move as e:         # This is probably not a good idea...
            #    print(e.arg)

            #else:
            if not new_board.king_is_under_attack(color):
                legal_moves_and_corresponding_boards[move] = new_board

            
        #print(legal_moves_and_corresponding_boards)
        return legal_moves_and_corresponding_boards













    def draw(self):
        piece_repr = {W_ROOK: 'R', W_KNIGHT: 'S', W_BISHOP: 'B',
                W_QUEEN: 'Q', W_KING: 'K', W_PAWN: 'P',
                B_ROOK: 'r', B_KNIGHT: 's', B_BISHOP: 'b',
                B_QUEEN: 'q', B_KING: 'k', B_PAWN: 'p', NONE: ' '}

        print('------------------------')
        print('')

        for r in range(8):

                line_string = ''
                for f in range(8):
                    line_string += ' ' + piece_repr[self.board[r*8 + f]] + ' '                    
                
                print(line_string)
                print('')

        print('------------------------')
                    

    def setup_board(self):

        # Place white Rooks
        self.place_piece(W_ROOK, a1)
        self.place_piece(W_ROOK, h1)

        # Place white Knights
        self.place_piece(W_KNIGHT, b1)
        self.place_piece(W_KNIGHT, g1)

        # Place white Bishops
        self.place_piece(W_BISHOP, c1)
        self.place_piece(W_BISHOP, f1)

        # Place white Queen
        self.place_piece(W_QUEEN, d1)

        # Place white King
        self.place_piece(W_KING, e1)

        # Place white Pawns
        for position in (a2, b2, c2, d2, e2, f2, g2, h2):
            self.place_piece(W_PAWN, position)


        # Place black Rooks
        self.place_piece(B_ROOK, a8)
        self.place_piece(B_ROOK, h8)

        # Place black Knights
        self.place_piece(B_KNIGHT, b8)
        self.place_piece(B_KNIGHT, g8)

        # Place black Bishops
        self.place_piece(B_BISHOP, c8)
        self.place_piece(B_BISHOP, f8)

        # Place black Queen
        self.place_piece(B_QUEEN, d8)

        # Place black King
        self.place_piece(B_KING, e8)

        # Place black Pawns
        for position in (a7, b7, c7, d7, e7, f7, g7, h7):
            self.place_piece(B_PAWN, position)

        # Set all castling flags
        self.set_all_castling_flags(WHITE)
        self.set_all_castling_flags(BLACK)

        # Clear all en passant flags
        self.forcibly_clear_all_en_passant_flags()

        # The board is initialized with all empty squares, so we are all done

        self.board[BLACK_TO_MOVE] = 0


if __name__ == '__main__':

    b = ChessBoard()

    t0 = time.time()

#    for i in range(10000):
#        c = copy.deepcopy(b)

    t1 = time.time()

    for i in range(1000000):
        c = ChessBoard(b)

    t2 = time.time()

#    print t1 - t0
    print(t2 - t1)


