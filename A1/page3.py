import os
import tiktoken
import pandas as pd
import streamlit as st
from openai import OpenAI
from db import DBConnection
from dotenv import load_dotenv

def count_tokens(text, model="gpt-4"):    
    # Count the number of tokens in the text using the OpenAI tokenization system.
    encoding = tiktoken.encoding_for_model(model)
    return len(encoding.encode(text))

def chunk_text(text, max_tokens=4000, model="gpt-4"):
    # Chunk text into smaller pieces to fit within the token limit.
    encoding = tiktoken.encoding_for_model(model)
    tokens = encoding.encode(text)

    # Split tokens into chunks of max_tokens size
    chunks = [tokens[i:i + max_tokens] for i in range(0, len(tokens), max_tokens)]

    # Convert token chunks back to text
    chunked_texts = [encoding.decode(chunk) for chunk in chunks]
    return chunked_texts
 
def show():
    st.title("Assist LLM Page")
    db = DBConnection.get_instance()
    cursor = db.cursor
    load_dotenv()
    # Initialize OpenAI client with the API key
    api_key = os.getenv("OPENAI_API_KEY")  # OpenAI API key
    client = OpenAI(api_key=api_key)
   
 
    # Test case window
    tc_result = st.session_state.get("tc_result")
    st.write(f"Test Case: {tc_result[0][3]}") # Question
 
   
    # Output window placeholder
    st.text_area(f"Input the steps:", tc_result[0][7]) # Annotator_metadata
    st.write("Expected Output:", f"{tc_result[0][4]}") # Final Answer 
   
    file_content = st.session_state.get('file_content')
 
    if file_content is not None and isinstance(file_content, pd.DataFrame) and not file_content.empty:
        # If the DataFrame is not empty, convert it to a string or process it further
        file_content = file_content.head(50)  # Convert DataFrame to string to be used later
        file_content = file_content.to_string()
    else:
        pass  # If the DataFrame is empty or None, set it as an empty string
 
    chatgpt_prompt = "File Contents:" + file_content + "\n" +  tc_result[0][3] + "\n" + tc_result[0][7]
 
    if st.button("Search"):
                try:
                    token_count = count_tokens(chatgpt_prompt)
                    st.write(f"Token count: {token_count}")
                    if token_count > 7000:
                        st.warning("Content is too large. Chunking the content.")
                        chunks = chunk_text(file_content, max_tokens=3000)
                        for chunk in chunks:
                            # OpenAI API call - pass chunked content along with the question
                            response_updated = client.chat.completions.create(
                                model="gpt-4",
                                messages=[
                                    {"role": "user", "content": f"File content:\n{chunk}\n\nQuestion: {chatgpt_prompt}"}
                                ],
                                max_tokens=3000  # Use a reasonable limit per request
                            )
                    else:
                        
                    # OpenAI API call - pass the question directly without file content
                        response_updated = client.chat.completions.create(
                        model="gpt-4",
                        messages=[
                            {"role": "user", "content": f"Question: {chatgpt_prompt}"}
                        ],
                        max_tokens=3000  # Use a reasonable limit per request
                        )
 
                    # Safely access the choices if available
                    if response_updated.choices and len(response_updated.choices) > 0:
                        openai_response_content = response_updated.choices[0].message.content
                        # Output window with the OpenAI response in a text area
                        st.text_area("LLM Updated Output", openai_response_content)
                        st.success("Response from OpenAI successfully received!")
 
                        # Navigate to page 3 to display the response
                        st.session_state["page"] = "3_Test_Case"
                   
                    else:
                        st.error("Unexpected API response format. No choices found.")
                except Exception as e:
                    st.error(f"Error during OpenAI API call: {e}")
 
    # Create two columns for the Correct and Wrong buttons
    col1, col2 = st.columns(2)
 
    with col1:
        if st.button("Correct"):
            cursor.execute(f"UPDATE validation_table  SET validation_status = 2 WHERE serial_no = {tc_result[0][1]}")
            db.connection.commit()
            st.write("LLM Output Validated")
 
    with col2:
        if st.button("Wrong"):
            cursor.execute(f"UPDATE validation_table  SET validation_status = 3 WHERE serial_no = {tc_result[0][1]}")
            db.connection.commit()
            
 
    if st.button("Go to Home"):
        st.session_state["page"] = "Home"
 