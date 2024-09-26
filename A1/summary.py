import streamlit as st
import pandas as pd
from db import DBConnection

def show():
    st.title("Summary Page")

    db = DBConnection.get_instance()
    cursor = db.cursor

    # Querying the validation_status counts from the database
    query1 = """
    SELECT validation_status, COUNT(*) as count 
    FROM validation_table 
    GROUP BY validation_status
    """
    cursor.execute(query1)
    result1 = cursor.fetchall()

    # Processing the query result into a DataFrame
    status_counts = pd.DataFrame(result1, columns=["Validation Status", "Count"])

    # Mapping the validation_status values to more descriptive labels
    status_label_mapping = {
        0: "Not Tested",
        1: "No Assistance",
        2: "With Assistance",
        3: "Failed"
    }
    status_counts["Validation Status"] = status_counts["Validation Status"].map(status_label_mapping)

    # Placeholder for performance chart
    st.subheader("Validation Status Performance Chart")
    st.bar_chart(status_counts.set_index("Validation Status"))

    # Query for counts based on file_path being NULL or NOT NULL
    query2 = """
    SELECT 
        CASE WHEN file_path IS NULL THEN 'No File' ELSE 'Has File' END AS file_path_status,
        COUNT(CASE WHEN validation_status = 0 THEN 1 END) AS count_status_0,
        COUNT(CASE WHEN validation_status != 0 THEN 1 END) AS count_status_not_0
    FROM validation_table
    GROUP BY file_path_status
    """
    cursor.execute(query2)
    result2 = cursor.fetchall()

    # Processing the query result into a DataFrame
    file_path_counts = pd.DataFrame(result2, columns=["External File", "Count of Question Not Tested", "Count of Question Tested"])

    # Display the table for file_path and validation_status counts
    st.subheader("Validation Status for Document-Linked Questions")
    st.table(file_path_counts)

    # Navigation buttons
    if st.button("Go to Home"):
        st.session_state["page"] = "Home"
