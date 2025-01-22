
import streamlit as st
import uuid
from pathlib import Path
import json
#from huggingface_hub import CommitScheduler
from datetime import datetime

# # Configure logging
# log_file = Path("logs/") / f"data_{uuid.uuid4()}.json"
# log_folder = log_file.parent
# log_folder.mkdir(parents=True, exist_ok=True)  # Ensure the folder exists

# # Initialize CommitScheduler
# scheduler = CommitScheduler(
#     repo_id="Research-to-Product-logs",
#     repo_type="dataset",
#     folder_path=log_folder,
#     path_in_repo="data",
#     every=2  # Commit logs every 2 entries
# )

def predict(query, file_path, task):

    # with scheduler.lock:
    #     with log_file.open("a") as f:
    #         f.write(json.dumps(
    #             {
    #                 'query': query,
    #                 "task": task,
    #                 #"response": response,
    #                 "file_name": file_name,
    #                 "timestamp": datetime.now().isoformat()  # Add timestamp
    #                 #'model_response': prediction
    #             }
    #         ))
    #         f.write("\n")       
    return f" file_path:'{file_path}' query: '{query}' task: '{task}' "

    
    
    #return f"mime_type:'{mime_type}' pdf_path:'{pdf_path}' saved_file_path:'{saved_file_path}' page_count:'{page_count}' file_path:'{file_path}' query: '{query}' mime_type: '{mime_type}' "
     

# # Function to log data
# def log_data(query, task, response, file_name=None):
#     log_entry = {
#         "query": query,
#         "task": task,
#         "response": response,
#         "file_name": file_name,
#         "timestamp": datetime.now().isoformat()
#     }
#     with open(log_file, "a") as log:
#         log.write(json.dumps(log_entry) + "\n")
#     #scheduler.step()  # Schedule the commit
    
#     # Attempt to step the scheduler
#     try:
#         scheduler.step()  # Schedule the commit
#     except Exception as e:
#         st.error(f"Failed to commit logs: {e}")

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
            #log_data(query_input_txt, task_selection, response, file_name)
            st.success("Query processed and logged successfully.")
