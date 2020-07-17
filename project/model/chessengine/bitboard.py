#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np

# LSF (Least Significant File-rank) mapping
# square_index = 8*rank_index + file_index

# file_index   = square_index modulo 8  = square_index & 7
# rank_index   = square_index div    8  = square_index >> 3

# 0 <= rank_index <= 7
# 0 <= file_index <= 7


# Representation:

# a8 . . . . . . h8     RANK_8
# .              .
# .              .
# .              .
# .              .
# .              .
# .              .
# a1 . . . . . . h1     RANK_1

# 56 . . . . . . 63
# .              .
# .              .
# .              .
# .              .
# .              .
# .              .
# 00 . . . . . . 07
 
# board = h8......a8h7......a7..................a2h1......a1
# bit:    63...............................................0


# NW             N            NE
#         +7    +8    +9
#             \  |  /
# W       -1 <-  0 -> +1       E
#             /  |  \
#         -9    -8    -7
# SW             S            SE


# Directions

N = 8       
E = 1
S = -8
W = -1
NE = 9
SE = -7
SW = -9
NW = 7


# Vectors

NNE = (2, 1)
NNW = (2, -1)
EEN = (1, 2)
EES = (-1, 2)
SSW = (-2, -1)
SSE = (-2, 1)
WWN = (1, -2)
WWS = (-1, -2)


# Named positions                                                                                   # Chess specific

a1 = 0
b1 = 1
c1 = 2
d1 = 3
e1 = 4
f1 = 5
g1 = 6
h1 = 7
a2 = 1*8 + 0
b2 = 1*8 + 1
c2 = 1*8 + 2
d2 = 1*8 + 3
e2 = 1*8 + 4
f2 = 1*8 + 5
g2 = 1*8 + 6
h2 = 1*8 + 7
a3 = 2*8 + 0
b3 = 2*8 + 1
c3 = 2*8 + 2
d3 = 2*8 + 3
e3 = 2*8 + 4
f3 = 2*8 + 5
g3 = 2*8 + 6
h3 = 2*8 + 7
a4 = 3*8 + 0
b4 = 3*8 + 1
c4 = 3*8 + 2
d4 = 3*8 + 3
e4 = 3*8 + 4
f4 = 3*8 + 5
g4 = 3*8 + 6
h4 = 3*8 + 7
a5 = 4*8 + 0
b5 = 4*8 + 1
c5 = 4*8 + 2
d5 = 4*8 + 3
e5 = 4*8 + 4
f5 = 4*8 + 5
g5 = 4*8 + 6
h5 = 4*8 + 7
a6 = 5*8 + 0
b6 = 5*8 + 1
c6 = 5*8 + 2
d6 = 5*8 + 3
e6 = 5*8 + 4
f6 = 5*8 + 5
g6 = 5*8 + 6
h6 = 5*8 + 7
a7 = 6*8 + 0
b7 = 6*8 + 1
c7 = 6*8 + 2
d7 = 6*8 + 3
e7 = 6*8 + 4
f7 = 6*8 + 5
g7 = 6*8 + 6
h7 = 6*8 + 7
a8 = 7*8 + 0
b8 = 7*8 + 1
c8 = 7*8 + 2
d8 = 7*8 + 3
e8 = 7*8 + 4
f8 = 7*8 + 5
g8 = 7*8 + 6
h8 = 7*8 + 7


# For easy string representation of positions                                                      # Chess specific 

pos_str = {}
i = 0
for f in ('1', '2', '3', '4', '5', '6', '7', '8'):
    for r in ('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'):
        pos_str[i] = r + f
        i += 1


# Piece representations                                                                             # Chess specific

ROOK = 0
KNIGHT = 1
BISHOP = 2
QUEEN = 3
KING = 4
PAWN = 5


# Functions

def square_index(rank_index, file_index):
    return (rank_index*8 + file_index)

def file_index(square_index):
    return (square_index & 7)

def rank_index(square_index):
    return (square_index >> 3)


# Set functions

def bit_set(square_index):
    return np.uint64(1) << np.uint64(square_index)        # Perhaps slow and inefficient


def adjecent_square_set(origin_square_index, direction):
# Returns the set of the adjecent square in a direction.
    f = file_index(origin_square_index)
    r = rank_index(origin_square_index)
    if (direction == N or direction == NE or direction == NW) and r == 7:
        return EMPTY
    elif (direction == S or direction == SE or direction == SW) and r == 0:
        return EMPTY
    elif (direction == W or direction == NW or direction == SW) and f == 0:
        return EMPTY
    elif (direction == E or direction == NE or direction == SE) and f == 7:
        return EMPTY
    else:
        return bit_set(origin_square_index + direction)


