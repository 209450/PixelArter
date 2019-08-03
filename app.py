import sys
from gui.main_window import MainWindow
from PyQt5.QtWidgets import QApplication


class App(QApplication):
  
    def __init__(self, argv):
        super().__init__(argv)
        main_window = MainWindow()
        main_window.show()
        self.main_window = main_window

if __name__ == "__main__":
    app = App(sys.argv)
    sys.exit(app.exec_())
