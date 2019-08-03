from gui.window import Window
from PyQt5.QtWidgets import QMainWindow


class MainWindow(QMainWindow, Window):
    ui_path = 'gui/uis/MainWindow.ui'

    def __init__(self):
        super().__init__()
        self.laod_ui(self.ui_path)
