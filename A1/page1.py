import streamlit as st
from openai import OpenAI
import pandas as pd
import boto3
from io import BytesIO
from db import DBConnection
# import PyPDF2
# from pptx import Presentation
# import docx
# import zipfile
# from PIL import Image
# import pytesseract
import os
from pydub import AudioSegment
import speech_recognition as sr
import tiktoken  # OpenAI's token counter library
from dotenv import load_dotenv

load_dotenv() 
# Securely get environment variables
api_key = os.getenv("OPENAI_API_KEY")  # OpenAI API key
aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")  # AWS access key
aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")  # AWS secret key
aws_region = os.getenv("AWS_REGION", "us-east-1")  # AWS region, default to us-east-1

# Initialize OpenAI client with the API key
client = OpenAI(api_key=api_key)

# Initialize Boto3 client for S3
s3_client = boto3.client(
    's3',
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
    region_name=aws_region
)

# Add handling for .xlsx files
def get_s3_file_content(s3_url):
    try:
        # Determine the S3 bucket and object key
        if s3_url.startswith("s3://"):
            bucket_name = s3_url.split('/')[2]
            object_key = '/'.join(s3_url.split('/')[3:])
        elif "s3.amazonaws.com" in s3_url:
            parts = s3_url.split('/')
            bucket_name = parts[2].split('.')[0]  # Extract bucket name
            object_key = '/'.join(parts[3:])     # Extract object key
        else:
            raise ValueError("Invalid S3 URL format")

        # Fetch the object from S3
        response = s3_client.get_object(Bucket=bucket_name, Key=object_key)
        content_type = response['ContentType']
        content = response['Body'].read()

        # Log for debugging purposes
        st.write(f"Bucket: {bucket_name}, Key: {object_key}, ContentType: {content_type}")

        # Detect and handle different file formats
        if content_type == 'application/pdf':
            return extract_text_from_pdf(content)
        elif content_type == 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet':
            return pd.read_excel(BytesIO(content))  # Handle .xlsx files
        elif content_type == 'application/vnd.openxmlformats-officedocument.presentationml.presentation':
            return extract_text_from_pptx(content)
        elif content_type == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
            return extract_text_from_docx(content)
        elif content_type == 'image/png' or content_type == 'image/jpeg':
            return extract_text_from_image(content)  # OCR for PNG/JPG
        elif content_type == 'text/csv':
            return pd.read_csv(BytesIO(content))
        elif content_type == 'audio/mpeg':
            return extract_text_from_audio(content)
        elif content_type == 'application/zip':
            return extract_text_from_zip(content)
        else:
            # Try to decode as UTF-8 if it's a plain text file
            try:
                return content.decode('utf-8')
            except UnicodeDecodeError:
                st.error(f"Cannot decode the file content at {s3_url} as text. It might be a binary file.")
                return None

    except Exception as e:
        st.error(f"Error processing S3 file: {e}")
        raise

