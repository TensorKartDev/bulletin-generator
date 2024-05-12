from PyQt6.QtWidgets import QVBoxLayout,QWidget,QTreeView
from PyQt6.QtCore import QDir, Qt,pyqtSignal
from PyQt6.QtGui import QFileSystemModel
from dotenv import load_dotenv
from Topic import Topic
import os
load_dotenv()
# root_path = os.environ["DEFAULT_LOCATION_FOR_TOPIC_COLLECTION"]
default_root_path = os.getenv('DEFAULT_LOCATION_FOR_TOPIC_COLLECTION', QDir.rootPath())
class FileDirectoryExplorer(QWidget):
    topicNodeClicked = pyqtSignal(Topic)
    MOST_RECENT_TIME = 0
    MOST_RECENT_FILE = None
    def __init__(self, pdf_viewer):
        super().__init__()

        self.pdf_viewer = pdf_viewer
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout(self)
        self.treeView = QTreeView(self)
        self.model = QFileSystemModel()
        
        self.treeView.setModel(self.model)
        
        self.treeView.setRootIndex(self.model.index(default_root_path))
        self.model.setRootPath(default_root_path)
        
        self.treeView.setColumnHidden(1, True)
        self.treeView.setColumnHidden(2, True)
        self.treeView.setColumnHidden(3, True)

        self.treeView.clicked.connect(self.onTreeClicked)
        layout.addWidget(self.treeView)
    def most_recent(self,index):
        MOST_RECENT_TIME = 0 
        MOST_RECENT_FILE = None
        # iterate over the files in the directory using os.scandir
        for entry in os.scandir(self.model.filePath(index)):
            if entry.is_file():
                if entry.path.split(".")[-1] == "png":
                    # get the modification time of the file using entry.stat().st_mtime_ns
                    mod_time = entry.stat().st_mtime_ns
                
                    if mod_time > MOST_RECENT_TIME:
                    # update the most recent file and its modification time
                        MOST_RECENT_FILE = entry.name
                        MOST_RECENT_TIME = mod_time
                
        return MOST_RECENT_FILE, MOST_RECENT_TIME
    def onTreeClicked(self, index):
        try:
            # print(index, type(index))
            file_path = self.model.filePath(index)
            file_title = self.model.fileName(index)
            MOST_RECENT_FILE, MOST_RECENT_TIME = self.most_recent(index)

            topic = Topic(title=file_title, path=file_path,most_recent_file=MOST_RECENT_FILE, most_recent_time=MOST_RECENT_TIME )
            #print(file_path)
            #path = self.model.filePath(file_path)
            self.topicNodeClicked.emit(topic)
            self.pdf_viewer.selectedtopic = topic
        except:
            print("Not a directory")
            return False