import sys
import fitz  # PyMuPDF
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QGraphicsView, QGraphicsScene, QFileDialog, QGraphicsRectItem,QGraphicsPixmapItem
from PyQt6.QtGui import QImage, QPixmap, QPainter
from PyQt6.QtCore import QRect, QRectF, Qt,pyqtSignal
# import event
from InteractiveGraphicsView import InteractiveGraphicsView
class PDFViewer(QWidget):
    def __init__(self):
        super().__init__()
        self.doc = None
        self.currentPage = 0
        self.initUI()
        self.capturing = False
        self.selectedtopic = None

    def initUI(self):
        layout = QVBoxLayout(self)

        # Buttons for actions
        self.btncreate_new_bulletin = QPushButton('Create a new bulletin ', self)
        layout.addWidget(self.btncreate_new_bulletin)
        self.btncreate_new_bulletin.clicked.connect(self.new_bulletin)

        self.btnOpen = QPushButton('Open the input pdf file and start modelling ', self)
        self.btnOpen.clicked.connect(self.openFile)
        layout.addWidget(self.btnOpen)
        
        # Graphics view to display PDF
        self.scene = QGraphicsScene(self)
        self.graphicsView = InteractiveGraphicsView(self.scene, self)
        # self.graphicsView.mouseRelease
        
        
        
        # layout.addWidget(self.btnScreenshot)
        layout.addWidget(self.graphicsView)

        self.setGeometry(100, 100, 800, 600)
        self.setWindowTitle('Topic Modeller')
        
        # self.graphicsView.valueChanged.connect(self.mouseReleaseEvent)  # Connect the signal to the slot
        # self.graphicsView.pixmapCropped.connect(self.handleCroppedPixmap)  # Connect the signal to the slot

        self.graphicsView.pixmapCropped.connect(self.handleCroppedPixmap)
        self.show()

    def handleCroppedPixmap(self, pixmap):
        print("signal intrcepted")
        path_to_save = f"{self.selectedtopic}/output_image.png"
        success = pixmap.save(path_to_save, 'PNG', 100)
        print(success)
        if self.graphicsView.rubberBand :
            print('From Viewer Crop area defined:', self.graphicsView.rubberBand.rect())

    def new_bulletin(self):
        build_left_panel = True
        print("New bulletin clicked open left panel")
        return
    def openFile(self):
        path, _ = QFileDialog.getOpenFileName(self, "Open file", "", "PDF files (*.pdf);;")
        if path:
            self.loadPDF(path)

    def loadPDF(self, path):
        self.doc = fitz.open(path)
        self.showPage(self.currentPage)

    def showPage(self, page_number):
        if self.doc:
            print(page_number)
            page = self.doc.load_page(page_number)
            pix = page.get_pixmap()
            img = QImage(pix.samples, pix.width, pix.height, pix.stride, QImage.Format.Format_RGB888)
            self.scene.clear()
            self.scene.addPixmap(QPixmap.fromImage(img))
            #self.btnScreenshot.setEnabled(True)

