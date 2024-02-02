import xml.etree.ElementTree as ET

def process_files(nexus_file_path, xml_file_path):
  """
  Reads a NEXUS file and an XML file, inserts or overrides CHARSTATELABELS,
  formatted as specified.

  Args:
    nexus_file_path (str): Path to the NEXUS file.
    xml_file_path (str): Path to the XML file.
  """

  with open(nexus_file_path, "r+") as nexus_file:
    lines = nexus_file.readlines()

    charstatelabels_start_index = None
    matrix_index = None
    for i, line in enumerate(lines):
      stripped_line = line.strip()
      if stripped_line.startswith("CHARSTATELABELS"):
        charstatelabels_start_index = i
      elif stripped_line.startswith("MATRIX"):
        matrix_index = i
        break

    if charstatelabels_start_index is not None and matrix_index is not None:
      charstatelabels = generate_charstatelabels_from_xml(xml_file_path)

      # Override existing CHARSTATELABELS with matching indentation
      indent_level = len(line) - len(line.lstrip())
      indented_lines = [f"{' ' * indent_level}{label}\n" for label in charstatelabels]
      lines[charstatelabels_start_index:matrix_index] = ["\tCHARSTATELABELS\n"] + indented_lines

    nexus_file.seek(0)
    nexus_file.writelines(lines)

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