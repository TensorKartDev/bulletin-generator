import sys
import fitz  # PyMuPDF
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QToolBar, QScrollArea, QToolBar, QGraphicsView, QLabel, QGraphicsScene, QFileDialog, QGraphicsRectItem,QGraphicsPixmapItem,QStatusBar
from PyQt6.QtGui import QImage, QPixmap, QPainter,QAction, QIcon
from PyQt6.QtCore import QRect, QRectF, Qt,pyqtSignal
from PDFGenerators import ImageToPDF
from PyQt6.QtCore import *
from PyQt6.QtGui import *

from paddleocr import PaddleOCR,draw_ocr
# import event
import os, os.path
from InteractiveGraphicsView import InteractiveGraphicsView
MOST_RECENT_FILE = None
MOST_RECENT_TIME = 0

class PDFViewer(QWidget):
    def __init__(self):
        super().__init__()
        self.doc = None
        self.currentPage = 0
        self.initUI()
        self.capturing = False
        self.selectedtopic = ""
        self.pages = []
        # self.ocr = PaddleOCR(use_angle_cls=True, lang='en')

    def initUI(self):
        self.layout = QVBoxLayout(self)
        def add_toolbar(self):
            # Tool bar for actions like zoom and page navigation
            self.toolBar = QToolBar("PDF Tools", self)
            self.layout.addWidget(self.toolBar)

            # Add actions to the toolbar
            self.prevPageAction = QAction('Previous Page', self)
            self.nextPageAction = QAction('Next Page', self)
            # Action for building topics 
            self.getTopicsAction = QAction("Build Topics", self)
            self.toolBar.addAction(self.getTopicsAction)

            # Action for generating new bulletin from topics topics 
            self.buildBulletinAction = QAction("Build New Bulletin", self)
            self.toolBar.addAction(self.buildBulletinAction)

            self.pageLabel = QLabel("Page: 0/0")
            self.toolBar.addAction(self.prevPageAction)
            self.toolBar.addAction(self.nextPageAction)
            self.toolBar.addWidget(self.pageLabel)

            self.prevPageAction.triggered.connect(self.prevPage)
            self.nextPageAction.triggered.connect(self.nextPage)
            self.getTopicsAction.triggered.connect(self.getTopics)
            self.buildBulletinAction.triggered.connect(self.buildBulletin)
            self.statusBar = QStatusBar()
            # self.setStatusBar(self.statusBar)

            # # Scroll area to hold the graphics view
            # self.scrollArea = QScrollArea(self)
            # self.scrollArea.setWidgetResizable(True)
            # self.scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
            # self.scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)

        # Buttons for actions
        
        add_toolbar(self)
        # self.btncreate_new_bulletin = QPushButton('Create a new bulletin ', self)
        # self.layout.addWidget(self.btncreate_new_bulletin)
        # self.btncreate_new_bulletin.clicked.connect(self.new_bulletin)

        self.btnOpen = QPushButton('Open the input pdf file and start model topics ', self)
        self.btnOpen.clicked.connect(self.openFile)
        self.layout.addWidget(self.btnOpen)
        
        # Graphics view to display PDF
        self.scene = QGraphicsScene(self)
        self.graphicsView = InteractiveGraphicsView(self.scene, self)
        # self.graphicsView.mouseRelease
        
        self.layout.addWidget(self.graphicsView)
        self.setGeometry(100, 100, 800, 600)
        self.setWindowTitle('Topic Modeller')
        
        # self.graphicsView.valueChanged.connect(self.mouseReleaseEvent)  # Connect the signal to the slot
        # self.graphicsView.pixmapCropped.connect(self.handleCroppedPixmap)  # Connect the signal to the slot

        self.graphicsView.pixmapCropped.connect(self.handleCroppedPixmap)
        
        self.show()

    
    
    def handleCroppedPixmap(self, pixmap):
        topic = self.selectedtopic 
        try:

            # print("Topic : ", self.selectedtopic)
            recent_file = self.selectedtopic.most_recent_file
            # print("most recent file ", recent_file)
            # print("File number",str(self.selectedtopic.next_file_index))

            path_to_save = f"{self.selectedtopic.path}/{str(self.selectedtopic.next_file_index)}.png"
            high_res_pixmap = pixmap.scaled(pixmap.width() * 1, pixmap.height() * 1, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            #self.label.Text = self.selectedtopic.split("/")[-1]
            success = high_res_pixmap.save(path_to_save, 'PNG', 100)
            print(success)
            if self.graphicsView.rubberBand :
                print('From Viewer Crop area defined:', self.graphicsView.rubberBand.rect())
        except Exception as e:
            print(e)
    def new_bulletin(self):
        build_left_panel = True
        print("New bulletin clicked open left panel")
        return
    
    def getTopics(self):
        a = 4
        print("Getting topics from pdf file")

    def buildBulletin(self):
        print("Starting to build bulletin from given json file")
    def openFile(self):
        path, _ = QFileDialog.getOpenFileName(self, "Open file", "", "PDF files (*.pdf);;")
        if path:

            self.loadPDF(path)

    def loadPDF(self, path):
        self.doc = fitz.open(path)
        zoom = 1.0  # Adjust this factor to increase the rendering resolution
        new_size_matrix = fitz.Matrix(zoom, zoom)
        #load all pages at once
        self.deepload(new_size_matrix)
        pageno = 0
        self.currentPage = pageno
        self.showPage(self.currentPage)

    def prevPage(self):
        if self.currentPage > 0:
            self.currentPage -= 1
            self.showPage(self.currentPage)

    def nextPage(self):
        if self.doc and self.currentPage < self.doc.page_count - 1:
            self.currentPage += 1
            self.showPage(self.currentPage)
    def updatePageLabel(self):
        if self.doc:
            self.pageLabel.setText(f"Page: {self.currentPage + 1}/{self.doc.page_count}")

    def deepload(self, size_matrix):
        if self.doc:
            for i in range(self.doc.page_count):
                # if i > 0:
                    page = self.doc.load_page(i)
                    pix = page.get_pixmap(matrix=size_matrix)
                    img = QImage(pix.samples, pix.width, pix.height, pix.stride, QImage.Format.Format_RGB888)
                    self.pages.append(img)
            #print(len(self.pages))

    def showPage(self, page_number):
        if self.doc and len(self.pages) != 0:
            img = self.pages[page_number-1]
            self.scene.clear()
            self.scene.addPixmap(QPixmap.fromImage(img))
            #self.btnScreenshot.setEnabled(True)

