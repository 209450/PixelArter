import numpy
from PyQt5.QtCore import QRectF
from PyQt5.QtGui import QPainter, QPen, QColor, QBrush, QImage
from PyQt5.QtWidgets import QGraphicsScene, QGraphicsRectItem, QGraphicsView
from PyQt5 import QtCore

from gui.drawing_modes import DrawingModeStrategy


class PixelGridScene(QGraphicsScene):
    zoom = {'value': 1, 'ratio': 0.1}
    pixel_size = 50
    background_color = QColor(0, 0, 0, 0)
    first_color = QColor(0, 0, 255, 255)
    second_color = QColor(255, 0, 0, 255)

    def __init__(self, graphic_view, height, width):
        super().__init__()
        self.graphic_view = graphic_view
        self.setBackgroundBrush(self.background_color)
        self.pixels = numpy.empty((height, width), dtype=Pixel)
        self._makePixelGrid(height, width)
        self.current_drawing_mode = DrawingModeStrategy()

    @classmethod
    def pixelGridFromQImage(cls, graphic_view, image):
        new_grid = PixelGridScene(graphic_view, image.height(), image.width())
        new_grid.modifyPixels(lambda x, i, j: x.changeFulfillment(image.pixelColor(j, i)))
        return new_grid

    def _makePixelGrid(self, height, width):
        size = self.pixel_size
        for i in range(height):
            for j in range(width):
                pixel = Pixel(QRectF(j * size, i * size, size, size), Pixel.default_color)
                self.pixels[i, j] = pixel
                self.addItem(pixel)

    def changeDrawingMode(self, mode):
        self.current_drawing_mode = mode

    def mousePressEvent(self, event):
        self.current_drawing_mode.mousePress(self, event)
        self.update()

    def mouseReleaseEvent(self, event):
        self.current_drawing_mode.mouseRelease(self, event)
        self.update()

    def mouseMoveEvent(self, event):
        self.current_drawing_mode.mouseMove(self, event)
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
        self.modifyPixels(lambda x, i, j: image.setPixelColor(j, i, x.getCurrentColor()))
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
        self.color = qColor
        self.brush = QBrush(qColor)
        self.color_state = self.color

    def changeFulfillment(self, color):
        self.color = color
        self.brush = QBrush(color)

    def getCurrentColor(self):
        return self.color

    def stateCurrentColor(self):
        self.color_state = QColor(self.color)

    def applyStatedColor(self):
        self.changeFulfillment(self.color_state)

    def paint(self, painter, QStyleOptionGraphicsItem, widget=None):
        painter.setBrush(self.brush)
        painter.drawRect(self.rect())
