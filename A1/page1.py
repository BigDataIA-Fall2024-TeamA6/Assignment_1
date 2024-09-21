import pandas as pd
import streamlit as st
from db import DBConnection


    # Connect to Amazon RDS Database
db = DBConnection.get_instance()
cursor = db.cursor
cursor.execute('SELECT * FROM validation_table;')
validation_table = cursor.fetchall()
    
    

# Fetch test cases from Amazon RDS
test_cases = pd.DataFrame(validation_table,columns=cursor.column_names)

def show():
    st.title("GAIA Benchmark Evaluation App")

    test_case_options = dict(zip(test_cases['serial_no'],test_cases['question']))

    # Dropdown for selecting test case
    selected_test_case = st.selectbox("Select a Test Case:", options=test_case_options.keys(),key="select_test_case")

    # Fetch the  details for the selected test case
    cursor.execute("SELECT * FROM validation_table WHERE serial_no = " + str(selected_test_case) + ";")
    st.session_state['tc_result'] = cursor.fetchall()

    # Display the selected question
    if selected_test_case:
        selected_question = test_case_options[selected_test_case]
        st.write(f"Question: {selected_question}")

    # Search button
    if st.button("Search"):
        st.session_state["page"] = "2_Test_Case"

    # Button to navigate to summary page
    if st.button("Go to Summary"):
        st.session_state["page"] = "summary"

