#%%writefile /content/drive/MyDrive/ColabNotebooks-2/app.py
import os
import json
import streamlit as st
from datetime import datetime
from google.cloud import documentai_v1 as documentai
from google.oauth2 import service_account

def save_uploaded_file(file_path):
  
    UPLOAD_DIR = "./saved_uploads"
    os.makedirs(UPLOAD_DIR, exist_ok=True)

    """Saves the uploaded file to a permanent location."""
    if not file_path:
        return None, "No file uploaded!"

    # Extract filename from the uploaded path
    filename = os.path.basename(file_path)
    saved_file_path = os.path.join(UPLOAD_DIR, filename)

    # Copy the uploaded file to the permanent directory
    shutil.copy(file_path, saved_file_path)
    return saved_file_path, f"File saved at: {saved_file_path}"
  

def process_pdf(pdf_path):
  # Load credentials from Azure environment variable
  credentials_info = json.loads(os.environ["GCP_SERVICE_ACCOUNT_KEY"])
  credentials = service_account.Credentials.from_service_account_info(credentials_info)

  # Initialize Google Document AI Client
  client = documentai.DocumentProcessorServiceClient(credentials=credentials)

  # Define Google Document AI processor
  project_id = "myfirstocrvisionproject"
  location = "us"  # Adjust if needed
  processor_id = "7670b830a0fd8325"
  processor_name = f"projects/{project_id}/locations/{location}/processors/{processor_id}"

  #prediction_endpoint="https://us-documentai.googleapis.com/v1/projects/261324698708/locations/us/processors/7670b830a0fd8325:process"
  
  # Load PDF file from local or Azure Blob Storage
  with open("pdf_path", "rb") as file:
      raw_document = documentai.RawDocument(content=file.read(), mime_type="application/pdf")

  # Send document for processing
  request = documentai.ProcessRequest(name=processor_name, raw_document=raw_document)
  result = client.process_document(request=request)

  # Print extracted text
  print(result.document.text)
  

def predict(query, file_path, task):
  # Save the uploaded file to local directory
  saved_file_path, save_msg = save_uploaded_file(file_path)
  document_text = process_pdf(saved_file_path)
  return f"document_text:{document_text} \n\n\nfile_path:'{file_path}' query: '{query}' task: '{task}'  "


# Define the Streamlit UI
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
file_name = file_upload.name if file_upload else None

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
    elif not query_input_txt:
        st.error("Please enter a query.")
    else:
        # Simulating the predict function call
        with st.spinner("Processing..."):
            response = predict(query_input_txt, file_upload, task_selection)
            st.text_area("Model Response", response, height=150)

            # Log the data
            st.success("Query processed and logged successfully.")


#_________________________________

# import streamlit as st
# import uuid
# from pathlib import Path
# import json
# #from huggingface_hub import CommitScheduler
# from datetime import datetime

# # # Configure logging
# # log_file = Path("logs/") / f"data_{uuid.uuid4()}.json"
# # log_folder = log_file.parent
# # log_folder.mkdir(parents=True, exist_ok=True)  # Ensure the folder exists

# # # Initialize CommitScheduler
# # scheduler = CommitScheduler(
# #     repo_id="Research-to-Product-logs",
# #     repo_type="dataset",
# #     folder_path=log_folder,
# #     path_in_repo="data",
# #     every=2  # Commit logs every 2 entries
# # )

# def predict(query, file_path, task):

#     # with scheduler.lock:
#     #     with log_file.open("a") as f:
#     #         f.write(json.dumps(
#     #             {
#     #                 'query': query,
#     #                 "task": task,
#     #                 #"response": response,
#     #                 "file_name": file_name,
#     #                 "timestamp": datetime.now().isoformat()  # Add timestamp
#     #                 #'model_response': prediction
#     #             }
#     #         ))
#     #         f.write("\n")       
#     return f" file_path:'{file_path}' query: '{query}' task: '{task}' "

    
    
#     #return f"mime_type:'{mime_type}' pdf_path:'{pdf_path}' saved_file_path:'{saved_file_path}' page_count:'{page_count}' file_path:'{file_path}' query: '{query}' mime_type: '{mime_type}' "
     

# # # Function to log data
# # def log_data(query, task, response, file_name=None):
# #     log_entry = {
# #         "query": query,
# #         "task": task,
# #         "response": response,
# #         "file_name": file_name,
# #         "timestamp": datetime.now().isoformat()
# #     }
# #     with open(log_file, "a") as log:
# #         log.write(json.dumps(log_entry) + "\n")
# #     #scheduler.step()  # Schedule the commit
    
# #     # Attempt to step the scheduler
# #     try:
# #         scheduler.step()  # Schedule the commit
# #     except Exception as e:
# #         st.error(f"Failed to commit logs: {e}")

# # Define the Streamlit UI
# st.title("Research Paper Processor")
# st.write("Upload a PDF, enter your query, and choose a task.")

# # Query input text box
# query_input_txt = st.text_area(
#     "Query Input",
#     placeholder="Enter your query here",
#     height=150
# )

# # File upload
# file_upload = st.file_uploader("Upload PDF", type=["pdf"])
# file_name = file_upload.name if file_upload else None

# # Task selection radio buttons
# task_selection = st.radio(
#     "Select Task",
#     options=["Summarize", "Extract Use Cases", "Generate PRD"],
#     index=0  # Default selection
# )

# # Submit button
# if st.button("Submit"):
#     if file_upload is None:
#         st.error("Please upload a PDF file.")
#     elif not query_input_txt:
#         st.error("Please enter a query.")
#     else:
#         # Simulating the predict function call
#         with st.spinner("Processing..."):
#             response = predict(query_input_txt, file_upload, task_selection)
#             st.text_area("Model Response", response, height=150)

#             # Log the data
#             #log_data(query_input_txt, task_selection, response, file_name)
#             st.success("Query processed and logged successfully.")
