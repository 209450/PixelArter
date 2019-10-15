from PyQt5.QtCore import QRectF
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QGraphicsScene, QGraphicsRectItem
from PyQt5 import QtCore


class PixelGridScene(QGraphicsScene):

    def __init__(self, graphic_view, h, w):
        super().__init__()
        self.graphic_view = graphic_view
        self.setBackgroundBrush(QtCore.Qt.green)
        self.addRect(QRectF(0, 0, 200, 50), brush=QtCore.Qt.blue)
        self.pixelQPainter = QPainter()

    def mousePressEvent(self, event):
        x = event.scenePos().x()
        y = event.scenePos().y()
        print(x, y)
        print(self.itemAt(x, y, self.graphic_view.transform()))


class Pixel(QGraphicsRectItem):
    def __init__(self):
        super().__init__()

    def paint(self, QPainter, QStyleOptionGraphicsItem, widget=None):
        super().paint(QPainter, QStyleOptionGraphicsItem, widget)
