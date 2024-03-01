from lxml import etree
import concurrent.futures
from ai_models import gemini
from file_handlers import xml_handler

# Import specific functions to enhance clarity
from utils import handler

# Import prompt templates
from prompt_template import FUNCTION_PROMPT, STRUCTURED_EXAMPLE

#Constants
MAX_RETRIES = 3
CHUNK_SIZE = 20

def generate_character_state_tree(character_state_data, total_character_states):
    """
    Generates valid character state XML elements in chunks using concurrent processing.

    Args:
        character_state_data: The complete character state data source.
        total_character_states: Total number of character states to process.

    Returns:
        An lxml Element representing the complete 'characters' XML structure.
    """

    character_state_xml = etree.Element('characters')

    with concurrent.futures.ProcessPoolExecutor() as executor:  # Use a process pool
        futures = [
            executor.submit(
                process_character_state_chunk, character_state_data, start_index, end_index
            )
            for start_index, end_index in handler.generate_chunks(
                total_character_states, CHUNK_SIZE
            )
        ]

        for future in concurrent.futures.as_completed(futures):
            xml_string = future.result()
            if xml_string:
                # Parse the XML string back into an lxml.etree._Element object
                parsed_xml = etree.fromstring(xml_string)
                character_state_xml.extend(parsed_xml)
    
    return character_state_xml


def process_character_state_chunk(character_state_data, start_index, end_index):
    """
    Processes a chunk of character states, handling errors and validation.

    Args:
        character_state_data: The complete character state data source.
        start_index: Starting index of the chunk.
        end_index: Ending index of the chunk.

    Returns:
        A list of valid XML strings for the chunk.
    """

    for _ in range(MAX_RETRIES):
        try:
            # Generate the prompt for the chunk
            function_prompt = FUNCTION_PROMPT.format(start=start_index, end=end_index)
            prompt = character_state_data + function_prompt + STRUCTURED_EXAMPLE

            # Get the response from the model
            raw_xml_response = gemini.get_response(prompt)

            # Repair and parse the XML response
            parsed_xml = xml_handler.repair_and_parse(raw_xml_response.text)

            if not xml_handler.validate_count_and_range(parsed_xml, start_index, end_index):
                print("Validation failed for XML response for ", start_index, "-", end_index)
            
            # Convert the parsed XML to a string and return it
            return etree.tostring(parsed_xml, encoding='unicode')


        except Exception as e:
            print(f"Error processing chunk: {e}")

    print(f"Maximum retries exceeded for chunk {start_index} - {end_index}")
    return []


def build_character_state_labels(xml_tree):
    """
    Extracts CHARSTATELABELS from the provided XML tree, formatted as specified,
    prioritizing the 'index' attribute for character numbering.

    Args:
        xml_tree: The parsed XML tree.

    Returns:
        list: List of formatted CHARSTATELABELS strings.
    """

    tree = etree.ElementTree(xml_tree)
    root = tree.getroot()

    character_state_labels = []

    for character in root.findall("character"):
        name = character.attrib["name"].replace("'", "?")

        # Prioritize 'index' attribute if it exists
        if 'index' in character.attrib:
            character_number = int(character.attrib['index'])
        else:
            character_number = len(character_state_labels) + 1  # Fallback: sequential numbering

        states = ["'" + state.text + "'" for state in character.findall("state")]
        label = f"{character_number} '{name}' / {' '.join(states)},"

        character_state_labels.append("\t\t" + label)

    character_state_labels[-1] = character_state_labels[-1].replace(",", ";")

    return character_state_labels