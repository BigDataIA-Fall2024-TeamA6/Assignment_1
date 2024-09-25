import streamlit as st
from db import DBConnection

def show():
    st.title("GAIA Benchmark App - Assist LLM Page")
    db = DBConnection.get_instance()
    cursor = db.cursor

    
    st.write("This is Page 3")

    # Test case window
    tc_result = st.session_state.get("tc_result")
    st.write(f"Test Case: {tc_result[0][3]}")

    
    # Output window placeholder
    st.text_area(f"Input the steps:", tc_result[0][7])
    
    # Correct and Wrong buttons
    if st.button("Correct"):
        cursor.execute(f"UPDATE validation_table  SET validation_status = 2 WHERE serial_no = {tc_result[0][1]}")
        db.connection.commit()
        
    if st.button("Wrong"):
        cursor.execute(f"UPDATE validation_table  SET validation_status = 3 WHERE serial_no = {tc_result[0][1]}")
        db.connection.commit()
        
    if st.button("Go to Home"):
        st.session_state["page"] = "Home"
