# DescriptionDialog.py
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QTextEdit, QPushButton
import os
from paddleocr import PaddleOCR,draw_ocr

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

        self.ocr_button = QPushButton("Perform OCR")
        self.ocr_button.clicked.connect(self.doOCR)
        layout.addWidget(self.submit_button)
        layout.addWidget(self.ocr_button)

        self.setLayout(layout)
    def doOCR(self):
        image = self.image_path
        print(f"Performing OCR on {image}")
        ocr = PaddleOCR(use_angle_cls=True, lang='en')
        result = ocr.ocr(image, cls=True)
        ocr_text = '\n'.join([line[1][0] for line in result[0]])
        txt_filename = os.path.splitext(image)[0] + '.txt'
        with open(txt_filename, 'w') as txt_file:
            txt_file.write(ocr_text)
        print(f'OCR completed for {image}. Text saved to {txt_filename}.')
       

    def submit(self):
        description = self.text_edit.toPlainText()
        annotation_file = f"{self.image_path}.annotation.txt"
        with open(annotation_file, 'a+') as file:
            file.write(description)
        self.accept()
