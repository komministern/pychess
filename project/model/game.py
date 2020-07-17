
import logging
import time

from PySide2 import QtCore, QtWidgets

from .chessengine import chessengine
from .player import HumanPlayer, ComputerPlayer

logger = logging.getLogger(__name__)

WHITE = 1
BLACK = -1

class Game(QtCore.QObject):

    #request_human_move = QtCore.Signal(object, object)
    wait_no_more = QtCore.Signal()
    #execute_computer_move_on_screen = QtCore.Signal(object)

    def __init__(self, handler, white_is_human, black_is_human):
        super(Game, self).__init__()
        
        self.handler = handler

        self.state = 'idle'

        self.white_is_human = white_is_human
        self.black_is_human = black_is_human


    def initialize_white_player(self, is_human=True, chess_engine_parameters=None):
        pass

    def initialize_black_player(self, is_human=True, chess_engine_parameters=None):
        pass

    def initialize_chessboard(self):
        pass

    def abandon(self):
        
        # send signal to stop chess engine
        # send signal to chessboard view to 
        pass


    def pause(self):
        self.state = 'idle'
        pass
        # make sure that computer finishes its move, and signal I guess


    def restart(self):
        self.state = 'playing'
        self.loop()

    def human_move_received(self, move):
        # Pass move to chess engine and continue
        self.received_human_move = move
        #print('so far so good')
        self.wait_no_more.emit()
        #print(move)

        #self.flip_playing_color()
        #self.loop()

    #def computer_move_received(self, move):
    #    pass

    def process(self):

        if not self.white_is_human:
            print('white chess engine created')
            self.white_chessengine = chessengine.ChessEngine()

        if not self.black_is_human:
            print('black chess engine created')
            self.black_chessengine = chessengine.ChessEngine()

        self.playing_color = 'white'
        self.state = 'playing'

        self.chessengine = chessengine.ChessEngine()

        self.chessengine.chessboard.draw()

        

        #moves = self.chessengine.get_all_allowed_moves('white')
        
        #print('allowed moves: ' + repr(moves))
        
        self.game_loop()

    def flip_playing_color(self):
        if self.playing_color == 'white':
            self.playing_color = 'black'
        else:
            self.playing_color = 'white'

    def game_loop(self):
        
        print('starting game loop')

        while self.state == 'playing':

            if self.playing_color == 'white':

                if self.white_is_human:
                    print('white human is playing')

                    allowed_moves = self.chessengine.get_all_allowed_moves(self.playing_color)
                    self.handler.get_human_move(self.playing_color, allowed_moves)

                    loop = QtCore.QEventLoop()
                    self.wait_no_more.connect(loop.quit)
                    loop.exec_()
                    
                    self.chessengine.register_move(self.received_human_move)

                    if not self.black_is_human:
                        self.black_chessengine.register_move(self.received_human_move)

                else:
                    print('white computer is playing')
                    
                    computer_move = self.white_chessengine.get_next_move(self.playing_color)

                    self.chessengine.register_move(computer_move)
                    
                    #self.handler.execute_computer_move_on_screen.emit(computer_move)

                    if not self.black_is_human:
                        self.black_chessengine.register_move(computer_move)


            elif self.playing_color == 'black':

                if self.black_is_human:
                    print('black human is playing')

                    allowed_moves = self.chessengine.get_all_allowed_moves(self.playing_color)
                    self.handler.get_human_move(self.playing_color, allowed_moves)

                    loop = QtCore.QEventLoop()
                    self.wait_no_more.connect(loop.quit)
                    loop.exec_()

                    self.chessengine.register_move(self.received_human_move)

                    if not self.white_is_human:
                        self.white_chessengine.register_move(self.received_human_move)

                else:
                    print('black computer is playing')

                    computer_move = self.black_chessengine.get_next_move(self.playing_color)

                    self.chessengine.register_move(computer_move)
                    
                    if not self.white_is_human:
                        self.white_chessengine.register_move(computer_move)
    

            self.handler.update_chessboard_view.emit(self.chessengine.current_board_representation())

            # Check if game is over here I guess.

            self.flip_playing_color()

            if len(self.chessengine.get_all_allowed_moves(self.playing_color)) == 0:
                if self.chessengine.king_is_under_attack(self.playing_color):
                    print('VICTORY!')
                else:
                    print('DRAW.')
                self.state = 'idle'

        #elif self.state == 'idle':
        #    pass 

