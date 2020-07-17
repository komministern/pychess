
from PySide2 import QtCore, QtWidgets, QtGui

from .scene import ChessBoardScene
from .chesspiece import ChessPiece
from .boardsquare import Square

class QChessBoard(QtWidgets.QGraphicsView):

    legal_move_made = QtCore.Signal(object)
    start_game = QtCore.Signal(object, object)

    def get_tile_rect(self, coord):
        if self.white_at_bottom:
            vcoords = '87654321'
            hcoords = 'abcdefgh'
        else:
            vcoords = '12345678'
            hcoords = 'hgfedcba'
        return QtCore.QRectF(hcoords.index(coord[0]) * self.square_size + self.margin_size + 0.5,
                            vcoords.index(coord[1]) * self.square_size + self.margin_size + 0.5,
                            self.square_size - 1.0, self.square_size - 1.0)

    def __init__(self, *args, **kwargs):
        super(QChessBoard, self).__init__(*args, **kwargs)

        self.coord_marking_text_items = []

        self.chess_piece_pixmaps = {}

        self.allowed_moves = []
        self.moving_color = None

        self.square_at_coord = {}
        self.chess_piece_at_coord = {}

        self.white_at_bottom = True
        self.animations_on = False

        self.square_size = 60
        self.margin_size = self.square_size / 3
        self.dot_size = self.square_size / 4

        self.chess_square_Z_value = 0
        self.marked_chess_square_Z_value = 1
        self.possible_move_dot_Z_value = 15
        self.chess_piece_Z_value = 10
        self.dragged_chess_piece_Z_value = 20

        self.chessboard_scene = ChessBoardScene(0, 0, self.square_size * 8 + self.margin_size * 2, 
                                                self.square_size * 8 + self.margin_size * 2)
        self.setScene(self.chessboard_scene)

        self.create_squares()
        self.create_coordinate_markings()


        # Should find larger png pics of chess pieces....
        dx, dy = 1.0, 1.0
        transform_scale = QtGui.QTransform.fromScale(dx, dy)
        transform_rotate = QtGui.QTransform()
        transform_rotate.rotate(180)
        #self.setTransform(transform_rotate)

        #self.timer = QtCore.QTimer()
        #self.timer.setInterval(1000)
        #self.timer.timeout.connect(self.test)
        #self.timer.start()
    
    #def test(self):
    #    print(self.moving_color)


    def create_possible_move_dots(self, from_coord):
        possible_coords = [move[3:] for move in [move for move in self.allowed_moves if move[:2] == from_coord]]
        self.possible_move_dots = []
        for coord in possible_coords:
            position = self.square_at_coord[coord].boundingRect().center() - QtCore.QPointF(self.dot_size/2, self.dot_size/2)
            dot = QtWidgets.QGraphicsEllipseItem(position.x(), position.y(), self.dot_size, self.dot_size)
            dot.setBrush(QtGui.QBrush(QtCore.Qt.green))
            dot.setZValue(self.possible_move_dot_Z_value)
            self.possible_move_dots.append(dot)
            self.scene().addItem(dot)


    def delete_possible_move_dots(self):
        for dot in self.possible_move_dots:
            self.scene().removeItem(dot)
        self.possible_move_dots = []

    
    def add_piece(self, piece_type, color, at_coord):
        chess_piece = ChessPiece(self, at_coord, color, piece_type, self.chess_piece_pixmaps[(color, piece_type)])
        chess_piece.setPixmap(self.chess_piece_pixmaps[color, piece_type])
        self.chess_piece_at_coord[at_coord] = chess_piece

    def execute_move(self, move):
        from_coord = move[:2]
        to_coord = move[3:]
        if to_coord in self.chess_piece_at_coord.keys():
            self.delete_piece(to_coord)
        #piece_to_be_moved = self.chess_piece_at_coord[from_coord]
        #piece_to_be_moved.move_to_chess_coordinate(to_coord)
        self.move_piece(from_coord, to_coord)

    def delete_all_pieces(self):
        for item in self.scene().items():
            if item.__class__.__name__ == 'ChessPiece':
                self.scene().removeItem(item)
        self.chess_piece_at_coord = {}

    def delete_piece(self, from_coord):
        self.scene().removeItem(self.chess_piece_at_coord[from_coord])
        del self.chess_piece_at_coord[from_coord]

    def move_piece(self, from_coord, to_coord):
        piece_to_be_moved = self.chess_piece_at_coord[from_coord]
        piece_to_be_moved.move_to_chess_coordinate(to_coord)
        self.chess_piece_at_coord[to_coord] = piece_to_be_moved
        del self.chess_piece_at_coord[from_coord]



    def update_complete_board(self, board_representation):

        updated_pieces, chess_flags = board_representation
        
        all_coords = []
        for letter in ('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'):
            for number in ('1', '2', '3', '4', '5', '6', '7', '8'):
                all_coords.append(''.join((letter, number)))

        for coord in all_coords:

            if coord in updated_pieces.keys():
                updated_piece_type, updated_piece_color = updated_pieces[coord]
                if self.get_piece(coord):
                    if not (self.get_piece(coord).color == updated_piece_color and self.get_piece(coord).type == updated_piece_type):
                        self.delete_piece(coord)
                        self.add_piece(updated_piece_type, updated_piece_color, coord)
                else:
                    self.add_piece(updated_piece_type, updated_piece_color, coord)
            elif self.get_piece(coord):
                self.delete_piece(coord)



    def get_piece(self, at_coord):
        if at_coord in self.chess_piece_at_coord.keys():
            return self.chess_piece_at_coord[at_coord]
        else:
            return None


    def init_chess_pieces(self, wpawnpixmap, bpawnpixmap, wrookpixmap, brookpixmap, wknightpixmap, bknightpixmap, 
                            wbishoppixmap, bbishoppixmap, wqueenpixmap, bqueenpixmap, wkingpixmap, bkingpixmap):
        
        self.chess_piece_pixmaps[('white', 'pawn')] = wpawnpixmap
        self.chess_piece_pixmaps[('black', 'pawn')] = bpawnpixmap
        self.chess_piece_pixmaps[('white', 'rook')] = wrookpixmap
        self.chess_piece_pixmaps[('black', 'rook')] = brookpixmap
        self.chess_piece_pixmaps[('white', 'knight')] = wknightpixmap
        self.chess_piece_pixmaps[('black', 'knight')] = bknightpixmap
        self.chess_piece_pixmaps[('white', 'bishop')] = wbishoppixmap
        self.chess_piece_pixmaps[('black', 'bishop')] = bbishoppixmap
        self.chess_piece_pixmaps[('white', 'queen')] = wqueenpixmap
        self.chess_piece_pixmaps[('black', 'queen')] = bqueenpixmap
        self.chess_piece_pixmaps[('white', 'king')] = wkingpixmap
        self.chess_piece_pixmaps[('black', 'king')] = bkingpixmap

        #print(wpawnpixmap.rect())

    def create_coordinate_markings(self):
        if self.white_at_bottom:
            vcoords = '87654321'
            hcoords = 'ABCDEFGH'
        else:
            vcoords = '12345678'
            hcoords = 'HGFEDCBA'

        for v in vcoords:
            vertical_coord_text_item = QtWidgets.QGraphicsSimpleTextItem()
            vertical_coord_text_item.setText(v)
            coord_bounding_rect = vertical_coord_text_item.boundingRect()
            vertical_coord_text_item.setPos(self.margin_size*0.5 - coord_bounding_rect.width()*0.5,
                                             self.margin_size + self.square_size*(vcoords.index(v) + 0.5) - coord_bounding_rect.height()*0.5)
            
            self.coord_marking_text_items.append(vertical_coord_text_item)
            self.scene().addItem(vertical_coord_text_item)

        for h in hcoords:
            horizontal_coord_text_item = QtWidgets.QGraphicsSimpleTextItem()
            horizontal_coord_text_item.setText(h)
            coord_bounding_rect = horizontal_coord_text_item.boundingRect()
            horizontal_coord_text_item.setPos(self.margin_size + self.square_size*(hcoords.index(h) + 0.5) - coord_bounding_rect.width()*0.5,
                                             self.margin_size*1.5 + self.square_size*8 - coord_bounding_rect.height()*0.5)
            
            self.coord_marking_text_items.append(horizontal_coord_text_item)
            self.scene().addItem(horizontal_coord_text_item)

    def delete_coordinate_markings(self):
        for item in [item for item in self.scene().items() if item in self.coord_marking_text_items]:
            self.scene().removeItem(item)
        self.coord_text_items = []

    def create_squares(self):
        for h in 'abcdefgh':
            for v in '12345678':
                coord = ''.join((h, v))
                square = Square(self, coord, self.get_tile_rect(coord))
                self.square_at_coord[coord] = square
                #self.board_squares[coord] = square
                self.scene().addItem(square)

    def update_squares(self):
        for square in [item for item in self.scene().items() if item.__class__.__name__ == 'Square']:
            square.setRect(self.get_tile_rect(square.get_coord()))
    
    def update_pieces(self):
        for chess_piece in [item for item in self.scene().items() if item.__class__.__name__ == 'ChessPiece']:
            chess_piece.move_to_chess_coordinate(chess_piece.coord) 

    def flip_board(self):
        if self.white_at_bottom == True:
            self.white_at_bottom = False
        else: 
            self.white_at_bottom = True    
        self.update_squares()
        self.update_pieces()
        self.delete_coordinate_markings()
        self.create_coordinate_markings()

        

    def enable_human_move(self, color, allowed_moves):

        #print('it is happening')

        #print(color + ' ' + self.moving_color)
        self.moving_color = color
        self.allowed_moves = allowed_moves
        #print(color + ' ' + self.moving_color)
        #self.return_function = return_function
    
    def human_move_made(self, move):            # More should happen here................

        self.disable_human_move()

        self.execute_move(move)

        #print('JESYS')

        self.legal_move_made.emit(move)

        #self.return_function(move)
        #self.disable_human_move()

    def disable_human_move(self):
        self.moving_color = None
        self.allowed_moves = []
    


    





    
