import google.generativeai as genai
import os

# Configure your API key
genai.configure(api_key="AIzaSyAoiOta4yu3PBMaddNgGwJtT2zJqCHxlrk")  # Replace with your actual API key

# Load the Gemini Pro model
model = genai.GenerativeModel("gemini-pro")

def prompt_and_save_tree(input_txt_file, output_file_path, prompt):
    """Prompts Gemini with the given text and prompt, and saves the response to a file, using UTF-8 encoding."""

    with open(input_txt_file, "r", encoding="utf-8") as f:
        input_text = f.read()

    response = model.generate_content(input_text + "\n" + prompt)

    with open(os.path.join(output_file_path, "extracted-character-list-xml-tree.txt"), 'w' , encoding="utf-8") as f:
        f.write(response.text)


# Example usage (replace placeholders with actual file paths)
#input_file = # Adjust input file path as needed
#prompt =   # Adjust prompt as needed
#output_xml_file =   # Adjust output file path as needed

#prompt_and_save_tree(input_file, prompt, output_xml_file)