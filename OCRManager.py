from paddleocr import PaddleOCR,draw_ocr
import os
ocr = PaddleOCR(use_angle_cls=True, lang='en')
def perform_ocr_on_images(root_dir,ocr):
    # ocr = PaddleOCR(use_angle_cls=True, lang='en')  # Initialize PaddleOCR
    for subdir, _, files in os.walk(root_dir):
        for file in files:
            if file.endswith('.png'):
                file_path = os.path.join(subdir, file)
                result = ocr.ocr(file_path, cls=True)
                ocr_text = '\n'.join([line[1][0] for line in result[0]])
                txt_filename = os.path.splitext(file_path)[0] + '.txt'
                with open(txt_filename, 'w') as txt_file:
                    txt_file.write(ocr_text)
                print(f'OCR completed for {file_path}. Text saved to {txt_filename}.')
