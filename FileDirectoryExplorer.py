from PyQt6.QtWidgets import QVBoxLayout,QWidget,QTreeView
from PyQt6.QtCore import QDir, Qt,pyqtSignal
from PyQt6.QtGui import QFileSystemModel

class FileDirectoryExplorer(QWidget):
    topicNodeClicked = pyqtSignal(str)

    def __init__(self, pdf_viewer):
        super().__init__()
        self.pdf_viewer = pdf_viewer
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout(self)
        
        self.treeView = QTreeView(self)
        self.model = QFileSystemModel()
        self.model.setRootPath(QDir.rootPath())
        self.treeView.setModel(self.model)
        self.treeView.setColumnHidden(1, True)
        self.treeView.setColumnHidden(2, True)
        self.treeView.setColumnHidden(3, True)

        self.treeView.clicked.connect(self.onTreeClicked)
        layout.addWidget(self.treeView)

    def onTreeClicked(self, index):
        path = self.model.filePath(index)
        self.topicNodeClicked.emit(path)
        self.pdf_viewer.selectedtopic = path
        if path.endswith('.pdf'):
            self.pdf_viewer.loadPDF(path)