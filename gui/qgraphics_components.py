from PyQt5.QtCore import QRectF
from PyQt5.QtGui import QPainter, QPen
from PyQt5.QtWidgets import QGraphicsScene, QGraphicsRectItem, QGraphicsView
from PyQt5 import QtCore


class PixelGridScene(QGraphicsScene):
    zoom = {'value': 1, 'ratio': 0.05}

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
        self.zoom_scene(event)

    def zoom_scene(self, event):
        x = event.scenePos().x()
        y = event.scenePos().y()

        zoom = self.zoom
        wheel_change_angle = event.delta()

        change_value = zoom['ratio'] if wheel_change_angle > 0 else -zoom['ratio']
        zoom_value = zoom['value'] + change_value

        self.graphic_view.scale(zoom_value, zoom_value)
        self.graphic_view.centerOn(x, y)


class Pixel(QGraphicsRectItem):
    def __init__(self, qColor):
        super().__init__()
        self.qColor = qColor

    def paint(self, painter, QStyleOptionGraphicsItem, widget=None):
        # super().paint(painter, QStyleOptionGraphicsItem, widget)
        painter.setPen(QPen(self.qColor))
        painter.drawRect(self.rect())
