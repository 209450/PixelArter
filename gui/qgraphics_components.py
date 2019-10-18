import numpy
from PyQt5.QtCore import QRectF
from PyQt5.QtGui import QPainter, QPen, QColor, QBrush
from PyQt5.QtWidgets import QGraphicsScene, QGraphicsRectItem, QGraphicsView
from PyQt5 import QtCore


class PixelGridScene(QGraphicsScene):
    zoom = {'value': 1, 'ratio': 0.1}
    default_pixel_size = 50

    def __init__(self, graphic_view, h, w):
        super().__init__()
        self.graphic_view = graphic_view
        self.setBackgroundBrush(QColor(0, 0, 0, 0))
        self.pixels = numpy.empty((h, w), dtype=Pixel)
        self.make_pixel_grid(h, w)

    def make_pixel_grid(self, h, w):
        size = self.default_pixel_size
        for i in range(h):
            for j in range(w):
                pixel = Pixel(QRectF(j * size, i * size, size, size), Pixel.default_color)
                self.pixels[i, j] = pixel
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

        wheel_change_angle = event.delta()

        zoom = self.zoom
        change_value = zoom['ratio'] if wheel_change_angle > 0 else -zoom['ratio']
        zoom_value = zoom['value'] + change_value

        self.graphic_view.scale(zoom_value, zoom_value)
        self.graphic_view.centerOn(x, y)


class Pixel(QGraphicsRectItem):
    default_color = QColor(79, 75, 64)

    def __init__(self, rect, qColor):
        super().__init__(rect)
        self.change_fulfillment(qColor)

    def change_fulfillment(self, color):
        self.color = color
        self.brush = QBrush(color)

    def paint(self, painter, QStyleOptionGraphicsItem, widget=None):
        painter.setBrush(self.brush)
        painter.drawRect(self.rect())
