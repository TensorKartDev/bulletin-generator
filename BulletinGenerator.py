from PyQt6.QtWidgets import QWidget,QHBoxLayout,QSplitter,QApplication,QToolBar
from PDFViewer import PDFViewer
import sys,os
from FileDirectoryExplorer import FileDirectoryExplorer
from PyQt6.QtCore import QDir, Qt
from dotenv import load_dotenv
load_dotenv()
default_root_path = os.getenv('DEFAULT_LOCATION_FOR_TOPIC_COLLECTION', QDir.rootPath())
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

        self.setWindowTitle(os.environ["APP_TITLE"])
        self.setGeometry(100, 100, 1200, 600)
        self.file_explorer.topicNodeClicked.connect(self.handleTopicChanged)
        
        self.show()
        # print()

    def handleTopicChanged(self, topic):
        print("From Bulletin generator", topic)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    try:
        main_viewer = MainViewer()
    except:
        main_viewer = MainViewer()
    sys.exit(app.exec())