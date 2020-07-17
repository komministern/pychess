#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random

#from chessboard import W_PAWN, W_ROOK, W_KNIGHT, W_BISHOP, W_QUEEN, W_KING 
#from chessboard import B_PAWN, B_ROOK, B_KNIGHT, B_BISHOP, B_QUEEN, B_KING
#from chessboard import CASTLING_W_Q, CASTLING_W_K, CASTLING_B_Q, CASTLING_B_K
#from chessboard import EN_PASSANT_FILE_0, EN_PASSANT_FILE_1, EN_PASSANT_FILE_2, EN_PASSANT_FILE_3
#from chessboard import EN_PASSANT_FILE_4, EN_PASSANT_FILE_5, EN_PASSANT_FILE_6, EN_PASSANT_FILE_7
#from chessboard import BLACK_TO_MOVE


#---- To solve circular import issue

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

#PIECECLASSES = {W_PAWN: Pawn, B_PAWN: Pawn,
#                W_ROOK: Rook, B_ROOK: Rook,
#                W_KNIGHT: Knight, B_KNIGHT: Knight,
#                W_BISHOP: Bishop, B_BISHOP: Bishop,
#                W_QUEEN: Queen, B_QUEEN: Queen,
#                W_KING: King, B_KING: King, NONE: None}

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



#----


class Zobrist(object):

    def __init__(self):

        self.dict_of_zobrist_numbers = {}

        random.seed(7824523044563117865)

        self.create_dictionary()

    def zobrist_number(self, key):      # key is either (piece (int), position (int))
                                        # or just an int.

        return self.dict_of_zobrist_numbers[key]

    def create_dictionary(self):
        pieces = (W_PAWN, W_ROOK, W_KNIGHT, W_BISHOP, W_QUEEN, W_KING, 
                B_PAWN, B_ROOK, B_KNIGHT, B_BISHOP, B_QUEEN, B_KING)

        for piece in pieces:
            self.dict_of_zobrist_numbers.update(self.create_keys_for_piece(piece))

        # Add flags for En Passant

        self.dict_of_zobrist_numbers.update({EN_PASSANT_FILE_0: self.get_new_key()})
        self.dict_of_zobrist_numbers.update({EN_PASSANT_FILE_1: self.get_new_key()})
        self.dict_of_zobrist_numbers.update({EN_PASSANT_FILE_2: self.get_new_key()})
        self.dict_of_zobrist_numbers.update({EN_PASSANT_FILE_3: self.get_new_key()})
        self.dict_of_zobrist_numbers.update({EN_PASSANT_FILE_4: self.get_new_key()})
        self.dict_of_zobrist_numbers.update({EN_PASSANT_FILE_5: self.get_new_key()})
        self.dict_of_zobrist_numbers.update({EN_PASSANT_FILE_6: self.get_new_key()})
        self.dict_of_zobrist_numbers.update({EN_PASSANT_FILE_7: self.get_new_key()})

        # Add flags for castling

        self.dict_of_zobrist_numbers.update({CASTLING_W_Q: self.get_new_key()})
        self.dict_of_zobrist_numbers.update({CASTLING_W_K: self.get_new_key()})
        self.dict_of_zobrist_numbers.update({CASTLING_B_Q: self.get_new_key()})
        self.dict_of_zobrist_numbers.update({CASTLING_B_K: self.get_new_key()})

        # Add flag for black to move

        self.dict_of_zobrist_numbers.update({BLACK_TO_MOVE: self.get_new_key()})

    def create_keys_for_piece(self, piece):
        dictionary = {}
        for position in range(64):
            dictionary.update({(piece, position): self.get_new_key()})
        return dictionary

    def get_new_key(self):
        return random.getrandbits(64)


if __name__ == '__main__':


    print(W_PAWN)
    z = Zobrist()

    print(z.dict_of_zobrist_numbers)

#    print z.dict_of_zobrist_keys[(3,13)]
#    print z.dict_of_zobrist_keys['string']

#    for i in range(10):
#        print z.get_new_key()
