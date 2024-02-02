import streamlit as st
import os

# Import your Python scripts
from scripts import grobid_pdf_processor, extract_text_from_xml, trim_paper_for_prompt, prompt_character_list, prompt_xml_tree, build_character_list_xml_tree, nexus_updater

# Layout and file upload
st.title("MorphoBank PBDB PDF to NEXUS File Generator")

charstate_pdf = st.file_uploader("Upload PDF containing the Character List", type="pdf")
nexus_file = st.file_uploader("Upload Empty NEXUS File", type="nex")

if charstate_pdf and nexus_file:
    # Create output directory
    working_dir = os.path.join(r"/data", os.path.splitext(nexus_file.name)[0])
    os.makedirs(working_dir, exist_ok=True)  # Create if it doesn't exist

    # Save uploaded files to the working directory
    with open(os.path.join(working_dir, charstate_pdf.name), "wb") as f:
        f.write(charstate_pdf.getbuffer())
    with open(os.path.join(working_dir, nexus_file.name), "wb") as f:
        f.write(nexus_file.getbuffer())

    # Generate output file names
    charstate_pdf_path = os.path.join(working_dir, charstate_pdf.name)  # Constructed path using output_dir
    processed_xml_path = os.path.join(working_dir, "processed-pdf.xml")  # Constructed path using output_dir
    extracted_tags_path = os.path.join(working_dir, "extracted-tags.txt")
    trimmed_paper_path = os.path.join(working_dir, "trimmed-paper.txt")
    extracted_character_list_path = os.path.join(working_dir, "extracted-character-list.txt")
    extracted_character_list_xml_tree_path = os.path.join(working_dir, "extracted-character-list-xml-tree.txt")
    character_list_xml_tree_path = os.path.join(working_dir, "character-list-xml-tree.xml")
    nexus_file_path = os.path.join(working_dir, nexus_file.name)

    # Define Grobid server
    grobid_api_url = "http://35.188.91.205:8070"

    # Define prompts
    character_list_extraction_prompt = "Identify and extract the following information from the provided text: Character list: A list of characters or features being described, along with their possible states or values. Additional instructions: Prioritize clarity and precision in the extracted data."
    character_list_xml_tree_extraction_prompt = """Generate XML code that represents the following character list: Structure: Represent each character with a <character> element. Enclose all characters within a root element named <characters>. Assign the characters name to the name attribute of the <character> element. List each state within a separate <state> element under the <character> element. Desired structure: <characters> <character name="Triangular 'doublure lock' anteriorly on carapace"> <state>absent</state> <state>present</state> </character>"""

    # Process the files
    processed_xml = grobid_pdf_processor.process_full_text_document(grobid_api_url, charstate_pdf_path, working_dir)  # Call the function
    extracted_tags = extract_text_from_xml.extract_text_from_p_tags(processed_xml_path, working_dir)  # Call the function
    trimmed_paper = trim_paper_for_prompt.extract_last_characters(extracted_tags_path, working_dir)  # Call the function
    extracted_character_list = prompt_character_list.prompt_and_save_response(trimmed_paper_path, working_dir, character_list_extraction_prompt)
    extracted_character_list_xml_tree = prompt_xml_tree.prompt_and_save_tree(extracted_character_list_path, working_dir, character_list_xml_tree_extraction_prompt)
    character_list_xml_tree = build_character_list_xml_tree.parse_broken_xml(extracted_character_list_xml_tree_path, working_dir)
    updated_nexus_file = nexus_updater.process_files(nexus_file_path, character_list_xml_tree_path)

    # Add download button for the updated NEXUS file
    st.download_button(
        label="Download File",
        data=open(nexus_file_path, "rb").read(),  # Open the file in binary mode to read its contents
        file_name=os.path.basename(nexus_file_path)  # Set the suggested filename for the download
    )