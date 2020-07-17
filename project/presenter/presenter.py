#!python
# -*- coding: utf-8 -*-

#    Copyright © 2016, 2017, 2018 Oscar Franzén <oscarfranzen@protonmail.com>
#
#    This file is part of GCA Analysis Tool.

from pathlib import Path
from PySide2 import QtCore, QtGui

class MyPresenter(QtCore.QObject):

    create_game = QtCore.Signal(object, object)
    #start_game = QtCore.Signal()



    def __init__(self, model, view, app):
        super(MyPresenter, self).__init__()

        # Store view and model.
        self.model = model
        self.view = view
        self.app = app

        self.init_chessboard()

        #self.populate_chessboard()
        
        self.connect_signals()

        self.new_game()

        #allowed_moves = ['e2-e3', 'e2-e4']
        #self.view.chessBoard.enable_human_move('white', allowed_moves, self.human_move_made)
    
    #def test(self):
    #    print('fita')

    def connect_signals(self):

        #self.model.test_signal.connect(self.test)
        
        self.view.quit.connect(self.model.quit_)    # quit_ not to conflict with QThread.quit method.
        self.view.pushButton_flip.pressed.connect(self.flip_chessboard)
        self.view.pushButton_start.pressed.connect(self.new_game)
        
        self.view.chessBoard.legal_move_made.connect(self.human_move_made)
        self.view.chessBoard.legal_move_made.connect(self.model.human_move_received)

        self.create_game.connect(self.model.create_game)
        
        self.model.request_human_move.connect(self.get_human_move)
        #self.model.execute_computer_move_on_screen.connect(self.execute_computer_move)
        #self.model.clear_square_on_screen.connect(self.clear_square)

        self.model.update_chessboard_view.connect(self.update_chessboard)
    

    def execute_computer_move(self, move):
        self.view.chessBoard.execute_move(move)

    def clear_square(self, coord):
        self.view.chessBoard.delete_piece(coord)
        

    def update_chessboard(self, board_representation):
        self.view.chessBoard.update_complete_board(board_representation)


    def new_game(self):

        self.reset_chessboard()
        self.populate_chessboard()

        #self.white_is_computer = self.view.radioButton_white_computer.isChecked()
        #self.black_is_computer = self.view.radioButton_black_computer.isChecked()
        #self.white_is_computer = False
        #self.black_is_computer = False

        self.create_game.emit(True, False)  # human, computer


    def get_next_move(self, color=None):

        if color:
            self.now_playing = color
        else:
            if self.now_playing == 'white':
                self.now_playing = 'black'
            else:
                self.now_playing = 'white'

        if self.now_playing == 'white':
            if self.white_is_computer:
                self.get_computer_move('white')
            else:
                self.get_human_move('white')
        else:
            if self.black_is_computer:
                self.get_computer_move('black')
            else:
                self.get_human_move('black')

    def get_computer_move(self, color):
        #chessengine.calculate_move(color)
        self.view.chessBoard.enable_human_move(color, [])

    def get_human_move(self, color, allowed_moves):
        #allowed_moves = chessengine.get_all_legal_moves(color)
        #print('get human move...')
        #print('allowed: ' + repr(allowed_moves))
        self.view.chessBoard.enable_human_move(color, allowed_moves)
        self.view.plainTextEdit_status.appendPlainText(color + ' to move...')
        #print(color + ' is moving')

    def computer_move_made(self, move):
        self.view.plainTextEdit_status.appendPlainText(move)
        self.get_next_move()

    def human_move_made(self, move):
        self.view.plainTextEdit_status.appendPlainText(move)
        #self.get_next_move()

    def reset_chessboard(self):
        self.view.chessBoard.delete_all_pieces()
        #chessengine.reset()
        
    def populate_chessboard(self):

        self.view.chessBoard.add_piece('pawn', 'white', 'a2')
        self.view.chessBoard.add_piece('pawn', 'white', 'b2')
        self.view.chessBoard.add_piece('pawn', 'white', 'c2')
        self.view.chessBoard.add_piece('pawn', 'white', 'd2')
        self.view.chessBoard.add_piece('pawn', 'white', 'e2')
        self.view.chessBoard.add_piece('pawn', 'white', 'f2')
        self.view.chessBoard.add_piece('pawn', 'white', 'g2')
        self.view.chessBoard.add_piece('pawn', 'white', 'h2')

        self.view.chessBoard.add_piece('rook', 'white', 'a1')
        self.view.chessBoard.add_piece('knight', 'white', 'b1')
        self.view.chessBoard.add_piece('bishop', 'white', 'c1')
        self.view.chessBoard.add_piece('queen', 'white', 'd1')
        self.view.chessBoard.add_piece('king', 'white', 'e1')
        self.view.chessBoard.add_piece('bishop', 'white', 'f1')
        self.view.chessBoard.add_piece('knight', 'white', 'g1')
        self.view.chessBoard.add_piece('rook', 'white', 'h1')

        self.view.chessBoard.add_piece('pawn', 'black', 'a7')
        self.view.chessBoard.add_piece('pawn', 'black', 'b7')
        self.view.chessBoard.add_piece('pawn', 'black', 'c7')
        self.view.chessBoard.add_piece('pawn', 'black', 'd7')
        self.view.chessBoard.add_piece('pawn', 'black', 'e7')
        self.view.chessBoard.add_piece('pawn', 'black', 'f7')
        self.view.chessBoard.add_piece('pawn', 'black', 'g7')
        self.view.chessBoard.add_piece('pawn', 'black', 'h7')

        self.view.chessBoard.add_piece('rook', 'black', 'a8')
        self.view.chessBoard.add_piece('knight', 'black', 'b8')
        self.view.chessBoard.add_piece('bishop', 'black', 'c8')
        self.view.chessBoard.add_piece('queen', 'black', 'd8')
        self.view.chessBoard.add_piece('king', 'black', 'e8')
        self.view.chessBoard.add_piece('bishop', 'black', 'f8')
        self.view.chessBoard.add_piece('knight', 'black', 'g8')
        self.view.chessBoard.add_piece('rook', 'black', 'h8')

    def init_chessboard(self):

        white_pawn_path = Path.cwd() / 'resources' / 'pieces' / 'Chess_plt60.png'
        white_pawn_pixmap = QtGui.QPixmap()
        white_pawn_pixmap.load(str(white_pawn_path))
        black_pawn_path = Path.cwd() / 'resources' / 'pieces' / 'Chess_pdt60.png'
        black_pawn_pixmap = QtGui.QPixmap()
        black_pawn_pixmap.load(str(black_pawn_path))

        white_rook_path = Path.cwd() / 'resources' / 'pieces' / 'Chess_rlt60.png'
        white_rook_pixmap = QtGui.QPixmap()
        white_rook_pixmap.load(str(white_rook_path))
        black_rook_path = Path.cwd() / 'resources' / 'pieces' / 'Chess_rdt60.png'
        black_rook_pixmap = QtGui.QPixmap()
        black_rook_pixmap.load(str(black_rook_path))

        white_knight_path = Path.cwd() / 'resources' / 'pieces' / 'Chess_nlt60.png'
        white_knight_pixmap = QtGui.QPixmap()
        white_knight_pixmap.load(str(white_knight_path))
        black_knight_path = Path.cwd() / 'resources' / 'pieces' / 'Chess_ndt60.png'
        black_knight_pixmap = QtGui.QPixmap()
        black_knight_pixmap.load(str(black_knight_path))

        white_bishop_path = Path.cwd() / 'resources' / 'pieces' / 'Chess_blt60.png'
        white_bishop_pixmap = QtGui.QPixmap()
        white_bishop_pixmap.load(str(white_bishop_path))
        black_bishop_path = Path.cwd() / 'resources' / 'pieces' / 'Chess_bdt60.png'
        black_bishop_pixmap = QtGui.QPixmap()
        black_bishop_pixmap.load(str(black_bishop_path))

        white_queen_path = Path.cwd() / 'resources' / 'pieces' / 'Chess_qlt60.png'
        white_queen_pixmap = QtGui.QPixmap()
        white_queen_pixmap.load(str(white_queen_path))
        black_queen_path = Path.cwd() / 'resources' / 'pieces' / 'Chess_qdt60.png'
        black_queen_pixmap = QtGui.QPixmap()
        black_queen_pixmap.load(str(black_queen_path))

        white_king_path = Path.cwd() / 'resources' / 'pieces' / 'Chess_klt60.png'
        white_king_pixmap = QtGui.QPixmap()
        white_king_pixmap.load(str(white_king_path))
        black_king_path = Path.cwd() / 'resources' / 'pieces' / 'Chess_kdt60.png'
        black_king_pixmap = QtGui.QPixmap()
        black_king_pixmap.load(str(black_king_path))

        self.view.chessBoard.init_chess_pieces(white_pawn_pixmap, black_pawn_pixmap, white_rook_pixmap, black_rook_pixmap,
                                                white_knight_pixmap, black_knight_pixmap, white_bishop_pixmap, black_bishop_pixmap,
                                                white_queen_pixmap, black_queen_pixmap, white_king_pixmap, black_king_pixmap)

    def flip_chessboard(self):
        self.view.chessBoard.flip_board()



    