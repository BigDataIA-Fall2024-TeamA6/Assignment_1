import pandas as pd
import streamlit as st
import mysql.connector

# Connect to Amazon RDS Database
connection = mysql.connector.connect(
host='database-1.cdwumcckkqqt.us-east-1.rds.amazonaws.com',
user='admin',
password='amazonrds7245',
database='gaia_benchmark_dataset_validation')

cursor = connection.cursor()

query = 'SELECT * FROM validation_table;'
cursor.execute(query)
validation_table = cursor.fetchall()
st.session_state["results"] = validation_table

def show():
    st.title("GAIA Benchmark Evaluation App")

    # Fetch test cases from Amazon RDS
    test_cases = pd.DataFrame(validation_table,columns = cursor.column_names)
    test_case_options = dict(zip(test_cases['serial_no'],test_cases['question']))

    # Dropdown for selecting test case
    selected_test_case = st.selectbox("Select a Test Case:", options=test_case_options.keys(),key="select_test_case")

    # Display the selected question
    if selected_test_case:
        selected_question = test_case_options[selected_test_case]
        st.write(f"Question: {selected_question}")

    # Search button
    if st.button("Search"):
        st.session_state["serial_no"] = selected_test_case
        st.session_state["page"] = "2_Test_Case"

    # Button to navigate to summary page
    if st.button("Go to Summary"):
        st.session_state["page"] = "summary"

