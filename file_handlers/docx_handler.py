import docx

def extract_text_by_page(doc_path, start_page, end_page):
    """
    Extracts text from a Word document (.docx) between specified pages.

    Args:
        doc_path (str): Path to the Word document.
        start_page (int): The starting page number (1-based indexing).
        end_page (int): The ending page number (inclusive).

    Returns:
        str: The extracted text.
    """

    doc = docx.Document(doc_path)
    text = ''

    page_count = 0  # Keep track of the current page
    for paragraph in doc.paragraphs:
        page_count += 1  # Approximate page count (see limitations below)

        if start_page <= page_count <= end_page:
            text += paragraph.text + '\n'

    return text