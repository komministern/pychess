#!python
# -*- coding: utf-8 -*-

#    Copyright © 2016, 2017, 2018 Oscar Franzén <oscarfranzen@protonmail.com>
#
#    This file is part of GCA Analysis Tool.

from PySide2 import QtCore, QtWidgets
from view.ui_mainwindow import Ui_MainWindow

class MyView(QtWidgets.QMainWindow, Ui_MainWindow):

    quit = QtCore.Signal()

    def __init__(self):
        super(MyView, self).__init__()
        self.setupUi(self)

    def closeEvent(self, event):
        event.ignore()
        self.quit.emit() 
