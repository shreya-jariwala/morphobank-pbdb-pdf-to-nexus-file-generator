from lxml import etree

def repair_and_parse(data):

    # Find the start and end positions of the XML within the text data
    start_index = data.find("<characters>")
    end_index = data.find("</characters>", start_index) + len("</characters>")

    if start_index == -1 or end_index == -1:
        raise ValueError("Invalid input: Couldn't find XML data within the text.")
    
    
    xml_data = data[start_index:end_index]

    xml_data = xml_data.replace(""""><""", """">&lt;""")
    xml_data = xml_data.replace("""">>""", """">&gt;""")
    xml_data = xml_data.replace(""""> <""", """">&lt;""")
    xml_data = xml_data.replace(""""> >""", """">&gt;""")
    xml_data = xml_data.replace("≤", "&lt;=")
    xml_data = xml_data.replace("≥", "&gt;=")
    
    xml = etree.fromstring(xml_data.encode('utf-8'))
    return xml

def validate_count_and_range(xml_tree, start_index, end_index):
    """
    Validates the XML data according to the specified criteria.

    Args:
        xml_data (str): The XML data as a string.
        start_index (int): The starting index.
        end_index (int): The ending index.

    Returns:
        bool: True if the XML data is valid, False otherwise.
    """

    tree = etree.ElementTree(xml_tree)
    root = tree.getroot()

    print(f"Validating XML data for characters {start_index}-{end_index}")

    # 1. Check for non-empty 'name' attributes
    for character in root.iter('character'):
        if not character.attrib.get('name'):
            print(f"Error: Character at index {character.attrib['index']} is missing 'name' attribute.")
            return False

    # 2. Check index range
    for character in root.iter('character'):
        index = int(character.attrib['index'])
        if index < start_index or index > end_index:
            print(f"Error: Character index {index} is out of range ({start_index}-{end_index}).")
            return False
        
    print(f"XML data for characters {start_index}-{end_index} is valid.")
    return True  # All validations passed 
