from PyQt5.QtGui import QImage
from PyQt5.QtWidgets import QFileDialog


class IOManager:
    filters = "PNG (*.png);;JPG (*.jpg)"
    _saveAsImageString = 'Save image as...'

    def __init__(self, file_path=None):
        self.current_file_path = file_path

    @staticmethod
    def _quickSaveQImage(image, path):
        image.save(path)

    def saveAsQImage(self, widget, image):
        name = QFileDialog.getSaveFileName(widget, self._saveAsImageString, filter=self.filters)
        path = name[0]
        self.current_file_path = path
        self._quickSaveQImage(image, path)

    def saveQImage(self, widget, image):
        if self.current_file_path is None:
            self.saveAsQImage(widget, image)
        else:
            self._quickSaveQImage(image, self.current_file_path)
