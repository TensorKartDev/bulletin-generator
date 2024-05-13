from PIL import Image
from fpdf import FPDF

class ImageToPDF:
    def __init__(self, default_pdf_path=None):
        """
        Constructor for the ImageToPDF class.

        :param default_pdf_path: str, default path to save the PDF if not specified in the method call.
        """
        self.default_pdf_path = default_pdf_path

    def image_to_pdf(self, image_path, pdf_path=None):
        """
        Convert an image to a PDF file.

        :param image_path: str, path to the image file
        :param pdf_path: str, path to save the PDF file. If None, uses the default path or the same name as the image.
        """
        if pdf_path is None:
            if self.default_pdf_path is not None:
                pdf_path = self.default_pdf_path
            else:
                pdf_path = image_path.rsplit('.', 1)[0] + '.pdf'
        
        # Load the image
        image = Image.open(image_path)
        
        # Create instance of FPDF class
        pdf = FPDF(unit="pt", format=[image.width, image.height])
        
        # Add a page with the same size as the image
        pdf.add_page()
        
        # Place the image on the page at (0,0)
        pdf.image(image_path, 0, 0, image.width, image.height)
        
        # Save the PDF to a file
        pdf.output(pdf_path, 'F')
        print(f"PDF file has been created: {pdf_path}")

# Example usage:
# Create an instance of ImageToPDF with a default path (optional)
# converter = ImageToPDF()

# # Convert an image to PDF
# converter.image_to_pdf('path_to_your_image.jpg')
