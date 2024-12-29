import fitz  # PyMuPDF
from docx import Document
import difflib
from diff_match_patch import diff_match_patch

# Function to extract text from a PDF using PyMuPDF
def extract_text_from_pdf(pdf_filename):
    pdf_document = fitz.open(pdf_filename)
    text = ""
    for page_num in range(pdf_document.page_count):
        page = pdf_document.load_page(page_num)
        text += page.get_text("text")  # Extract text from the page
    return text

# Function to generate a diff between the original and new text
def generate_diff(original_text, new_text):
    dmp = diff_match_patch()
    diffs = dmp.diff_main(original_text, new_text)
    dmp.diff_cleanupSemantic(diffs)  # Optionally clean up the diff
    # Convert the diff into a HTML-friendly format
    html_diff = ""
    for diff in diffs:
        if diff[0] == 1:  # Added text
            html_diff += f'<span style="background-color: #e6ffed;">{diff[1]}</span>'
        elif diff[0] == -1:  # Removed text
            html_diff += f'<span style="background-color: #ffe6e6;">{diff[1]}</span>'
        else:  # Unchanged text
            html_diff += diff[1]
    return html_diff

# Function to create a DOCX file from the extracted text from PDF
def create_docx_from_pdf(pdf_filename, docx_filename):
    # Create a new DOCX document
    doc = Document()

    # Extract text from the PDF
    text = extract_text_from_pdf(pdf_filename)

    # Add the extracted text to the DOCX document
    doc.add_paragraph(text)

    # Save the DOCX document
    doc.save(docx_filename)
    return docx_filename
