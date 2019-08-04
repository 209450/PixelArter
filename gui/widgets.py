from PyQt5.QtWidgets import QWidget, QGridLayout, QPushButton
from PyQt5 import QtCore, uic

class WidgetFromFile():
    def laod_ui(self, ui_path):
        uic.loadUi(ui_path, self)


class PixelsContainerWidget(QWidget):
    def __init__(self,x, y):
        super().__init__()
        # self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint)
        self.setMinimumSize(100,100)
        self.makePixelGrid(x, y)

    def makePixelGrid(self, x, y):
        layout = QGridLayout()

        [layout.addWidget(QPushButton(),i,j) for i in range(x) for j in range(y)]
        

        self.setLayout(layout)