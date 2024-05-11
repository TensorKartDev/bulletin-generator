from PyQt6.QtWidgets import QRubberBand
import sys
from PyQt6.QtWidgets import QGraphicsView,QGraphicsRectItem,QGraphicsPixmapItem
from PyQt6.QtCore import QRect,QSize
from PyQt6.QtGui import QImage, QPixmap, QPainter
from PyQt6.QtCore import QRect, QRectF, Qt,pyqtSignal
# from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QGraphicsView, QGraphicsScene, QFileDialog, QGraphicsRectItem
# from PyQt6.QtGui import QImage, QPixmap, QPainter
# from PyQt6.QtCore import QRect, QRectF, Qt

class InteractiveGraphicsView(QGraphicsView):
    # Define a signal that emits a QPixmap
    pixmapCropped = pyqtSignal(QPixmap)

    def __init__(self, scene, parent=None):
        super().__init__(scene, parent)
        self.scene = scene
        self.setMouseTracking(True)
        self.rubberBand = None
        self.origin = None

    def mousePressEvent(self, event):
        self.origin = self.mapToScene(event.position().toPoint())
        if not self.rubberBand:
            self.rubberBand = QGraphicsRectItem()
            self.rubberBand.setPen(Qt.GlobalColor.blue)
            self.scene.addItem(self.rubberBand)
            self.rubberBand.show()
            self.rubberBand.setRect(self.origin.x(), self.origin.y(), 0, 0)
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self.rubberBand and self.origin:
            to = self.mapToScene(event.position().toPoint())
            try:

                self.rubberBand.setRect(min(self.origin.x(), to.x()), min(self.origin.y(), to.y()),
                                    abs(self.origin.x() - to.x()), abs(self.origin.y() - to.y()))
            except:
                print("Error")
                if not self.rubberBand:
                    self.rubberBand = QGraphicsRectItem()
                    self.rubberBand.setPen(Qt.GlobalColor.blue)
                    self.scene.addItem(self.rubberBand)
                    self.rubberBand.show()
                    self.rubberBand.setRect(self.origin.x(), self.origin.y(), 0, 0)
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if self.rubberBand:
            print("IN Called")
            rect = self.rubberBand.rect().toRect()
            print(len(self.scene.items()))
            pixmap_item = self.scene.items()[1]  # Assuming the first item is the pixmap item
            print(type(pixmap_item))
            if isinstance(pixmap_item, QGraphicsPixmapItem):
                print(rect)
                # Crop the pixmap based on the rubber band's rectangle
                cropped_pixmap = pixmap_item.pixmap().copy(rect)
                self.pixmapCropped.emit(cropped_pixmap)  # Emit the cropped pixmap
                # print(rect)
            self.rubberBand.hide()
        super().mouseReleaseEvent(event)