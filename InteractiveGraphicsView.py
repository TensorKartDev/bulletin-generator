from PyQt6.QtWidgets import QRubberBand
import sys
from PyQt6.QtWidgets import QGraphicsView,QGraphicsRectItem,QGraphicsPixmapItem
from PyQt6.QtCore import QRect,QSize
from PyQt6.QtGui import QImage, QPixmap, QPainter
from PyQt6.QtCore import QRect, QRectF, Qt,pyqtSignal


class InteractiveGraphicsView(QGraphicsView):
    # Define a signal that emits a QPixmap
    pixmapCropped = pyqtSignal(QPixmap)

    def __init__(self, scene, parent=None):
        super().__init__(scene, parent)
        self.scene = scene
        self.setMouseTracking(True)
        self.rubberBand = None
        self.origin = None
        self.createRubberBand()
    
    def createRubberBand(self):
        # Ensure there's no existing rubberBand before creating a new one
        if self.rubberBand is not None:
            self.scene.removeItem(self.rubberBand)
            self.rubberBand = None
        self.rubberBand = QGraphicsRectItem()
        self.rubberBand.setPen(Qt.GlobalColor.red)
        self.scene.addItem(self.rubberBand)
        self.rubberBand.hide()  # Hide it initially
    
    def clearSceneSafely(self):
        if self.rubberBand:
            self.scene.removeItem(self.rubberBand)
            self.rubberBand = None
        self.scene.clear()
        self.createRubberBand()  # Recreate the rubberBand after clearing

    def mousePressEvent(self, event):
        self.origin = self.mapToScene(event.position().toPoint())
        if not self.rubberBand:
            print("No rubber band")
            self.rubberBand = QGraphicsRectItem()
            self.rubberBand.setPen(Qt.GlobalColor.blue)
            self.scene.addItem(self.rubberBand)
        try:  
            self.rubberBand.show()
            self.rubberBand.setRect(self.origin.x(), self.origin.y(), 0, 0)
        except:
            print("Error - recreating")
            self.rubberBand = QGraphicsRectItem()
            self.rubberBand.setPen(Qt.GlobalColor.blue)
            self.scene.addItem(self.rubberBand)

        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self.rubberBand and self.origin:
            to = self.mapToScene(event.position().toPoint())
            try:
                self.rubberBand.setRect(min(self.origin.x(), to.x()), min(self.origin.y(), to.y()),
                                    abs(self.origin.x() - to.x()), abs(self.origin.y() - to.y()))
            except:
                print("Error - clearing scene")
                self.rubberBand = QGraphicsRectItem()
                self.rubberBand.setPen(Qt.GlobalColor.blue)
                self.scene.addItem(self.rubberBand)
                self.rubberBand.setRect(min(self.origin.x(), to.x()), min(self.origin.y(), to.y()),
                                    abs(self.origin.x() - to.x()), abs(self.origin.y() - to.y()))
                

        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if not self.rubberBand.isVisible():
            return super().mouseReleaseEvent(event)
        
        if self.rubberBand:
            rect = self.rubberBand.rect().toRect()
            
            pixmap_item = self.scene.items()[1]  # Assuming the first item is the pixmap item

            if isinstance(pixmap_item, QGraphicsPixmapItem):
                # Crop the pixmap based on the rubber band's rectangle
                cropped_pixmap = pixmap_item.pixmap().copy(rect)
                self.pixmapCropped.emit(cropped_pixmap)  # Emit the cropped pixmap
                # print(rect)
            self.rubberBand.hide()
        super().mouseReleaseEvent(event)