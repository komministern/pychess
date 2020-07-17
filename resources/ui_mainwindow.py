# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_mainwindow.ui'
##
## Created by: Qt User Interface Compiler version 5.14.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import (QCoreApplication, QMetaObject, QObject, QPoint,
    QRect, QSize, QUrl, Qt)
from PySide2.QtGui import (QBrush, QColor, QConicalGradient, QFont,
    QFontDatabase, QIcon, QLinearGradient, QPalette, QPainter, QPixmap,
    QRadialGradient)
from PySide2.QtWidgets import *

import QChessBoard

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1035, 979)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout_4 = QGridLayout(self.centralwidget)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.chessBoard = QChessBoard(self.centralwidget)
        self.chessBoard.setObjectName(u"chessBoard")
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(2)
        sizePolicy1.setHeightForWidth(self.chessBoard.sizePolicy().hasHeightForWidth())
        self.chessBoard.setSizePolicy(sizePolicy1)
        self.chessBoard.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.chessBoard.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.chessBoard.setRubberBandSelectionMode(Qt.ContainsItemShape)

        self.gridLayout_4.addWidget(self.chessBoard, 0, 0, 3, 1)

        self.groupBox_3 = QGroupBox(self.centralwidget)
        self.groupBox_3.setObjectName(u"groupBox_3")
        sizePolicy2 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.groupBox_3.sizePolicy().hasHeightForWidth())
        self.groupBox_3.setSizePolicy(sizePolicy2)
        self.gridLayout_2 = QGridLayout(self.groupBox_3)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.radioButton_black_human = QRadioButton(self.groupBox_3)
        self.radioButton_black_human.setObjectName(u"radioButton_black_human")

        self.gridLayout_2.addWidget(self.radioButton_black_human, 0, 0, 1, 1)

        self.radioButton_black_computer = QRadioButton(self.groupBox_3)
        self.radioButton_black_computer.setObjectName(u"radioButton_black_computer")
        self.radioButton_black_computer.setChecked(True)

        self.gridLayout_2.addWidget(self.radioButton_black_computer, 1, 0, 1, 1)


        self.gridLayout_4.addWidget(self.groupBox_3, 0, 1, 1, 1)

        self.groupBox_2 = QGroupBox(self.centralwidget)
        self.groupBox_2.setObjectName(u"groupBox_2")
        sizePolicy2.setHeightForWidth(self.groupBox_2.sizePolicy().hasHeightForWidth())
        self.groupBox_2.setSizePolicy(sizePolicy2)
        self.gridLayout = QGridLayout(self.groupBox_2)
        self.gridLayout.setObjectName(u"gridLayout")
        self.radioButton_white_human = QRadioButton(self.groupBox_2)
        self.radioButton_white_human.setObjectName(u"radioButton_white_human")
        self.radioButton_white_human.setChecked(True)

        self.gridLayout.addWidget(self.radioButton_white_human, 0, 0, 1, 1)

        self.radioButton_white_computer = QRadioButton(self.groupBox_2)
        self.radioButton_white_computer.setObjectName(u"radioButton_white_computer")

        self.gridLayout.addWidget(self.radioButton_white_computer, 1, 0, 1, 1)


        self.gridLayout_4.addWidget(self.groupBox_2, 1, 1, 1, 1)

        self.groupBox = QGroupBox(self.centralwidget)
        self.groupBox.setObjectName(u"groupBox")
        self.gridLayout_3 = QGridLayout(self.groupBox)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.pushButton_flip = QPushButton(self.groupBox)
        self.pushButton_flip.setObjectName(u"pushButton_flip")

        self.gridLayout_3.addWidget(self.pushButton_flip, 0, 0, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 608, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout_3.addItem(self.verticalSpacer, 1, 0, 1, 1)

        self.pushButton_start = QPushButton(self.groupBox)
        self.pushButton_start.setObjectName(u"pushButton_start")

        self.gridLayout_3.addWidget(self.pushButton_start, 3, 0, 1, 1)

        self.pushButton_stop = QPushButton(self.groupBox)
        self.pushButton_stop.setObjectName(u"pushButton_stop")

        self.gridLayout_3.addWidget(self.pushButton_stop, 4, 0, 1, 1)


        self.gridLayout_4.addWidget(self.groupBox, 2, 1, 2, 1)

        self.plainTextEdit_status = QPlainTextEdit(self.centralwidget)
        self.plainTextEdit_status.setObjectName(u"plainTextEdit_status")
        self.plainTextEdit_status.setReadOnly(True)

        self.gridLayout_4.addWidget(self.plainTextEdit_status, 3, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1035, 26))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"PyChess", None))
        self.groupBox_3.setTitle(QCoreApplication.translate("MainWindow", u"Black", None))
        self.radioButton_black_human.setText(QCoreApplication.translate("MainWindow", u"Human", None))
        self.radioButton_black_computer.setText(QCoreApplication.translate("MainWindow", u"Computer", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("MainWindow", u"White", None))
        self.radioButton_white_human.setText(QCoreApplication.translate("MainWindow", u"Human", None))
        self.radioButton_white_computer.setText(QCoreApplication.translate("MainWindow", u"Computer", None))
        self.groupBox.setTitle(QCoreApplication.translate("MainWindow", u"Controls", None))
        self.pushButton_flip.setText(QCoreApplication.translate("MainWindow", u"Flip sides", None))
        self.pushButton_start.setText(QCoreApplication.translate("MainWindow", u"New Game", None))
        self.pushButton_stop.setText(QCoreApplication.translate("MainWindow", u"Stop Game", None))
    # retranslateUi

