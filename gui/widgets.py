import PyQt5

from PyQt5.QtWidgets import QWidget, QGridLayout, QPushButton
from PyQt5.QtGui import QPainter, QColor, QPen, QBrush, QTransform
from PyQt5 import QtCore, uic
from PyQt5.QtCore import QPoint, QRect, QLine
import numpy as np


class WidgetFromFile():
    def laod_ui(self, ui_path):
        uic.loadUi(ui_path, self)


class PixelsContainerWidget(QWidget):
    zoom_ratio = 50

    def __init__(self, x, y, h, w):
        super().__init__()
        self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint)
        self.makePixelGrid(x, y, h, w)
        self.qp = QPainter(self)

        self.setAutoFillBackground(True)
        p = self.palette()
        p.setColor(self.backgroundRole(), QtCore.Qt.blue)
        self.setPalette(p)

    def makePixelGrid(self, x, y, h, w):
        self.pixels = np.array([[self.Pixel(QColor(0, 255, 0), QPoint(j, i))
                                 for i in range(w)] for j in range(h)])
        print(self.pixels.shape)
        self.setMinimumHeight(self.zoom_ratio * h)
        self.setMinimumWidth(self.zoom_ratio * w)
        print("  gdsagsd {}".format(self.pixels[0, 0].point.x()))

        f = np.vectorize(lambda x: x.point.x())
        print(f(self.pixels))

    def mousePressEvent(self, event):
        x = event.pos().x()
        y = event.pos().y()
        print('{},{}'.format(x, y))

    def wheelEvent(self, QWheelEvent):
        wheel_change_angle = QWheelEvent.angleDelta() / 8
        if wheel_change_angle.y() > 0:
            self.zoom_ratio -= 2
        else:
            self.zoom_ratio += 2
        self.repaint()

    def paintEvent(self, event):
        self.qp.begin(self)
        self.qp.setPen(QPen(QtCore.Qt.green))
        self.drawPixelGrid(self.qp)
        self.qp.end()

    def drawPixelGrid(self, qp):
        zoom_ratio = self.zoom_ratio
        for i in self.pixels:
            for j in i:
                x = j.point.x()
                y = j.point.y()
                empty_rect = QRect(zoom_ratio * x, zoom_ratio * y, zoom_ratio, zoom_ratio)
                qp.drawRect(empty_rect)

    class Pixel:
        def __init__(self, color, point):
            self.color = color
            self.point = point

        def __str__(self):
            return "{}, {}, {}".format(self.color, self.point.x, self.point.y)
