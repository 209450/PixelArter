from PyQt5.QtCore import QRectF
from PyQt5.QtGui import QPainter, QPen
from PyQt5.QtWidgets import QGraphicsScene, QGraphicsRectItem, QGraphicsView
from PyQt5 import QtCore


class PixelGridScene(QGraphicsScene):

    def __init__(self, graphic_view, h, w):
        super().__init__()
        self.graphic_view = graphic_view
        self.setBackgroundBrush(QtCore.Qt.green)
        # self.addRect(QRectF(0, 0, 50, 50), brush=QtCore.Qt.blue)
        self.pixelQPainter = QPainter()
        pixel = Pixel(QtCore.Qt.blue)
        pixel.setRect(QRectF(0, 50, 100, 100))
        self.addItem(pixel)

    def mousePressEvent(self, event):
        x = event.scenePos().x()
        y = event.scenePos().y()
        print(x, y)
        print(self.itemAt(x, y, self.graphic_view.transform()))

    def wheelEvent(self, event):
        x = event.scenePos().x()
        y = event.scenePos().y()
        self.graphic_view.scale(5, 5)
        self.graphic_view.centerOn(x, y)


class Pixel(QGraphicsRectItem):
    def __init__(self, qColor):
        super().__init__()
        self.qColor = qColor

    def paint(self, painter, QStyleOptionGraphicsItem, widget=None):
        # super().paint(painter, QStyleOptionGraphicsItem, widget)
        painter.setPen(QPen(self.qColor))
        painter.drawRect(self.rect())
