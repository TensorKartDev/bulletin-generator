# DescriptionDialog.py
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QTextEdit, QPushButton
import os

class DescriptionDialog(QDialog):
    def __init__(self, image_path, parent=None):
        super().__init__(parent)
        self.image_path = image_path
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Add Description")
        self.setModal(True)

        layout = QVBoxLayout()

        self.label = QLabel(f"Add description for {os.path.basename(self.image_path)}")
        layout.addWidget(self.label)

        self.text_edit = QTextEdit(self)
        layout.addWidget(self.text_edit)

        self.submit_button = QPushButton("Submit")
        self.submit_button.clicked.connect(self.submit)
        layout.addWidget(self.submit_button)

        self.setLayout(layout)

    def submit(self):
        description = self.text_edit.toPlainText()
        annotation_file = f"{self.image_path}.annotation.txt"
        with open(annotation_file, 'a+') as file:
            file.write(description)
        self.accept()
