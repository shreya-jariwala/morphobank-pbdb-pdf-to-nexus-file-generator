import google.generativeai as genai
import os

# Configure your API key
genai.configure(api_key="")  # Replace with your actual API key

# Load the Gemini Pro model
model = genai.GenerativeModel("gemini-pro")

def prompt_and_save_response(input_txt_file, output_file_path, prompt,):
    """Prompts Gemini with the given text and prompt, and saves the response to a file, using UTF-8 encoding."""

    with open(input_txt_file, "r", encoding="utf-8") as f:
        input_text = f.read()

    response = model.generate_content(input_text + "\n" + prompt)

    with open(os.path.join(output_file_path, "extracted-character-list.txt"), 'w' , encoding="utf-8") as f:
        f.write(response.text)

# Example usage (paths adjusted for clarity)
#input_file =
#prompt = "Identify and extract the following information from the provided text: Character list: A list of characters or features being described, along with their possible states or values. Additional instructions: Prioritize clarity and precision in the extracted data."
#character_list = r"G:\Shared drives\My Drive (aquiveal@gmail.com)\Projects\Large Language Model - MorphoBank\Testing\Adelophthalmoidea_Tetlie_&_Poschmann_2008-character-list.txt"

#prompt_and_save_response(input_file, prompt, character_list)
