from PyQt5 import QtCore
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QMainWindow, QWidget, QDialog, QLabel, QHBoxLayout
from gui.widgets import PixelsContainerWidget, WidgetFromFile, NewFileDialog
from gui.io_manager import IOManager
from gui.qgraphics_components import PixelGridScene
import os


class MainWindow(QMainWindow, WidgetFromFile):
    ui_path = 'gui/uis/MainWindow.ui'
    title = 'PixelEditor'

    def __init__(self):
        super().__init__()
        self.loadUI(self.ui_path)
        self.setWindowTitle(self.title)
        self.pixelGridScene = PixelGridScene(self.pixelGridView, 4, 16)
        self.pixelGridView.setScene(self.pixelGridScene)
        self.initEvents()
        self.io = IOManager()

    def initEvents(self):
        self.actionSave.triggered.connect(self.actionSaveHandler)
        self.actionSaveAs.triggered.connect(self.actionSaveAsHandler)
        self.actionNewFile.triggered.connect(self.actionNewFileHandler)
        self.actionOpenFile.triggered.connect(self.actionOpenFileHandler)

    def actionSaveHandler(self):
        self.io.saveQImage(self, self.pixelGridScene.convertPixelGridToQImage())

    def actionSaveAsHandler(self):
        self.io.saveAsQImage(self, self.pixelGridScene.convertPixelGridToQImage())

    def actionNewFileHandler(self):
        dialog = NewFileDialog()
        result = dialog.exec()
        if result:
            self.pixelGridScene = PixelGridScene(self.pixelGridView, dialog.user_chosen_height,
                                                 dialog.user_chosen_width)
            self.pixelGridView.setScene(self.pixelGridScene)

    def actionOpenFileHandler(self):
        scene = PixelGridScene.pixelGridFromQImage(self.pixelGridView, self.io.openQImageFromFile(self))
        self.pixelGridView.setScene(scene)
