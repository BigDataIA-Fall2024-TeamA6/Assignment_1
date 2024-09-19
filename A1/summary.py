import streamlit as st
import pandas as pd

def show():
    st.title("Summary Page")

    # Placeholder for data table
    st.subheader("Summary Table")
    summary_data = {
        "Metric": ["Accuracy", "Precision", "Recall"],
        "Value": [0.85, 0.80, 0.75]
    }
    summary_df = pd.DataFrame(summary_data)
    st.table(summary_df)

    # Placeholder for bar chart
    st.subheader("Performance Chart")
    chart_data = pd.DataFrame({
        "Metric": ["Accuracy", "Precision", "Recall"],
        "Value": [0.85, 0.80, 0.75]
    })
    st.bar_chart(chart_data.set_index("Metric"))

    # Navigation buttons
    if st.button("Go to Home"):
        st.session_state["page"] = "Home"

    if st.button("Go to Results"):
        st.session_state["page"] = "Results"
