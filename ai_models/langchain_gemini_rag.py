import vertexai
from vertexai.language_models import TextEmbeddingModel

import streamlit as st
from google.oauth2 import service_account

from langchain_core.prompts import PromptTemplate
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain_google_vertexai import VertexAI

VERTEXAI_PROJECT = st.secrets.vertexai.project
VERTEXAI_LOCATION = st.secrets.vertexai.location
GOOGLE_CREDENTIALS = service_account.Credentials.from_service_account_info(st.secrets["gcs_connections"])

def get_prompt(context, prompt):
    # Initialize Vertex AI SDK
    vertexai.init(project=VERTEXAI_PROJECT, location=VERTEXAI_LOCATION, credentials=GOOGLE_CREDENTIALS)

    # Initialize Vertex AI Model

    model = VertexAI(model_name="gemini-1.0-pro-001")

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=15000, chunk_overlap=1000)
    texts = text_splitter.split_text(context)

    # Initialize Text Embedding Model

    embeddings = TextEmbeddingModel(model_name="textembedding-gecko@003")

    # Initialize RetrievalQA Chain

    vector_index = Chroma.from_texts(texts, embeddings).as_retriever(search_kwargs={"k":5})

    
    template = "{context}\n\n Prompt: {prompt}"

    CHAIN_PROMPT = PromptTemplate.from_template(template)# Run chain

    chain = RetrievalQA.from_chain_type(
        model,
        retriever=vector_index,
        return_source_documents=True,
        chain_type_kwargs={CHAIN_PROMPT}
    )

    return chain.run(
        prompt=prompt,
        context=context,
    )