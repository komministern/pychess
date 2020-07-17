
from PySide2 import QtCore, QtWidgets, QtGui

class ChessBoardScene(QtWidgets.QGraphicsScene):

    def __init__(self, *args, **kwargs):
        super(ChessBoardScene, self).__init__(*args, **kwargs)

        self.setBackgroundBrush(QtGui.QBrush(QtCore.Qt.lightGray))

        self.current_hover_square = None
        self.previous_hover_square = None

        self.drag_in_progress = False

    def mousePressEvent(self, event):

        # Hmmmmmmmmmmmmmmmm....
        
        super(ChessBoardScene, self).mousePressEvent(event)
    
    #def mouseReleaseEvent(self, event):
    #    if self.drag_in_progress:

    def get_square(self, event):
        squares = [square for square in self.items(event.scenePos()) if square.__class__.__name__ == 'Square']
        if len(squares) > 0:
            return squares[0]
        else:
            return None



    def mouseMoveEvent(self, event):

        if self.drag_in_progress:

            squares = [square for square in self.items(event.scenePos()) if square.__class__.__name__ == 'Square']
        
            if len(squares) > 0:
                new_square = squares[0]
            
                if new_square != self.current_hover_square:
                    # If the pointed to square differs from the last recorded pointed to square (current_hover_square): 
                    self.previous_hover_square = self.current_hover_square
                    self.current_hover_square = new_square
                    # Mark current_hover_square, if a piece is beeing dragged at the moment
                    self.current_hover_square.mark()
                    # If previous_hover_square exists, unmark it
                    if self.previous_hover_square != None:
                        self.previous_hover_square.unmark()
            else:
                new_square = None
                if new_square != self.current_hover_square:
                    # If the mouse pointer exits the board, unmark the marked square, and nothing else.
                    self.current_hover_square.unmark()
                    self.current_hover_square = None
                    self.previous_hover_square = None
        
        super(ChessBoardScene, self).mouseMoveEvent(event)