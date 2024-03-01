import streamlit as st
import os

# Import your Python scripts
from utils import handler
import character_state_processor

from parsers import pymupdf_parser
from file_handlers import pdf_handler, nexus_handler

# Layout and file upload

st.title("MorphoBank PBDB PDF to NEXUS File Generator")

st.subheader("Start by Uploading the Document.")
st.write("Please upload the file containing the character list. Ideally I want you to keep the file open side by side to help me with more information that will help me process you request more effeciently")

research_paper = st.file_uploader("Upload Character List file", type="pdf")

parsing_method_description = st.empty()

st.subheader("Define your Characters")
st.write("""
    Please identify the pages in the document where the character state labels are located? Also, please specify the number of characters and their corresponding states that you'd like me to extract
""")

opt_col1, opt_col2 = st.columns(2)

with opt_col1:
    charstate_page_range = st.text_input("Pages in Range (Inclusive)", placeholder="3-4")

with opt_col2:
    charstate_count = st.number_input("Number of Characters", step=int(1))

st.subheader("Upload the Empty NEXUS File")
st.write("Please upload the Nexus file with the missing character state labels that need to be processed.")
nexus_file = st.file_uploader("Upload NEXUS File", type="nex")

character_state_view = st.empty()

# Processing

with st.sidebar:
    if st.button("Process NEXUS file"):

        with st.status("Processing...", expanded=True) as status:
            
            st.write("Parsing the Document...")
            start_page, end_page = handler.get_page_range(charstate_page_range)
            if research_paper:
                filename, file_extension = os.path.splitext(research_paper.name)
                if file_extension.lower() == '.pdf':

                    st.write("Extracting Pages...")
                    extracted_pages = pdf_handler.extract_pages(research_paper, start_page, end_page)

                    st.write("Extracting Text from Pages...")
                    text_data = pymupdf_parser.parse_pdf(extracted_pages)

                #elif file_extension.lower() == '.word':
                   # st.write("Extracting Text from Pages...")
                    #text_data = docx_handler.extract_text_by_page(research_paper, start_page, end_page)
            
            st.write("Extracting Character and State Data as XML Tree...")
            character_state_tree = character_state_processor.generate_character_state_tree(text_data, charstate_count)

            st.write("Building Character State Labels...")
            character_state_labels = character_state_processor.build_character_state_labels(character_state_tree)

            st.write("Updating the NEXUS file...")
            new_nexus_file = nexus_handler.insert_or_replace_charstatelabels(nexus_file, character_state_labels)

            status.update(label="Processing complete!", state="complete", expanded=False)

        # Create a download button
        download_button = st.download_button(
            label="Download the updated NEXUS File",
            data=new_nexus_file,
            file_name=filename + ".nex",
        )