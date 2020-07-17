#!/usr/bin/env python
# -*- coding: utf-8 -*-


from chessgame import ChessGame

if __name__ == '__main__':

    game = ChessGame()
    game.start(computerstarts = True)

#    position = (0,1)
#    print game.chessboard.piece(position).possible_moves(game.chessboard, position, 'black')

#    print game.chessboard.evaluate('black')

#    game.chessboard.all_possible_new_boards('white')

#    print game.chessboard.getadjecentposition( position, 'SW' )

#    print game.chessboard.piece(position).possible_moves(position, game.chessboard.color(position))

