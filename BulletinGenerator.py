from PyQt6.QtWidgets import QWidget,QHBoxLayout,QSplitter,QApplication,QToolBar
from PDFViewer import PDFViewer
import sys
from FileDirectoryExplorer import FileDirectoryExplorer
from PyQt6.QtCore import QDir, Qt
class MainViewer(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.layout = QHBoxLayout(self)
        self.splitter = QSplitter(Qt.Orientation.Horizontal)

        self.pdf_viewer = PDFViewer()
        self.file_explorer = FileDirectoryExplorer(self.pdf_viewer)

        self.splitter.addWidget(self.file_explorer)
        self.splitter.addWidget(self.pdf_viewer)
        self.layout.addWidget(self.splitter)

        self.setWindowTitle('Bulletin Generator')
        self.setGeometry(100, 100, 1200, 600)
        self.file_explorer.topicNodeClicked.connect(self.handleTopicChanged)
        self.show()
    def handleTopicChanged(self, topic):
        print("From Bulletin generator", topic)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_viewer = MainViewer()
    sys.exit(app.exec())