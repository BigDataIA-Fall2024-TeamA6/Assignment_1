import streamlit as st
from db import DBConnection

from openai import OpenAI
from dotenv import load_dotenv
import os
 
def show():
    st.title("GAIA Benchmark App - Assist LLM Page")
    db = DBConnection.get_instance()
    cursor = db.cursor
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")  # OpenAI API key
   
 
    # Initialize OpenAI client with the API key
    client = OpenAI(api_key=api_key)
 
    st.write("This is Page 3")
 
    # Test case window
    tc_result = st.session_state.get("tc_result")
    st.write(f"Test Case: {tc_result[0][3]}")
 
   
    # Output window placeholder
    st.text_area(f"Input the steps:", tc_result[0][7])
   
    chatgpt_prompt = tc_result[0][3] + "\n" + tc_result[0][7]
 
    if st.button("Search"):
                try:
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
 
                        # Navigate to page 2 to display the response
                        st.session_state["page"] = "3_Test_Case"
                   
                    else:
                        st.error("Unexpected API response format. No choices found.")
                except Exception as e:
                    st.error(f"Error during OpenAI API call: {e}")
 
 
    # Correct and Wrong buttons
    if st.button("Correct"):
        cursor.execute(f"UPDATE validation_table  SET validation_status = 2 WHERE serial_no = {tc_result[0][1]}")
        db.connection.commit()
       
    if st.button("Wrong"):
        cursor.execute(f"UPDATE validation_table  SET validation_status = 3 WHERE serial_no = {tc_result[0][1]}")
        db.connection.commit()
       
 
    if st.button("Go to Home"):
        st.session_state["page"] = "Home"
