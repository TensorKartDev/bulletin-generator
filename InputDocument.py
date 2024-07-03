import fitz

class InputDocument:
    def __init__(self, document_name, file_path):
        self.document_name = document_name
        self.file_path = file_path
        self.document = fitz.open(file_path)
        self.total_pages = self.document.page_count
        self.pages = [self.document.load_page(i).get_pixmap() for i in range(self.total_pages)]
        self.current_page = 0

    @property
    def extension(self):
        return self.document_name.split('.')[-1] if '.' in self.document_name else ''

    def get_current_page_pixmap(self):
        if 0 <= self.current_page < self.total_pages:
            return self.pages[self.current_page]
        else:
            return None

    def next_page(self):
        if self.current_page < self.total_pages - 1:
            self.current_page += 1
        else:
            print("You are at the last page.")

    def previous_page(self):
        if self.current_page > 0:
            self.current_page -= 1
        else:
            print("You are at the first page.")

    def go_to_page(self, page_number):
        if 0 <= page_number < self.total_pages:
            self.current_page = page_number
        else:
            print("Page number out of range.")


