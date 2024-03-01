import fitz  # Make sure you have PyMuPDF installed: pip install PyMuPDF

def extract_pdf_text_with_layout(pdf_file):
    """
    Extracts text from a PDF file using PyMuPDF (fitz) and preserves layout information.
    """
    doc = fitz.open(stream=pdf_file, filetype="pdf")  # Open from in-memory stream
    text_blocks = []

    for page in doc:
        # Perform layout analysis
        layout_data = analyze_page_layout(page)

        for block in layout_data:
            if block["type"] == "text": 
                text_block_dict = {
                    "text": block["text"],
                    "x0": block["bbox"][0],
                    "y0": block["bbox"][1],
                    "x1": block["bbox"][2],
                    "y1": block["bbox"][3]
                }
                text_blocks.append(text_block_dict)

    return text_blocks

def analyze_page_layout(page):
    """Analyzes the layout of a PDF page."""
    blocks = page.get_text("blocks")
    layout_data = []

    for b in blocks:
        r = b[:4]  # Block rectangle
        block_type = "text"  # Assume text initially
        if b[-1] == 1:  # If image block
            block_type = "image"

        layout_data.append({
            "type": block_type,
            "text": b[4],  # Text content (if applicable)
            "bbox": r 
        })

    return layout_data

# Parsing PDF

def parse_pdf(pdf_file):

    text_with_layout = extract_pdf_text_with_layout(pdf_file)
    all_text = ""

    for block in text_with_layout:
        all_text += str(block['text'])

    return(all_text)
