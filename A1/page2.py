import streamlit as st
from db import DBConnection
 
def show():
    # Connect to Amazon RDS Database
    try:
        db = DBConnection.get_instance()
        cursor = db.get_cursor()
    except Exception as e:
        st.error(f"Error connecting to the database: {e}")
        return
 
    st.title("Test Case Page")
 
    # Fetch the selected test case and question from session state
    selected_test_case = st.session_state.get('selected_test_case')
    selected_question = st.session_state.get('selected_question', "No question selected.")
   
    if not selected_test_case:
        st.error("No test case selected. Please go back and select a test case.")
        return
 
    # Display the selected question
    st.write(f"Selected Question: {selected_question}")
 
    # Fetch the OpenAI response from session state
    openai_response_content = st.session_state.get("openai_response", "No response received.")
   
    # Output window with the OpenAI response in a text area
    st.text_area("LLM Output", openai_response_content)
 
    # Fetch expected output from the database based on the selected test case
    cursor.execute(f"SELECT * FROM validation_table WHERE serial_no = {selected_test_case}")
    tc_result = cursor.fetchall()
 
    if tc_result:
        st.write("Expected Output", f"{tc_result[0][4]}")
 
        # Create two columns for the Correct and Wrong buttons
    col1, col2 = st.columns(2)
 
    with col1:
        if st.button("Correct"):
            cursor.execute(f"UPDATE validation_table SET validation_status = 1 WHERE serial_no = {tc_result[0][1]}")
            db.connection.commit()
            st.write("LLM Output Validated")
   
    with col2:
        if st.button("Wrong"):
            # Store tc_result in session state to use in page 3
            st.session_state["tc_result"] = tc_result
            st.session_state["page"] = "3_Test_Case"
 
    # Navigation buttons
    if st.button("Go to Home"):
        st.session_state["page"] = "Home"
 
 