def direction_set(origin_square_index, direction):
# Returns the set of positions in the direction from the origin square. The origin square is not part of the set.
    temp_set = adjecent_square_set(origin_square_index, direction)
    if temp_set == EMPTY:
        return EMPTY
    else:
        return temp_set | direction_set(origin_square_index + direction, direction)


def vector_set(origin_square_index, vector):
# Returns the set of the square in the position of the origin square plus the vector. Returns the EMPTY set if 
# calculated position is out of bounds.
    f = file_index(origin_square_index)
    r = rank_index(origin_square_index)
    dr, df = vector
    if 0 <= f + df and f + df < 8 and 0 <= r + dr and r + dr < 8:
        return bit_set(square_index(r + dr, f + df))
    else:
        return EMPTY


# Simple constants

ONE = np.uint64(1)

UNIVERSAL = np.uint64(2 ** 63 - 1)

EMPTY = np.uint64(0)

CORNERS = bit_set(a1) + bit_set(a8) + bit_set(h1) + bit_set(h8)

RANK_1 = np.uint64(0x00000000000000FF)  # 1
RANK_2 = np.uint64(0x000000000000FF00)  # 2
RANK_3 = np.uint64(0x0000000000FF0000)  # 3
RANK_4 = np.uint64(0x00000000FF000000)  # 
RANK_5 = np.uint64(0x000000FF00000000)
RANK_6 = np.uint64(0x0000FF0000000000)
RANK_7 = np.uint64(0x00FF000000000000)
RANK_8 = np.uint64(0xFF00000000000000)  # 8

RANK = (RANK_1, RANK_2, RANK_3, RANK_4, RANK_5, RANK_6, RANK_7, RANK_8)

FILE_A = np.uint64(0x0101010101010101)  # a
FILE_B = np.uint64(0x0202020202020202)  # b
FILE_C = np.uint64(0x0404040404040404)  # c
FILE_D = np.uint64(0x0808080808080808)  #
FILE_E = np.uint64(0x1010101010101010)
FILE_F = np.uint64(0x2020202020202020)
FILE_G = np.uint64(0x4040404040404040)
FILE_H = np.uint64(0x8080808080808080)  # h

FILE = (FILE_A, FILE_B, FILE_C, FILE_D, FILE_E, FILE_F, FILE_G, FILE_H)

NOT_FILE_A = np.uint64(0xfefefefefefefefe)
NOT_FILE_H = np.uint64(0x7f7f7f7f7f7f7f7f)

DIAG_1  = np.uint64(0x0000000000000080)
DIAG_2  = np.uint64(0x0000000000008040)
DIAG_3  = np.uint64(0x0000000000804020)
DIAG_4  = np.uint64(0x0000000080402010)
DIAG_5  = np.uint64(0x0000008040201008)
DIAG_6  = np.uint64(0x0000804020100804)
DIAG_7  = np.uint64(0x0080402010080402)
DIAG_8  = np.uint64(0x8040201008040201)
DIAG_9  = np.uint64(0x4020100804020100)
DIAG_10 = np.uint64(0x2010080402010000)
DIAG_11 = np.uint64(0x1008040201000000)
DIAG_12 = np.uint64(0x0804020100000000)
DIAG_13 = np.uint64(0x0402010000000000)
DIAG_14 = np.uint64(0x0201000000000000)
DIAG_15 = np.uint64(0x0100000000000000)

DIAG = (DIAG_1, DIAG_2, DIAG_3, DIAG_4, DIAG_5, DIAG_6, DIAG_7, DIAG_8, DIAG_9, DIAG_10, DIAG_11, DIAG_12, DIAG_13, DIAG_14, DIAG_15)


CENTRE = (FILE_D | FILE_E) & (RANK_4 | RANK_5)
EXTENDED_CENTRE = (FILE_C | FILE_D | FILE_E | FILE_F) & (RANK_3 | RANK_4 | RANK_5 | RANK_6)


# Ray sets

RAY_SET = [ ]       # RAY_SETS[square_index][ray_direction] = ray_set

def create_ray_sets():

    for original_square_index in range(64):
    
        RAY_SET.append({})
        for direction in (N, NE, E, SE, S, SW, W, NW):
            RAY_SET[-1].update({direction: direction_set(original_square_index, direction)})
        
