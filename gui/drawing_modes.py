import numpy
from PyQt5.QtCore import QPointF, QLineF, Qt
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QGraphicsLineItem


class DrawingModeStrategy:
    def mouseMove(self, scene, event):
        pass

    def mousePress(self, scene, event):
        pass

    def mouseRelease(self, scene, event):
        print("ee"
              "")
        pass

    @staticmethod
    def colorPixel(scene, x, y, color):
        pixel = scene.itemAt(x, y, scene.graphic_view.transform())
        if pixel is not None:
            pixel.changeFulfillment(color)

    @staticmethod
    def leftButtonEvent(event, callback):
        if event.buttons() & Qt.LeftButton:
            callback()

    @staticmethod
    def rightButtonEvent(event, callback):
        if event.buttons() & Qt.RightButton:
            callback()


class PenMode(DrawingModeStrategy):

    def mouseMove(self, scene, event):
        self._drawPixels(scene, event)

    def mousePress(self, scene, event):
        self._drawPixels(scene, event)

    def _drawPixels(self, scene, event):
        leftButtonCallback = lambda: DrawingModeStrategy.colorPixel(scene, event.scenePos().x(), event.scenePos().y(),
                                                                    scene.first_color)
        DrawingModeStrategy.leftButtonEvent(event, leftButtonCallback)

        rightButtonCallback = lambda: DrawingModeStrategy.colorPixel(scene, event.scenePos().x(), event.scenePos().y(),
                                                                     scene.second_color)

        DrawingModeStrategy.rightButtonEvent(event, rightButtonCallback)


class LineMode(DrawingModeStrategy):

    def __init__(self):
        self.line = QLineF()
        self.line_obj = QGraphicsLineItem(self.line)
        self.affected_items = set()

    def mousePress(self, scene, event):
        start_pos = event.scenePos()

        self.line = QLineF(start_pos.x(), start_pos.y(), start_pos.x(), start_pos.y())
        self.line_obj = QGraphicsLineItem(self.line)
        self.affected_items = set()
        # line_obj.setPen(Qt.transparent)

        scene.addItem(self.line_obj)
        pass

    def mouseMove(self, scene, event):
        DrawingModeStrategy.leftButtonEvent(event, lambda: self._drawLine(event, scene, scene.first_color))
        DrawingModeStrategy.rightButtonEvent(event, lambda: self._drawLine(event, scene, scene.second_color))

    def _drawLine(self, event, scene, color):
        self._changeLinePosition(event, scene)
        self._setUpPixels(scene, color)

    def _changeLinePosition(self, event, scene):
        actual_pos = event.scenePos()
        line = self.line_obj.line()
        line.setP2(actual_pos)
        self.line_obj.setLine(line)

    def _setUpPixels(self, scene, color):
        colliding_items = set(self.line_obj.collidingItems())
        color_items = colliding_items - self.affected_items
        prev_color_items = self.affected_items - colliding_items
        self.affected_items = self.affected_items | colliding_items
        for i in color_items:
            i.stateCurrentColor()
            i.changeFulfillment(color)
        for i in prev_color_items:
            i.applyStatedColor()
            self.affected_items.remove(i)

    def mouseRelease(self, scene, event):
        scene.removeItem(self.line_obj)
        pass
