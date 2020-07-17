#!python
# -*- coding: utf-8 -*-

#    Copyright © 2016, 2017, 2018 Oscar Franzén <oscarfranzen@protonmail.com>
#
#    This file is part of GCA Analysis Tool.


import sys
import logging
from PySide2 import QtWidgets
from view.view import MyView
from presenter.presenter import MyPresenter
#from model.model import MyModel
from model.gamehandler import GameHandler

logger = logging.getLogger(__name__)    # Ok here?
#logging.config.fileConfig('logging.ini', disable_existing_loggers=False)

if __name__ == '__main__':

    #multiprocessing.freeze_support()

    #logger = logging.getLogger(__name__)

    app = QtWidgets.QApplication(sys.argv)
    model = GameHandler()
    #model = MyModel()
    view = MyView() 
    presenter = MyPresenter(model, view, app)
    view.show()

    sys.exit(app.exec_())