create_ray_sets()


# LSB and MSB functions

def lsb(x):
    return (x & -x)

def msb(x):
    x |= (x >> np.uint64(1))
    x |= (x >> np.uint64(2))
    x |= (x >> np.uint64(4))
    x |= (x >> np.uint64(8))
    x |= (x >> np.uint64(16))
    x |= (x >> np.uint64(32))
    return x - (x >> np.uint64(1))


# One step onlys

def south_one(bb):
    return bb >> np.uint64(8)

def north_one(bb):
    return bb << np.uint64(8)

def east_one(bb):
    return (bb << np.uint64(1)) & NOT_FILE_A

def west_one(bb):
    return (bb >> np.uint64(1)) & NOT_FILE_H

def ne_one(bb):
    return (bb << 9) & NOT_FILE_A

def se_one(bb):
    return (bb >> 7) & NOT_FILE_A

def sw_one(bb):
    return (bb >> 9) & NOT_FILE_H

def nw_one(bb):
    return (bb << 7) & NOT_FILE_H


# General attack sets
# Obstruction difference method for attack sets

def vertical_attack_set(origin_position, occupied):
    lsb_upper = lsb(RAY_SET[origin_position][N] & occupied)
    msb_lower_or_1 = msb(RAY_SET[origin_position][S] & occupied | np.uint64(1))
    attack_set = (np.uint64(2)*lsb_upper - msb_lower_or_1) & (RAY_SET[origin_position][N] | RAY_SET[origin_position][S])
    return attack_set

def horizontal_attack_set(origin_position, occupied):
    lsb_upper = lsb(RAY_SET[origin_position][E] & occupied)
    msb_lower_or_1 = msb(RAY_SET[origin_position][W] & occupied | np.uint64(1))
    attack_set = (np.uint64(2)*lsb_upper - msb_lower_or_1) & (RAY_SET[origin_position][E] | RAY_SET[origin_position][W])
    return attack_set

def diagonal_attack_set(origin_position, occupied):
    lsb_upper = lsb(RAY_SET[origin_position][NE] & occupied)
    msb_lower_or_1 = msb(RAY_SET[origin_position][SW] & occupied | np.uint64(1))
    attack_set = (np.uint64(2)*lsb_upper - msb_lower_or_1) & (RAY_SET[origin_position][NE] | RAY_SET[origin_position][SW])
    return attack_set

def anti_diagonal_attack_set(origin_position, occupied):
    lsb_upper = lsb(RAY_SET[origin_position][NW] & occupied)
    msb_lower_or_1 = msb(RAY_SET[origin_position][SE] & occupied | np.uint64(1))
    attack_set = (np.uint64(2)*lsb_upper - msb_lower_or_1) & (RAY_SET[origin_position][NW] | RAY_SET[origin_position][SE])
    return attack_set



# SLIDING PIECES ATTACKS

def rook_attack_set(origin_position, occupied):
# Returns board with ones in all attack positions. To exclude own pieces, use & ownpieces.
    return vertical_attack_set(origin_position, occupied) | horizontal_attack_set(origin_position, occupied)

def knight_attack_set(origin_position, occupied):
# Returns board with ones in all attack positions. To exclude own pieces, use & ownpieces.
    return diagonal_attack_set(origin_position, occupied) | anti_diagonal_attack_set(origin_position, occupied)

def queen_attack_set(origin_position, occupied):
# Returns board with ones in all attack positions. To exclude own pieces, use & ownpieces.
    return rook_attack_set(origin_position, occupied) | knight_attack_set(origin_position, occupied)



# PAWN ATTACK SETS

# White
def white_pawns_east_attacks(white_pawns):
    return ne_one(white_pawns)

def white_pawns_west_attacks(white_pawns):
    return nw_one(white_pawns)

def white_pawns_attacks(white_pawns):
    return white_pawns_east_attacks(white_pawns) | white_pawns_west_attacks(white_pawns)

def white_pawns_double_attacks(white_pawns):
    return white_pawns_east_attacks(white_pawns) & white_pawns_west_attacks(white_pawns)

def white_pawns_single_attacks(white_pawns):
    return white_pawns_east_attacks(white_pawns) ^ white_pawns_west_attacks(white_pawns)

