import os

def extract_last_characters(input_file, output_file_path, num_characters=100000):
   """Extracts the last specified number of characters from a text file and saves them to a new file.

   Args:
       input_file (str): Path to the input text file.
       output_file (str): Path to the output text file.
       num_characters (int, optional): Number of characters to extract. Defaults to 100000.
   """

   with open(input_file, 'r', encoding="utf-8") as f:
       data = f.read()

   if len(data) >= num_characters:
       last_characters = data[-num_characters:]
   else:
       print(f"Warning: Input file has fewer than {num_characters} characters. Extracting all available characters.")
       last_characters = data

   with open(os.path.join(output_file_path, "trimmed-paper.txt"), 'w', encoding="utf-8") as output_file:
       output_file.write(last_characters)

# Example usage:
#input_file = r"G:\Shared drives\My Drive (aquiveal@gmail.com)\Projects\Large Language Model - MorphoBank\Testing\Adelophthalmoidea_Tetlie_&_Poschmann_2008-extracted.txt"
#output_file = r"G:\Shared drives\My Drive (aquiveal@gmail.com)\Projects\Large Language Model - MorphoBank\Testing\Adelophthalmoidea_Tetlie_&_Poschmann_2008-trimmed.txt"
#extract_last_characters(input_file, output_file)

