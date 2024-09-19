import streamlit as st

def show():
    st.title("GAIA Benchmark App - Assist LLM Page")
    
    # Your code for page 3
    # Example:
    st.write("This is Page 3")

    # Test case window
    selected_question = st.session_state.get("selected_question", "No question selected")
    st.write(f"Test Case: {selected_question}")
    
    # Output window placeholder
    st.text_area("Input the steps:", "Generating New prompt...")
    
    # Correct and Wrong buttons
    if st.button("Correct"):
        st.write("Correct clicked")  # Placeholder action
    if st.button("Wrong"):
        st.write("Correct clicked")  # Placeholder action
    if st.button("Go to Home"):
        st.session_state["page"] = "Home"
