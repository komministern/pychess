
from PySide2 import QtCore, QtWidgets, QtGui

class Square(QtWidgets.QGraphicsRectItem):

    def __init__(self, chessboard, coord, rect):
        super(Square, self).__init__(rect)

        self.chessboard = chessboard
        self.coord = coord

        hcoord = coord[0]
        vcoord = coord[1]
        
        if (hcoord in 'aceg' and vcoord in '1357') or (hcoord in 'bdfh' and vcoord in '2468'):
            self.color = 'black'
        else:
            self.color = 'white'

        self.localpen = QtGui.QPen()
        self.localpen.setWidth(0)
        self.localpen.setStyle(QtCore.Qt.NoPen)

        self.setZValue(self.chessboard.chess_square_Z_value)


        if self.color == 'black':
            self.localbrush = QtGui.QBrush(QtCore.Qt.gray)
        elif self.color == 'white':
            self.localbrush = QtGui.QBrush(QtCore.Qt.white)


    def get_coord(self):
        return self.coord

    def mark(self):
        self.localpen.setStyle(QtCore.Qt.SolidLine)
        self.setZValue(self.chessboard.marked_chess_square_Z_value)
    
    def unmark(self):
        self.localpen.setStyle(QtCore.Qt.NoPen)
        self.setZValue(self.chessboard.chess_square_Z_value)

    def paint(self, painter, option, widget):
        painter.setBrush(self.localbrush)
        painter.setPen(self.localpen)
        painter.drawRect(self.boundingRect())

    #def mousePressEvent(self, e):
        #print(self.get_coord())
    #    super(Square, self).mousePressEvent(e)

    #def hoverEnterEvent(self, event):
    #    print('square hover enter')
    #    self.localpen.setStyle(QtCore.Qt.SolidLine)
    #    self.setZValue(1)
    #    self.update()

    #def hoverLeaveEvent(self, event):
    #    print('square hover leave')
    #    self.localpen.setStyle(QtCore.Qt.NoPen)
    #    self.setZValue(0)
    #    self.update()

