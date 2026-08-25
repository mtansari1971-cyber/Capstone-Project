import io
from PyPDF2 import PdfReader
from docx import Document


def extract_text_from_pdf(file):
    """
    Extract text from an uploaded PDF file.
    """

    try:
        # Read uploaded file
        pdf_bytes = file.read()

        # Create PDF reader
        pdf_reader = PdfReader(
            io.BytesIO(pdf_bytes)
        )

        text = ""

        # Extract text from every page
        for page in pdf_reader.pages:

            page_text = page.extract_text()

            if page_text:
                text += page_text + "\n"

        return text.strip()

    except Exception as e:

        raise Exception(
            f"Could not extract text from PDF: {e}"
        )


def extract_text_from_docx(file):
    """
    Extract text from an uploaded DOCX file.
    """

    try:
        # Read uploaded DOCX file
        docx_bytes = file.read()

        # Open document from memory
        document = Document(
            io.BytesIO(docx_bytes)
        )

        text = ""

        # Extract paragraphs
        for paragraph in document.paragraphs:

            if paragraph.text.strip():

                text += paragraph.text + "\n"

        return text.strip()

    except Exception as e:

        raise Exception(
            f"Could not extract text from DOCX: {e}"
        )


def extract_text_from_file(file):
    """
    Automatically detect PDF/DOCX
    and extract the text.
    """

    file_name = file.name.lower()


    # PDF
    if file_name.endswith(".pdf"):

        return extract_text_from_pdf(file)


    # DOCX
    elif file_name.endswith(".docx"):

        return extract_text_from_docx(file)


    # Unsupported format
    else:

        raise ValueError(
            "Unsupported file format. "
            "Please upload a PDF or DOCX file."
        )