def show():
    st.title("GAIA Benchmark Evaluation App")

    # Fetch test cases from MongoDB
    test_cases = collection.find({}, {"task_id": 1, "Question": 1})
    test_case_options = {str(tc["task_id"]): tc["Question"] for tc in test_cases}

    # Dropdown for selecting test case
    selected_test_case = st.selectbox("Select a Test Case:", options=list(test_case_options.keys()))

    # Display the selected question
    if selected_test_case:
        selected_question = test_case_options[selected_test_case]
        file_path_series = test_cases[test_cases['serial_no'] == selected_test_case]['file_path']

        if not file_path_series.empty:
            file_path = file_path_series.values[0]
        else:
            file_path = None

        st.session_state['selected_test_case'] = selected_test_case  # Save selected test case in session state
        st.session_state['selected_question'] = selected_question    # Save selected question in session state

        # Display selected question
        st.write(f"Question: {selected_question}")

        # Only attempt to access file if file_path is available
        if file_path:
            st.write(f"Accessing File: {file_path.split('/')[-1]}")  # Print the file name with extension

            # Search button - trigger OpenAI API call when clicked
            if st.button("Test"):
                try:
                    # Access the file content from S3
                    file_content = get_s3_file_content(file_path)

                    if file_content is None:
                        # If file content could not be retrieved (e.g., binary file)
                        st.error("The file cannot be processed because it is not in a valid text format.")
                    elif isinstance(file_content, pd.DataFrame):
                        # If the file is an Excel file (DataFrame), limit the number of rows/columns to reduce size
                        st.write("Excel File Content (limited view):")
                        limited_content = file_content.head(10)  # Limit to the first 10 rows
                        st.dataframe(limited_content)  # Display the DataFrame in the Streamlit app

                        # Convert the limited DataFrame content to a string for the OpenAI API call
                        limited_content_str = limited_content.to_string()

                        # OpenAI API call - pass limited file content along with the question
                        response = client.chat.completions.create(
                            model="gpt-4",
                            messages=[
                                {"role": "user", "content": f"File content:\n{limited_content_str}\n\nQuestion: {selected_question}"}
                            ],
                            max_tokens=7000  # Adjust token limit for larger inputs
                        )

                        # Safely access the choices if available
                        if response.choices and len(response.choices) > 0:
                            openai_response_content = response.choices[0].message.content
                            st.session_state["openai_response"] = openai_response_content
                            st.success("Response from OpenAI successfully received!")

                            # Navigate to page 2 to display the response
                            st.session_state["page"] = "2_Test_Case"
                            
                        else:
                            st.error("Unexpected API response format. No choices found.")
                    else:
                        # Handle plain text file content
                        token_count = count_tokens(file_content)
                        st.write(f"Token count: {token_count}")

                        if token_count > 7000:
                            st.warning("Content is too large. Chunking the content.")
                            chunks = chunk_text(file_content, max_tokens=3000)
                        else:
                            chunks = [file_content]

                        for chunk in chunks:
                            # OpenAI API call - pass chunked content along with the question
                            response = client.chat.completions.create(
                                model="gpt-4",
                                messages=[
                                    {"role": "user", "content": f"File content:\n{chunk}\n\nQuestion: {selected_question}"}
                                ],
                                max_tokens=3000  # Use a reasonable limit per request
                            )

                            if response.choices and len(response.choices) > 0:
                                openai_response_content = response.choices[0].message.content
                                st.session_state["openai_response"] = openai_response_content
                                st.success("Response from OpenAI successfully received!")

                                # Navigate to page 2 to display the response
                                st.session_state["page"] = "2_Test_Case"
                                
                            else:
                                st.error("Unexpected API response format. No choices found.")

                except Exception as e:
                    st.error(f"Error during OpenAI API call or S3 file access: {e}")

        else:
            # If no file path is available, answer based on the question only
            st.warning("No file path found. Answering based on the question only.")
            if st.button("Search"):
                try:
                    # OpenAI API call - pass the question directly without file content
                    response = client.chat.completions.create(
                        model="gpt-4",
                        messages=[
                            {"role": "user", "content": f"Question: {selected_question}"}
                        ],
                        max_tokens=3000  # Use a reasonable limit per request
                    )

                    # Safely access the choices if available
                    if response.choices and len(response.choices) > 0:
                        openai_response_content = response.choices[0].message.content
                        st.session_state["openai_response"] = openai_response_content
                        st.success("Response from OpenAI successfully received!")

                        # Navigate to page 2 to display the response
                        st.session_state["page"] = "2_Test_Case"
                    
                    else:
                        st.error("Unexpected API response format. No choices found.")
                except Exception as e:
                    st.error(f"Error during OpenAI API call: {e}")

        # Add the "Go to Summary" button
        if st.button("Go to Summary"):
            st.session_state["page"] = "summary"

