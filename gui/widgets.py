import PyQt5

from PyQt5.QtWidgets import QWidget, QGridLayout, QPushButton, QDialog, QErrorMessage, QMessageBox
from PyQt5.QtGui import QPainter, QColor, QPen, QBrush, QTransform, QImage, QIntValidator
from PyQt5 import QtCore, uic
from PyQt5.QtCore import QPoint, QRect, QLine
import numpy as np


class WidgetFromFile:
    def loadUI(self, ui_path):
        uic.loadUi(ui_path, self)


class PixelsContainerWidget(QWidget):
    zoom_ratio = 50
    background_color = QtCore.Qt.darkGray
    alpha_color = QtCore.Qt.transparent

    def __init__(self, x, y, h, w):
        super().__init__()
        self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint)
        self.makeEmptyPixelGrid(h, w)
        self.qp = QPainter(self)
        self.setAutoFillBackground(True)
        p = self.palette()
        p.setColor(self.backgroundRole(), self.background_color)
        self.setPalette(p)

    def makeEmptyPixelGrid(self, h, w):
        self.pixels = np.array([[Pixel(self.alpha_color, QPoint(j, i))
                                 for i in range(h)] for j in range(w)])
        self.setMinimumHeight(h * self.zoom_ratio)
        self.setMinimumWidth(w * self.zoom_ratio)
        self.repaint()

    def mousePressEvent(self, event):
        x = event.pos().x()
        y = event.pos().y()
        print('{},{}'.format(x, y))

        r = self.pixels[int(x / self.zoom_ratio), int(y / self.zoom_ratio)]
        r.color = QColor(0, 0, 255)

        print("{},{}".format(r.point.x(), r.point.y()))
        self.repaint()

    def wheelEvent(self, QWheelEvent):
        wheel_change_angle = QWheelEvent.angleDelta() / 8
        print(QWheelEvent.pos())
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
                qp.fillRect(empty_rect, j.color)
                qp.drawRect(empty_rect)

    def convertPixelsToQImage(self):
        pixels = self.pixels
        image = QImage(pixels.shape[0], pixels.shape[1], QImage.Format_RGB32)
        for row in pixels:
            for col in row:
                image.setPixelColor(col.point, col.color)
        return image

    def makePixelGridFromQImage(self, image):
        height = image.height()
        width = image.width()
        pixels = np.empty([height, width], dtype=Pixel)
        for row in range(height):
            for col in range(width):
                pixels[row, col] = Pixel(image.pixelColor(col, row), QPoint(col, row))
        self.pixels = pixels
        self.repaint()

    def convertQImageToPixels(self, image):
        if not image.isNull():
            self.makePixelGridFromQImage(image)


class Pixel:
    def __init__(self, color, point):
        self.color = color
        self.point = point


class NewFileDialog(QDialog, WidgetFromFile):
    new_file_dialog = 'gui/uis/NewFileDialog.ui'
    error_message = 'Values are not valid!'
    window_title = 'New File'
    height_range = [1, 1000]
    width_range = [1, 1000]

    def __init__(self):
        super().__init__()
        self.user_chosen_height = -1
        self.user_chosen_width = -1
        self.loadUI(self.new_file_dialog)
        self.setWindowTitle(self.window_title)

        self.initLineEditValidation()
        self.initEvents()

    def initLineEditValidation(self):
        self.heightLineEdit.setValidator(QIntValidator(self.height_range[0], self.height_range[1], self))
        self.widthLineEdit.setValidator(QIntValidator(self.width_range[0], self.width_range[1], self))
        self.heightLabel.setText("{} {}".format(self.heightLabel.text(), self.height_range))
        self.widthLabel.setText("{} {}".format(self.widthLabel.text(), self.width_range))

    def initEvents(self):
        self.createButton.clicked.connect(self.createButtonHandler)
        self.cancelButton.clicked.connect(self.cancelButtonHandler)

    def createButtonHandler(self):
        if self.heightLineEdit.hasAcceptableInput() and self.widthLineEdit.hasAcceptableInput():
            self.user_chosen_height = int(self.heightLineEdit.text())
            self.user_chosen_width = int(self.widthLineEdit.text())
            print("in", self.user_chosen_height, self.user_chosen_width)
            self.accept()
        else:
            box = QMessageBox(self)
            box.setWindowTitle(self.window_title)
            box.setIcon(QMessageBox.Critical)
            box.setText(self.error_message)
            box.exec()

    def cancelButtonHandler(self):
        self.reject()

