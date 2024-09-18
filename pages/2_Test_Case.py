import streamlit as st

st.set_page_config(page_title="Test Case Details", layout="wide")

st.title("Test Case Details")

# Display the selected test case question
selected_question = st.session_state.get("selected_question", "No question selected")
st.subheader("Test Case")
st.write(selected_question)

# Placeholder for LLM output
st.subheader("Output")
st.write("This is a placeholder for the LLM's solution.")

# Buttons for marking correctness
col1, col2 = st.columns(2)
if col1.button("Correct"):
    # Add logic to update the database
    st.success("Marked as correct!")

if col2.button("Wrong"):
    # Navigate to the third page
    st.session_state["page"] = "3_Suggestion"