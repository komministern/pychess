
# -*- coding: utf-8 -*-

#    Copyright © 2016, 2017, 2018 Oscar Franzén <oscarfranzen@protonmail.com>
#
#    This file is part of GCA Analysis Tool.

import logging
from PySide2 import QtCore, QtWidgets
from .gamehandler import GameHandler

logger = logging.getLogger(__name__)

class MyModel(QtCore.QObject):

    def __init__(self):
        super(MyModel, self).__init__()
        
        self.game_handler = GameHandler()

    def quit(self):
        QtWidgets.QApplication.quit()
