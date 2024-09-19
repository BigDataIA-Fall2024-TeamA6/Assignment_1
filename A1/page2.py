import streamlit as st

def show():
    st.title("GAIA Benchmark App - Test Case Page")
    
    # Your code for page 2
    # Example:
    st.write("This is Page 2")

    # Test case window
    selected_question = st.session_state.get("selected_question", "No question selected")
    st.write(f"Test Case: {selected_question}")
    
    # Output window placeholder
    st.text_area("Output", "LLM's output will be displayed here...")
    
    # Correct and Wrong buttons
    if st.button("Correct"):
        st.write("Correct clicked")  # Placeholder action
    if st.button("Wrong"):
        st.session_state["page"] = "page3"
