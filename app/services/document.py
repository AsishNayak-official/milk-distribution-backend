import comtypes.client
import os

# Function to convert .docx to .pdf using Word Application
def convert_docx_to_pdf(docx_path, pdf_path):
    word = comtypes.client.CreateObject('Word.Application')
    doc = word.Documents.Open(docx_path)
    doc.SaveAs(pdf_path, FileFormat=17)  # 17 is the PDF format code
    doc.Close()
    word.Quit()

# Function to generate the path for PDF and perform conversion
def generate_pdf_from_word(docx_path):
    # Define the path for the PDF
    pdf_path = docx_path.replace(".docx", ".pdf")

    # Convert Word document to PDF
    convert_docx_to_pdf(docx_path, pdf_path)
    return pdf_path
