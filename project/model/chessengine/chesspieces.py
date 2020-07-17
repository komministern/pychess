#!/usr/bin/env python
# -*- coding: utf-8 -*-


WHITE = 1
BLACK = -1

W = -1      # Import these constants from chessboard perhaps
E = 1
N = -8
S = 8


class ChessPiece(object):

    @classmethod
    def possible_moves(cls, board, position, color):
        return []

    @classmethod
    def value(cls):
        return 1


    @staticmethod
    def possible_moves_in_directions(board, position, color, direction_vectors):

        rank = board.get_rank(position)
        file = board.get_file(position)


        possible_moves = []

        for direction_vector in direction_vectors:

            rank_vector, file_vector = direction_vector

            temp_rank = rank + rank_vector
            temp_file = file + file_vector

            while board.on_board(temp_rank, temp_file):

                temp_position = 8*temp_rank + temp_file

                if board.square_contains_friend(temp_position, color):
                    break
                elif board.square_contains_enemy(temp_position, color):
                    possible_moves.append( (position, temp_position) )
                    break
                else:
                    possible_moves.append( (position, temp_position) )

                temp_rank += rank_vector
                temp_file += file_vector

        return possible_moves



    @staticmethod
    def possible_moves_in_discrete_positions(board, position, color, discrete_positions):

        rank = board.get_rank(position)
        file = board.get_file(position)

        possible_moves = []

        for discrete_position in discrete_positions:

            rank_vector, file_vector = discrete_position

            temp_rank = rank + rank_vector
            temp_file = file + file_vector

            if board.on_board(temp_rank, temp_file):

                temp_position = 8*temp_rank + temp_file
                
                if not board.square_contains_friend(temp_position, color):
                    possible_moves.append( (position, temp_position) )
                
        return possible_moves


class King(ChessPiece):

    @classmethod
    def value(cls):
        return 5

    @classmethod
    def possible_moves(cls, board, position, color):

        discrete_positions = ((1,0), (-1,0), (1,1), (-1,-1), (1,-1), (-1,1), (0,1), (0,-1))
        possible_moves = cls.possible_moves_in_discrete_positions(board, position, color, discrete_positions)

        # Check castling

        if board.castling_queen_side_flag(color) and board.empty_square(position + W) and board.empty_square(position + 2*W) and board.empty_square(position + 3*W):

            possible_moves.append( (position, position + 2*W) )

        if board.castling_king_side_flag(color) and board.empty_square(position + E) and board.empty_square(position + 2*E):
            
            possible_moves.append( (position, position + 2*E) )

        return possible_moves



class Pawn(ChessPiece):

    @classmethod
    def value(cls):
        return 1

    @classmethod
    def possible_moves(cls, board, position, color):

        possible_moves = []

        rank = board.get_rank(position)
        file = board.get_file(position)

        if (rank == 6 and color == WHITE) or (rank == 1 and color == BLACK):
            startingposition = True
        else:
            startingposition = False

        if color == BLACK:
            delta = S
        elif color == WHITE:
            delta = N


        if board.empty_square(position + delta):      # One step forward
            possible_moves.append( (position, position + delta) )

            if startingposition:
                if board.empty_square(position + 2*delta):   # Two steps forward
                    possible_moves.append( (position, position + 2*delta) )

        
        if file < 7:
            if board.square_contains_enemy(position + delta + E, color):
                possible_moves.append( (position, position + delta + E) )

            # En passant
            if board.en_passant_flag(board.get_file(position + E)):

                if board.get_rank(position) == 3 and color == WHITE:
                    possible_moves.append( (position, position + delta + E) )
                elif board.get_rank(position) == 4 and color == BLACK:
                    possible_moves.append( (position, position + delta + E) )


        if file > 0:
            if board.square_contains_enemy(position + delta + W, color):
                possible_moves.append( (position, position + delta + W) )

            # En passant
            if board.en_passant_flag(board.get_file(position + W)):

                if board.get_rank(position) == 3 and color == WHITE:
                    possible_moves.append( (position, position + delta + W) )
                elif board.get_rank(position) == 4 and color == BLACK:
                    possible_moves.append( (position, position + delta + W) )


        return possible_moves



class Rook(ChessPiece):

    @classmethod
    def value(cls):
        return 5

    @classmethod
    def possible_moves(cls, board, position, color):

        directions = ((1,0), (-1,0), (0,1), (0,-1))

        return cls.possible_moves_in_directions(board, position, color, directions)



class Queen(ChessPiece):

    @classmethod
    def value(cls):
        return 9

    @classmethod
    def possible_moves(cls, board, position, color):

        directions = ((1,0), (-1,0), (1,1), (-1,1), (-1,-1), (1,-1), (0,1), (0,-1))

        return cls.possible_moves_in_directions(board, position, color, directions)



class Bishop(ChessPiece):

    @classmethod
    def value(cls):
        return 3

    @classmethod
    def possible_moves(cls, board, position, color):
        
        directions = ((1,1), (-1,1), (1,-1), (-1,-1))

        return cls.possible_moves_in_directions(board, position, color, directions)



class Knight(ChessPiece):
    
    @classmethod
    def value(cls):
        return 3

    @classmethod
    def possible_moves(cls, board, position, color):
        
        vectors = ((2,1), (2,-1), (-2,1), (-2,-1), (1,2), (-1,2), (1,-2), (-1,-2))

        return cls.possible_moves_in_discrete_positions(board, position, color, vectors)


    
