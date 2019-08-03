from PyQt5 import uic

class Window():
    def laod_ui(self, ui_path):
        uic.loadUi(ui_path, self)
