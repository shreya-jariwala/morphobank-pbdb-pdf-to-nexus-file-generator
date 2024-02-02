import requests
import os

# Function to process a PDF file using the Grobid API

def process_full_text_document(grobid_api_url, pdf_file_path, output_file_path):
    """Sends a PDF file to the Grobid API for full text processing and saves the output to a file.

    Args:
        grobid_api_url (str): The base URL of the Grobid API.
        pdf_file_path (str): The path to the PDF file to be processed.
        output_file_path (str): The path to save the processed output.
    """

    with open(pdf_file_path, 'rb') as pdf_file:
        try:
            response = requests.post(
                grobid_api_url + '/api/processFulltextDocument',
                files={'input': pdf_file}
            )
            response.raise_for_status()  # Raise an exception for non-200 status codes

            with open(os.path.join(output_file_path, "processed-pdf.xml"), 'w') as f:
                f.write(response.text)

            print(f"Processed text saved to: {output_file_path}")

        except requests.exceptions.RequestException as e:
            print(f"Error processing PDF: {e}")

# Example usage:
#grobid_api_url = "http://localhost:8070"  # Replace with your Grobid API URL
#pdf_file_path = "path/to/pdf/file.pdf"  # Replace with the path to the PDF file to be processed
#output_file_path = "path/to/output/file.xml"  # Replace with the path to save the processed output

#process_full_text_document(grobid_api_url, pdf_file_path, output_file_path)