import os
import json
import shutil
import streamlit as st
from datetime import datetime
from google.cloud import documentai_v1 as documentai
from google.oauth2 import service_account

def save_uploaded_file(uploaded_file):
    """Saves the uploaded file to a local directory and returns the file path."""
    UPLOAD_DIR = "./saved_uploads"
    os.makedirs(UPLOAD_DIR, exist_ok=True)

    if uploaded_file is None:
        return None, "No file uploaded!"

    # Define the file path where the uploaded file will be saved
    saved_file_path = os.path.join(UPLOAD_DIR, uploaded_file.name)

    # Save the uploaded file
    with open(saved_file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    return saved_file_path, f"File saved at: {saved_file_path}"

def process_pdf(pdf_path):
    """Processes the PDF using Google Document AI and extracts text."""
    # Load credentials from environment variable
    credentials_info = json.loads(os.environ["GCP_SERVICE_ACCOUNT_KEY"])
    credentials = service_account.Credentials.from_service_account_info(credentials_info)

    # Initialize Google Document AI Client
    client = documentai.DocumentProcessorServiceClient(credentials=credentials)

    # Define Google Document AI processor
    project_id = "myfirstocrvisionproject"
    location = "us"
    processor_id = "7670b830a0fd8325"
    processor_name = f"projects/{project_id}/locations/{location}/processors/{processor_id}"

    # Read the PDF file
    with open(pdf_path, "rb") as file:
        raw_document = documentai.RawDocument(content=file.read(), mime_type="application/pdf")

    # Send document for processing
    request = documentai.ProcessRequest(name=processor_name, raw_document=raw_document)
    result = client.process_document(request=request)

    # Extract and return text
    return result.document.text if result.document.text else "No text extracted."

def predict(query, uploaded_file, task):
    """Handles file saving and PDF processing, then returns extracted text."""
    if uploaded_file is None:
        return "No file uploaded!"

    # Save uploaded file locally
    saved_file_path, save_msg = save_uploaded_file(uploaded_file)

    # Process PDF and extract text
    document_text = process_pdf(saved_file_path)

    return f"Extracted Text:\n{document_text}\n\nFile Path: '{saved_file_path}'\nQuery: '{query}'\nTask: '{task}'"

# Streamlit UI
st.title("Research Paper Processor")
st.write("Upload a PDF, enter your query, and choose a task.")

# Query input text box
query_input_txt = st.text_area(
    "Query Input",
    placeholder="Enter your query here",
    height=150
)

# File upload
file_upload = st.file_uploader("Upload PDF", type=["pdf"])

# Task selection radio buttons
task_selection = st.radio(
    "Select Task",
    options=["Summarize", "Extract Use Cases", "Generate PRD"],
    index=0  # Default selection
)

# Submit button
if st.button("Submit"):
    if file_upload is None:
        st.error("Please upload a PDF file.")
    elif not query_input_txt.strip():
        st.error("Please enter a query.")
    else:
        with st.spinner("Processing..."):
            response = predict(query_input_txt, file_upload, task_selection)
            st.text_area("Model Response", response, height=150)
            st.success("Query processed and logged successfully.")
