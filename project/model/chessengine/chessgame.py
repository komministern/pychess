#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import negamax

INF = 1000000
BLACK = -1
WHITE = 1

from chessboard import ChessBoard

class ChessGame(object):

    def __init__(self):

        self.chessboard = ChessBoard()

    def start(self, computerstarts = True):
        
        if computerstarts:
            print('Computer is white. Take this move, bitch!')
            computer_color = 'white'
            
        else:
            print('Computer is black. Please, make your move, punk!')
            computer_color = 'black'

        if computer_color == 'white':


            self.chessboard.draw()
            print('Initial zobrist: ' + str(self.chessboard.zobrist_number))

            #print 'Resulting score: ' + str(self.chessboard.evaluate(WHITE))
            #print 'Hash key: ' + str(self.chessboard._hash_code)


            depth_white = 4
            depth_black = 5

            n = 1
            playing_color = WHITE

            while 1:

                if playing_color == WHITE:
                    depth = depth_white
                else:
                    depth = depth_black

                t0 = time.time()
                
#                abscore, principal_variation = negamax.alphabeta(self.chessboard, depth, -INF, INF, playing_color)

                t1 = time.time()
#                print 'alphabeta:    ' + str(t1 - t0) + ' ' + str(abscore)
#                print [each.zobrist_number for each in principal_variation]

#                abmemscore, principal_variation = negamax.alphabetamemory(self.chessboard, depth, -INF, INF, playing_color)
                
                t2 = time.time()
#                print 'alphabetamem: ' + str(t2 - t1) + ' ' + str(abmemscore)
#                print [each.zobrist_number for each in principal_variation]

#                idscore, principal_variation = negamax.iterativedeepeningalphabeta(self.chessboard, depth, playing_color)
                
                t3 = time.time()
#                print 'iterdeep:     ' + str(t3 - t2) + ' ' + str(idscore)
#                print [each.zobrist_number for each in principal_variation]

                idmemscore, principal_variation = negamax.iterativedeepeningalphabetamemory(self.chessboard, depth, playing_color)

                t4 = time.time()

#                print 'iterdeepmem:  ' + str(t4 - t3) + ' ' + str(idmemscore)
#                print [each.zobrist_number for each in principal_variation]

#                mtdfscore, principal_variation = negamax.mtdf(self.chessboard, depth, playing_color)

                t5 = time.time()

#                print 'mtdf:         ' + str(t5 - t4) + ' ' + str(mtdfscore)
#                print [each.zobrist_number for each in principal_variation]

#                idmtdfscore, principal_variation = negamax.iterativedeepeningmtdf(self.chessboard, depth, playing_color)
                
                t6 = time.time()
                
#                print 'idmtdf:       ' + str(t6 - t5) + ' ' + str(idmtdfscore)
#                print [each.zobrist_number for each in principal_variation]


                if len(principal_variation) == 1:
                    if playing_color == WHITE:
                        print('BLACK WON')
                    else:
                        print('WHITE WON')
                    break
                    
                print('')
                if playing_color == WHITE:
                    print('WHITE MOVED, n = ' + str(n))
                else:
                    print('BLACK MOVED, n = ' + str(n))
                n += 1
                self.chessboard = principal_variation[1]
                self.chessboard.draw()

                print('Resulting score: ' + str(self.chessboard.evaluate()))
                print('New zobrist number: ' + str(self.chessboard.zobrist_number))
                
                flagline = 'En passant flags: '
                for f in range(8):
                    flagline += str(self.chessboard.en_passant_flag(f))

                flagline += '   Castling flags (wq, wk, bq, bk): ' 
                
                if self.chessboard.castling_queen_side_flag(WHITE):
                    flagline += '1'
                else:
                    flagline += '0'
                
                if self.chessboard.castling_king_side_flag(WHITE):
                    flagline += '1'
                else:
                    flagline += '0'
                   
                if self.chessboard.castling_queen_side_flag(BLACK):
                    flagline += '1'
                else:
                    flagline += '0'

                if self.chessboard.castling_king_side_flag(BLACK):
                    flagline += '1'
                else:
                    flagline += '0'
                    

                print(flagline)
                
                print('')

                if playing_color == WHITE:
                    playing_color = BLACK
                else:
                    playing_color = WHITE


                
            



