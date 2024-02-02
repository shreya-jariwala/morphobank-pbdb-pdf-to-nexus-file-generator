from bs4 import BeautifulSoup
import html5lib  # Parser for handling broken XML

def extract_text_from_p_tags(filename, output_dir):
    """Extracts text from p tags in a potentially broken XML file and saves it to a TXT file.

    Args:
        filename (str): The path to the XML file.
        output_filename (str, optional): The name of the output TXT file. Defaults to "extracted_text.txt".
    """

    with open(filename, "r") as file:
        try:
            soup = BeautifulSoup(file, "html5lib")  # Use html5lib for robustness
            p_tags = soup.find_all("p")
            text_data = [p_tag.get_text(strip=True) for p_tag in p_tags]

            output_filename = f"{output_dir}/extracted-tags.txt"  # Construct output filename
            with open(output_filename, "w", encoding="utf-8") as f:
                f.writelines(text + "\n" for text in text_data)

        except Exception as e:
            print(f"Error processing XML: {e}")

