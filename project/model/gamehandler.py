
import logging
from PySide2 import QtCore, QtWidgets

from .game import Game
from .player import HumanPlayer, ComputerPlayer

logger = logging.getLogger(__name__)

#class GameHandler(QtCore.QThread):
class GameHandler(QtCore.QObject):

    #test_signal = QtCore.Signal()

    #game_created = QtCore.Signal()
    request_human_move = QtCore.Signal(object, object)
    execute_computer_move_on_screen = QtCore.Signal(object)
    clear_square_on_screen = QtCore.Signal(object)

    update_chessboard_view = QtCore.Signal(object)

    def __init__(self):
        super(GameHandler, self).__init__()

        self.thread = QtCore.QThread()

        #self.create_game(True, True)
    
    def quit_(self):

        if self.game:
            self.save_game()
        
        self.thread.quit()
        QtWidgets.QApplication.quit()


    def create_game(self, white_is_human, black_is_human):

        #white_is_human = True
        #black_is_human = True

        if white_is_human:
            white_player = HumanPlayer()
        else:
            white_player = ComputerPlayer()

        if black_is_human:
            black_player = HumanPlayer()
        else:
            black_player = ComputerPlayer()

        #white_player.moveToThread(self)
        #black_player.moveToThread(self)

        self.game = Game(self, white_is_human, black_is_human)
        self.game.moveToThread(self.thread)
        
        self.thread.started.connect(self.game.process)

        #self.game_created.emit()

        self.thread.start()

    #def start_game(self):
    #    self.start()

    def get_human_move(self, color, allowed_moves):
        #print('hepp')
        self.request_human_move.emit(color, allowed_moves)


    def human_move_received(self, move):
        self.game.human_move_received(move)
        

    def save_game(self):
        pass

    def load_game(self):
        pass

    def abandon_game(self):
        self.started.disconnect(self.game.process)  # I guess
        pass

    #def test(self):
    #    print('kuk')
    #    self.test_signal.emit()


