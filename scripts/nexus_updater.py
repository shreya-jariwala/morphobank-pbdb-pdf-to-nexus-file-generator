import xml.etree.ElementTree as ET

def process_files(nexus_file_path, xml_file_path):
    """ ... (docstring remains the same) ... """

    try:
        with open(nexus_file_path, "r+") as nexus_file:
            lines = nexus_file.readlines()

            charstatelabels_start_index = None
            matrix_index = None
            matrix_indent = None

            for i, line in enumerate(lines):
                stripped_line = line.strip()
                if stripped_line.startswith("CHARSTATELABELS"):
                    charstatelabels_start_index = i
                elif stripped_line.startswith("MATRIX"):
                    matrix_index = i
                    matrix_indent = len(line) - len(line.lstrip())
                    break

            charstatelabels = generate_charstatelabels_from_xml(xml_file_path)

            if matrix_index is not None:
                insert_index = matrix_index
                if charstatelabels_start_index is not None:  # Overwrite existing
                     insert_index = charstatelabels_start_index

                indented_lines = [f"{' ' * matrix_indent}{label}\n" for label in charstatelabels]
                lines[insert_index:insert_index] = [f"{' ' * matrix_indent}\tCHARSTATELABELS\n"] + indented_lines

            nexus_file.seek(0)
            nexus_file.writelines(lines)

    except FileNotFoundError as e:
        print(f"Error: File not found ({e.filename})")
    except ET.ParseError as e:
        print(f"Error parsing XML: {e}")

def generate_charstatelabels_from_xml(xml_file_path):
  """
  Extracts CHARSTATELABELS from the XML file, formatted as specified.

  Args:
    xml_file_path (str): Path to the XML file.

  Returns:
    list: List of CHARSTATELABELS strings.
  """

  tree = ET.parse(xml_file_path)
  root = tree.getroot()

  charstatelabels = []
  character_number = 1
  for character in root.findall("character"):
    name = character.attrib["name"].replace("'", "?")  # Replace ' with ? in character name
    states = [
                state.text.replace("≥", ">").replace("≤", "<")  # Replace symbols in states
                for state in character.findall("state")
            ]
    states = [f"'{state}'" for state in states]  # Enclose states in '
    label = f"{character_number} '{name}' / {' '.join(states)},"  # Add spaces between states
    charstatelabels.append("\t\t" + label)
    character_number += 1

  charstatelabels[-1] = charstatelabels[-1].replace(",", ";")  # Replace comma with semicolon for the last line
  return charstatelabels

"""
if __name__ == "__main__":
  nexus_file_path =  # Replace with your NEXUS file path
  xml_file_path = # Replace with your XML file path
  process_files(nexus_file_path, xml_file_path)
"""