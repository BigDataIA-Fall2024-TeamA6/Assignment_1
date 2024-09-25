import streamlit as st
from db import DBConnection



def show():
    # Connect to Amazon RDS Database
    db = DBConnection.get_instance()
    cursor = db.cursor

    st.title("GAIA Benchmark App - Test Case Page")
    
    #Code for page 2
    tc_result = st.session_state.get("tc_result")
    #Column order - Serial_no, task_id, question, final_answer, file_name, file_path, annotator_metadata, validation_status
    

    # Test case window
    st.write(f"Selected Question: {tc_result[0][3]}")
    
    # Output window placeholder
    st.text_area("Output", "LLM Output to be printed here")


    st.write("Expected Output", f"{tc_result[0][4]}")
    
    # Correct and Wrong buttons
    if st.button("Correct"):
        cursor.execute(f"UPDATE validation_table  SET validation_status = 1 WHERE serial_no = {tc_result[0][1]}")
        db.connection.commit()
        st.write("LLM Output Validated")
    if st.button("Wrong"):
        st.session_state["page"] = "3_Test_Case"
