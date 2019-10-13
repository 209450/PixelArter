from PyQt5.QtGui import QImage
from PyQt5.QtWidgets import QFileDialog


class IOManager:
    filters = "PNG (*.png);;JPG (*.jpg)"
    _saveAsImageString = 'Save image as...'
    _openFileString = 'Open file'

    def __init__(self, file_path=None):
        self.current_file_path = file_path

    def saveQImage(self, widget, image):
        if self.current_file_path is None:
            self.saveAsQImage(widget, image)
        else:
            self._quickSaveQImage(image, self.current_file_path)

    def saveAsQImage(self, widget, image):
        try:
            name = QFileDialog.getSaveFileName(widget, self._saveAsImageString, filter=self.filters)
            self._tryUpdateCurrentFilePathFromName(name)
            self._quickSaveQImage(image, self.current_file_path)
        except NameError:
            pass

    def openQImageFromFile(self, widget):
        try:
            name = QFileDialog.getOpenFileName(widget, self._openFileString, filter=self.filters)
            self._tryUpdateCurrentFilePathFromName(name)
            return QImage(self.current_file_path)
        except NameError:
            return QImage()

    def _tryUpdateCurrentFilePathFromName(self, name):
        path = name[0]
        if path:
            self.current_file_path = path
        else:
            raise NameError('No path')

    @staticmethod
    def _quickSaveQImage(image, path):
        image.save(path)
