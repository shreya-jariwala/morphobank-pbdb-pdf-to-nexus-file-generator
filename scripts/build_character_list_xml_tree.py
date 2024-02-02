import lxml.etree as ET
import os

def parse_broken_xml(input_txt, output_dir):
   """Parses a txt file containing possibly broken XML structure and saves it as a valid XML file.

   Args:
       input_txt (str): Path to the input txt file.
       output_dir (str): Path to the output directory where the XML file will be saved.
       output_filename (str): Desired filename for the output XML file.
   """

   with open(input_txt, 'r', encoding='utf-8') as f:
       txt_content = f.read()

   # Find the index of the first '<characters>' tag
   index = txt_content.find('<characters>')

   if index != -1:  # If the tag is found
       txt_content = txt_content[index:]  # Slice the content starting from the tag

   # Use a forgiving parser to handle common XML errors
   parser = ET.XMLParser(recover=True, no_network=True)

   try:
       root = ET.fromstring(txt_content, parser=parser)
   except ET.ParseError as e:
       # Handle parse errors gracefully
       print(f"Parsing error: {e}")
       return

   # Check for empty file:
   if not root:
       print("Input file is empty. No XML tree to write.")
       return

   # Construct the full output path
   output_xml = os.path.join(output_dir, "character-list-xml-tree.xml")

   # Ensure proper XML formatting
   tree = ET.ElementTree(root)
   tree.write(output_xml, encoding='utf-8')


#if __name__ == '__main__':
   #input_txt = input("Enter the path to the input txt file: ")
   #output_dir = input("Enter the desired output directory: ")
   #parse_broken_xml(input_txt, output_dir)