def white_safe_pawn_squares(white_pawns, black_pawns):
    return white_pawns_double_attacks(white_pawns) | ~black_pawns_attacks(black_pawns) | (white_pawns_single_attacks(white_pawns) & ~black_pawns_double_attacks(black_pawns))

#Black
def black_pawns_east_attacks(black_pawns):
    return se_one(black_pawns)

def black_pawns_west_attacks(black_pawns):
    return sw_one(black_pawns)

def black_pawns_attacks(black_pawns):
    return black_pawns_east_attacks(black_pawns) | black_pawns_west_attacks(black_pawns)

def black_pawns_double_attacks(black_pawns):
    return black_pawns_east_attacks(black_pawns) & black_pawns_west_attacks(black_pawns)

def black_pawns_single_attacks(black_pawns):
    return black_pawns_east_attacks(black_pawns) ^ black_pawns_west_attacks(black_pawns)

def black_safe_pawn_squares(white_pawns, black_pawns):
    return black_pawns_double_attacks(black_pawns) | ~white_pawns_attacks(white_pawns) | (black_pawns_single_attacks(black_pawns) & ~white_pawns_double_attacks(white_pawns))






# Bitscan functions

index64 = (
    0, 47,  1, 56, 48, 27,  2, 60,
   57, 49, 41, 37, 28, 16,  3, 61,
   54, 58, 35, 52, 50, 42, 21, 44,
   38, 32, 29, 23, 17, 11,  4, 62,
   46, 55, 26, 59, 40, 36, 15, 53,
   34, 51, 20, 43, 31, 22, 10, 45,
   25, 39, 14, 33, 19, 30,  9, 24,
   13, 18,  8, 12,  7,  6,  5, 63
)


np.seterr(all = 'ignore')           # Repress warnings for overflow due to data type


def bitscanforward(bitboard):       # Returns index for Least Signicant Bit
    debruijn64 = np.uint64(0x03f79d71b4cb0a89)
    if bitboard != EMPTY:
        return index64[((bitboard ^ (bitboard - np.uint64(1))) * debruijn64) >> np.uint64(58)]
    else:
        print('FEL')


def bitscanreverse(bitboard):       # Returns index for Most Significant Bit
    debruijn64 = np.uint64(0x03f79d71b4cb0a89)
    if bitboard != EMPTY:
        bitboard |= bitboard >> np.uint64(1)
        bitboard |= bitboard >> np.uint64(2)
        bitboard |= bitboard >> np.uint64(4)
        bitboard |= bitboard >> np.uint64(8)
        bitboard |= bitboard >> np.uint64(16)
        bitboard |= bitboard >> np.uint64(32)
        return index64[(bitboard * debruijn64) >> np.uint64(58)]
    else:
        print('FEL')



# Calculate square indexes

def get_square_indexes(bitboard):
    index_list = []
    while bitboard != EMPTY:
        index_list.append(bitscanforward(bitboard))     # Add index for LSB
        bitboard &= (bitboard - np.uint64(1))           # Remove LSB
    return index_list


# Bit fiddling

def reverse(bb):            # A naive and really slow reverse
    r = EMPTY
    for c in range(64):
        r |= bb & np.uint64(1)
        if c < 63:
            r <<= np.uint64(1)
        bb >>= np.uint64(1)
    return r


# For debugging purposes

def print_board(board):
    print('')
    for r in reversed(range(8)):
        line = ''
        for f in range(8):
            if board & bit_set(square_index(r, f)):
                line += '1'
            else:
                line += '0'
        print(line)
    print('')



TABLE = {}







if __name__ == '__main__':

    # Targets
#    targets = bit_set(b7) | bit_set(b8) | bit_set(e2) | bit_set(a6) | bit_set(b2)
#    targets = RANK_1 | RANK_8 | FILE_A | FILE_H | RANK_7
#    print_board(targets)

#    print_board(rook_attack_set(b5, targets))
#    print_board(knight_attack_set(b5, targets))
#    print_board(queen_attack_set(b5, targets))

#    print_board(diagonal_attack_set(c4, targets))
#    print_board(anti_diagonal_attack_set(b2, targets))
  
    targets = bit_set(a1) | bit_set(c3) | bit_set(e8) | bit_set(h4) | bit_set(c8)
    print_board(targets)

    attack_set = queen_attack_set(d4, targets)
    print_board(attack_set)

    movement_set = attack_set & ~targets    # All targets friendly
    print_board(movement_set)

    index_list = get_square_indexes(movement_set)
    for each in index_list:
        print(pos_str[each])
