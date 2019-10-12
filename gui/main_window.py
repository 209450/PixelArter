from PyQt5 import QtCore
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QMainWindow, QWidget, QDialog, QLabel, QHBoxLayout
from gui.widgets import PixelsContainerWidget, WidgetFromFile
from gui.io_manager import IOManager
import os


class MainWindow(QMainWindow, WidgetFromFile):
    ui_path = 'gui/uis/MainWindow.ui'

    def __init__(self):
        super().__init__()
        self.laod_ui(self.ui_path)
        self.pixelContainer = PixelsContainerWidget(0, 0, 8, 16)
        self.mdiArea.addSubWindow(self.pixelContainer)
        self.initEvents()
        self.io = IOManager()

    def initEvents(self):
        self.actionSave.triggered.connect(self.actionSaveHandler)
        self.actionSaveAs.triggered.connect(self.actionSaveAsHandler)

    def actionSaveHandler(self):
        self.io.saveQImage(self, self.pixelContainer.convertPixelsToQImage())

    def actionSaveAsHandler(self):
        self.io.saveAsQImage(self, self.pixelContainer.convertPixelsToQImage())
