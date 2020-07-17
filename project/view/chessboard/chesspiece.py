
from PySide2 import QtCore, QtWidgets, QtGui

class ChessPiece(QtWidgets.QGraphicsPixmapItem):

    def __init__(self, chessboard, coord, color, piece_type, pixmap, *args, **kwargs):
        super(ChessPiece, self).__init__(*args, **kwargs)

        self.chessboard = chessboard
        self.color = color
        self.type = piece_type
        self.setPixmap(pixmap)
        self.move_to_chess_coordinate(coord)

        self.chessboard.scene().addItem(self)

        # All new pieces is placed outside the view. It will get its final position when it is given a coordinate.
        #self.setPos(-100.0, -100.0)

        self.drag = False

        self.setZValue(self.chessboard.chess_piece_Z_value)
        self.setShapeMode(QtWidgets.QGraphicsPixmapItem.MaskShape)

        self.setAcceptHoverEvents(True)
    
    def move_to_chess_coordinate(self, coord):
        self.coord = coord
        self.setPos(self.chessboard.get_tile_rect(coord).topLeft() - QtCore.QPointF(1.0, 1.0))


    def get_square(self, scene_position):
        possible_squares = [square for square in self.scene().items(scene_position) if type(square).__name__ == 'Square']
        
        if len(possible_squares) == 0:
            return None
        elif len(possible_squares) == 1:
            return possible_squares[0]
        else:
            print('This should NEVER happen!!!!')

    def center_scene_position(self):
        return self.scenePos() + QtCore.QPointF(30.0, 30.0)
        


    def hoverEnterEvent(self, event):
        #print('chess piece hover enter - ' + self.color + ' ' + self.chessboard.moving_color)
        if self.chessboard.moving_color == self.color:
            self.setCursor(QtCore.Qt.OpenHandCursor)
        super(ChessPiece, self).hoverEnterEvent(event)

    def hoverLeaveEvent(self, event):
        
        self.setCursor(QtCore.Qt.ArrowCursor)

    def mousePressEvent(self, event):
        
        if self.chessboard.moving_color == self.color:
            
            self.setCursor(QtCore.Qt.ClosedHandCursor)

            self.drag = True

            self.setZValue(self.chessboard.dragged_chess_piece_Z_value)

            self.scene().drag_in_progress = True

            

            #self.original_scene_pos = self.scenePos()
            
            self.original_square = self.get_square(event.scenePos())
            self.original_square.mark()

            self.chessboard.create_possible_move_dots(self.original_square.get_coord())
            #print('original square : ' + self.original_square.get_coord())
            
            self.grab_offset = event.pos()
            self.setPos(event.scenePos() - self.grab_offset)
        
        #super(ChessPiece, self).mousePressEvent(event)  #?
    
    def mouseMoveEvent(self, event):
        if self.drag:
            self.setPos(event.scenePos() - self.grab_offset)
        super(ChessPiece, self).mouseMoveEvent(event)
    
    def mouseReleaseEvent(self, event):
        if self.drag:

            self.setCursor(QtCore.Qt.OpenHandCursor)
            self.drag = False
            self.setZValue(self.chessboard.chess_piece_Z_value)
            self.scene().drag_in_progress = False

            self.chessboard.delete_possible_move_dots()

            new_square = self.get_square(event.scenePos())
        
            if new_square == None:
                
                self.move_to_chess_coordinate(self.original_square.get_coord())
                #print('illegal move')
            
            elif new_square == self.original_square:

                #print('no_move')
                self.original_square.unmark()
                self.move_to_chess_coordinate(self.original_square.get_coord())


            else:

                move = '-'.join((self.original_square.get_coord(), new_square.get_coord()))

                if move in self.chessboard.allowed_moves:

                    new_square.unmark()
                    
                    #self.move_to_chess_coordinate(new_square.get_coord())

                    self.chessboard.human_move_made(move)

                    self.setCursor(QtCore.Qt.ArrowCursor)

                else:

                    new_square.unmark()
                    self.move_to_chess_coordinate(self.original_square.get_coord())

                    # Delete these three lines and uncomment the one above!!!!
                    
                    #self.move_to_chess_coordinate(new_square.get_coord())
                    #self.chessboard.human_move_made(move)
                    #self.setCursor(QtCore.Qt.ArrowCursor)
                    



