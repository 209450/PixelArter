import numpy
from PyQt5.QtCore import QRectF
from PyQt5.QtGui import QPainter, QPen, QColor, QBrush, QImage
from PyQt5.QtWidgets import QGraphicsScene, QGraphicsRectItem, QGraphicsView
from PyQt5 import QtCore


class PixelGridScene(QGraphicsScene):
    zoom = {'value': 1, 'ratio': 0.1}
    default_pixel_size = 50
    background_color = QColor(0, 0, 0, 0)

    def __init__(self, graphic_view, height, width):
        super().__init__()
        self.graphic_view = graphic_view
        self.setBackgroundBrush(self.background_color)
        self.pixels = numpy.empty((height, width), dtype=Pixel)
        self._makePixelGrid(height, width)

    @classmethod
    def pixelGridFromQImage(cls, graphic_view, image):
        new_grid = PixelGridScene(graphic_view, image.height(), image.width())
        new_grid.modifyPixels(lambda x, i, j: x.change_fulfillment(image.pixelColor(j, i)))
        return new_grid

    def _makePixelGrid(self, height, width):
        size = self.default_pixel_size
        for i in range(height):
            for j in range(width):
                pixel = Pixel(QRectF(j * size, i * size, size, size), Pixel.default_color)
                self.pixels[i, j] = pixel
                self.addItem(pixel)

    def mousePressEvent(self, event):
        x = event.scenePos().x()
        y = event.scenePos().y()
        pixel = self.itemAt(x, y, self.graphic_view.transform())
        pixel.change_fulfillment(QColor(0, 0, 255, 255))
        self.update()

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

    def convertPixelGridToQImage(self):
        pixels = self.pixels
        image = QImage(pixels.shape[1], pixels.shape[0], QImage.Format_RGB32)
        self.modifyPixels(lambda x, i, j: image.setPixelColor(j, i, x.get_current_color()))
        return image

    def modifyPixels(self, callback):
        pixels = self.pixels
        for i in range(pixels.shape[0]):
            for j in range(pixels.shape[1]):
                callback(pixels[i, j])

    def modifyPixels(self, callback):
        pixels = self.pixels
        for i in range(pixels.shape[0]):
            for j in range(pixels.shape[1]):
                callback(pixels[i, j], i, j)


class Pixel(QGraphicsRectItem):
    default_color = QColor(79, 75, 64)

    def __init__(self, rect, qColor):
        super().__init__(rect)
        self.change_fulfillment(qColor)

    def change_fulfillment(self, color):
        self.color = color
        self.brush = QBrush(color)

    def get_current_color(self):
        return self.color

    def paint(self, painter, QStyleOptionGraphicsItem, widget=None):
        painter.setBrush(self.brush)
        painter.drawRect(self.rect())
