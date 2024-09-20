import streamlit as st
import pandas as pd
# add_selectbox = st.sidebar.selectbox(
#     'Page',
#     ('Home', 'Page1', 'Page2', 'Summary')
# )

# Set the page configuration only once, at the top of app.py
st.set_page_config(page_title="GAIA Benchmark App", layout="wide")

def main():
    # Import pages here (after setting the page config)
    import page1
    import page2
    import summary

    # Logic to navigate to different pages
    if st.session_state.get("page") == "2_Test_Case":
        page2.show()
    elif st.session_state.get("page") == "3_Test_Case":
        page3.show()
    elif st.session_state.get("page") == "summary":
        summary.show()
    else:
        page1.show()

if __name__ == "__main__":
    main()
