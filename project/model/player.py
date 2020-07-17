
import logging
from PySide2 import QtCore, QtWidgets
from .chessengine.chessengine import ChessEngine

logger = logging.getLogger(__name__)

class Player(QtCore.QObject):

    def __init__(self):
        super(Player, self).__init__()

    def is_human(self):
        return False


class HumanPlayer(Player):
    
    def __init__(self):
        super(HumanPlayer, self).__init__()

    def is_human(self):
        return True
    
    def register_move(self, move):
        pass


class ComputerPlayer(Player, ChessEngine):

    def __init__(self):
        super(ComputerPlayer, self).__init__()
        #(Player, self).__init__()
        #(ChessEngine, self).__init__()

        print(dir(self))

        print('computer player initialized')

    #def register_move(self, move):
    #    print('-' + move)

    

    




    