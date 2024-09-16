from io import BytesIO

from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas


def add_hidden_text_to_pdf(uploaded_pdf_file, hidden_text):
    """
    Adds hidden text to the background of a PDF document with very small
    font size.

    Parameters:
    - uploaded_pdf_file: the uploaded PDF file object from Streamlit
    - hidden_text: str, the hidden text (keywords, notes) to be added

    Returns:
    - BytesIO: in-memory bytes buffer of the modified PDF
    """

    def create_background_text_pdf(text, page_width, page_height):
        buffer = BytesIO()
        c = canvas.Canvas(buffer, pagesize=(page_width, page_height))
        c.setFont("Helvetica", 8)
        c.setFillColorRGB(1, 1, 1)
        c.drawString(50, 50, text)
        c.showPage()
        c.save()
        buffer.seek(0)
        return buffer

    resume_reader = PdfReader(uploaded_pdf_file)
    writer = PdfWriter()

    for page in resume_reader.pages:
        page_width = float(page.mediabox.width)
        page_height = float(page.mediabox.height)

        background_pdf_buffer = create_background_text_pdf(
            hidden_text, page_width, page_height
        )
        background_reader = PdfReader(background_pdf_buffer)

        if len(background_reader.pages) > 0:
            page.merge_page(background_reader.pages[0])

        writer.add_page(page)

    output_pdf_buffer = BytesIO()
    writer.write(output_pdf_buffer)
    output_pdf_buffer.seek(0)

    return output_pdf_buffer
