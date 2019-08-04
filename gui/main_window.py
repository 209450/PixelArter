from PyQt5.QtWidgets import QMainWindow, QWidget
from gui.widgets import PixelsContainerWidget, WidgetFromFile

class MainWindow(QMainWindow, WidgetFromFile):
    ui_path = 'gui/uis/MainWindow.ui'

    def __init__(self):
        super().__init__()
        self.laod_ui(self.ui_path)
        # print(self.mdiArea)
        self.mdiArea.addSubWindow(PixelsContainerWidget(10,5))