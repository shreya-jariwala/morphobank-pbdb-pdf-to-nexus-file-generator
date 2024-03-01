import vertexai
from vertexai.generative_models import GenerativeModel

from google.oauth2 import service_account
import streamlit as st 

# Initialize the client
VERTEXAI_PROJECT = st.secrets.vertexai.project
VERTEXAI_LOCATION = st.secrets.vertexai.location
GOOGLE_CREDENTIALS = service_account.Credentials.from_service_account_info(st.secrets["gcs_connections"])

vertexai.init(project=VERTEXAI_PROJECT, location=VERTEXAI_LOCATION, credentials=GOOGLE_CREDENTIALS)

# Define the extraction function
def get_response(prompt):

    model = GenerativeModel("gemini-1.0-pro")

    print("Waiting for the response...")
    response = model.generate_content(prompt, generation_config={
        "max_output_tokens": 2048,
        "temperature": 0.6,
        "top_p": 1
    })
    print("Response received!")
    return response