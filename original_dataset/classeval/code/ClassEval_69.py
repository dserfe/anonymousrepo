import PyPDF2

class PDFHandler:

    def __init__(self, filepaths):
        self.filepaths = filepaths
        self.readers = [PyPDF2.PdfReader(fp) for fp in filepaths]

    def merge_pdfs(self, output_filepath):
        pdf_writer = PyPDF2.PdfWriter()
        for reader in self.readers:
            for page_num in range(len(reader.pages)):
                page = reader.pages[page_num]
                pdf_writer.add_page(page)
        with open(output_filepath, 'wb') as out:
            pdf_writer.write(out)
        return f'Merged PDFs saved at {output_filepath}'

    def extract_text_from_pdfs(self):
        pdf_texts = []
        for reader in self.readers:
            for page_num in range(len(reader.pages)):
                page = reader.pages[page_num]
                pdf_texts.append(page.extract_text())
        return pdf_texts