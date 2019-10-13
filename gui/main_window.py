from PyQt5 import QtCore
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QMainWindow, QWidget, QDialog, QLabel, QHBoxLayout
from gui.widgets import PixelsContainerWidget, WidgetFromFile, NewFileDialog
from gui.io_manager import IOManager
import os


class MainWindow(QMainWindow, WidgetFromFile):
    ui_path = 'gui/uis/MainWindow.ui'

    def __init__(self):
        super().__init__()
        self.loadUI(self.ui_path)
        self.pixelContainer = PixelsContainerWidget(0, 0, 8, 16)
        self.mdiArea.addSubWindow(self.pixelContainer)
        self.initEvents()
        self.io = IOManager()

    def initEvents(self):
        self.actionSave.triggered.connect(self.actionSaveHandler)
        self.actionSaveAs.triggered.connect(self.actionSaveAsHandler)
        self.actionNewFile.triggered.connect(self.actionNewFileHandler)
        self.actionOpenFile.triggered.connect(self.actionOpenFileHandler)

    def actionSaveHandler(self):
        self.io.saveQImage(self, self.pixelContainer.convertPixelsToQImage())

    def actionSaveAsHandler(self):
        self.io.saveAsQImage(self, self.pixelContainer.convertPixelsToQImage())

    def actionNewFileHandler(self):
        dialog = NewFileDialog()
        result = dialog.exec()
        if result:
            self.pixelContainer.makeEmptyPixelGrid(dialog.user_chosen_height,dialog.user_chosen_width)

    def actionOpenFileHandler(self):
        self.pixelContainer.convertQImageToPixels(self.io.openQImageFromFile(self))
