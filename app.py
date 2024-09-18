import streamlit as st
from pymongo import MongoClient

import mysql.connector
 

connection = mysql.connector.connect(
host='database-1.cdwumcckkqqt.us-east-1.rds.amazonaws.com',
user='admin',
password='amazonrds7245',
database='gaia_benchmark_dataset_validation'
)

# # MongoDB connection
# client = MongoClient("mongodb://localhost:27017/")
# db = client["Test1"]
# collection = db["1Case"]

st.set_page_config(page_title="GAIA Benchmark App", layout="wide")

st.title("GAIA Benchmark Evaluation App")

# Fetch test cases from MongoDB
test_cases = collection.find({}, {"task_id": 1, "Question": 1})
test_case_options = {str(tc["task_id"]): tc["Question"] for tc in test_cases}

# Dropdown for selecting test case
selected_test_case = st.selectbox("Select a Test Case:", options=list(test_case_options.keys()))

# Display the selected question
if selected_test_case:
    selected_question = test_case_options[selected_test_case]
    st.write(f"Question: {selected_question}")

# Search button
if st.button("Search"):
    st.session_state["selected_question"] = selected_question
    st.session_state["page"] = "2_Test_Case"

# Button to navigate to summary page
if st.button("Go to Summary"):
    st.session_state["page"] = "Summary"