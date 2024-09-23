import streamlit as st
from db import DBConnection

def show():
    st.title("GAIA Benchmark App - Assist LLM Page")
    
    # Connect to the database
    try:
        db = DBConnection.get_instance()
        cursor = db.get_cursor()
    except Exception as e:
        st.error(f"Error connecting to the database: {e}")
        return
    
    # Check if tc_result is stored in session state
    tc_result = st.session_state.get("tc_result")

    if tc_result:
        # Display the test case information
        st.write(f"Test Case: {tc_result[0][2]}")
        
        # Output window placeholder
        st.text_area("Input the steps:", "Generating New prompt...")
        
        # Correct and Wrong buttons
        if st.button("Correct"):
            cursor.execute(f"UPDATE validation_table SET validation_status = 2 WHERE serial_no = {tc_result[0][0]}")
            db.connection.commit()
        
        if st.button("Wrong"):
            cursor.execute(f"UPDATE validation_table SET validation_status = 3 WHERE serial_no = {tc_result[0][0]}")
            db.connection.commit()
    else:
        st.error("No test case data available. Please go back and select a test case.")

    # Go to Home button
    if st.button("Go to Home"):
        st.session_state["page"] = "Home"
        st.experimental_rerun()
