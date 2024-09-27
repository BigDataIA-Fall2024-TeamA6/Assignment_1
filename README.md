# Assignment 1 - GAIA Dataset Model Evaluation Tool

### Contributors:
- Sahiti Nallamolu
- Vishodhan Krishnan
- Vismay Devjee

## Synopsis

This project involves building a **Streamlit-based tool** for the Model Evaluation team to select and evaluate test cases from the **GAIA dataset** against **OpenAI's language models**. The tool provides an intuitive interface for selecting test cases, interacting with OpenAI's API, and visualizing the evaluation results. Users can compare the model responses with expected outputs, give feedback, and visualize model performance.

### Technologies Used:
- **Streamlit**: Web application frontend
- **OpenAI API**: Model evaluation
- **Python**: Backend logic and data processing
- **Matplotlib/Plotly**: Visualizing the evaluation results
- **Amazon S3**: Storage of unstructured data (e.g., files)
- **Amazon RDS**: Storage of structured data (e.g., validation statuses, test cases)
- **GAIA Dataset**: Validation data from Hugging Face

## Problem Statement

The primary goal of this project is to develop a tool that allows efficient evaluation of OpenAI’s language models on test cases from the GAIA dataset. It addresses the following challenges:
- Selecting and evaluating test cases
- Interfacing with OpenAI API for model evaluation
- Integrating structured and unstructured data from Amazon S3 and Amazon RDS
- Recording user feedback for each evaluated test case
- Generating insightful visualizations to understand model performance

## Desired Outcome
The application allows:
- Interactive test case selection from GAIA dataset
- Model evaluation through OpenAI API
- User feedback collection for validation
- Visual insights to track model performance

---

## Steps to Run this Application

1. Clone this repository to your local machine.
2. Install all required dependencies:
    ```bash
    pip install -r requirements.txt
    ```
3. Add your credentials to a `.env` file under the `A1/` folder:
   - AWS Access Key
   - AWS Secret Access Key
   - OpenAI API Key

4. Run the application:
    ```bash
    streamlit run A1/app.py
    ```
5. In the application, select a test case from the dropdown menu.
6. Click "Search" to retrieve model output and compare it with the "Expected Output".
7. Provide feedback on the model's response using the "Correct" or "Wrong" buttons.
8. View the results summary with visual insights by clicking the "Summary" button.

---

## File Structure

Assignment_1/
A1/
    app.py: Main Streamlit application
    page1.py: First page logic (Test case selection)
    page2.py: Second page logic (Model evaluation)
    page3.py: Third page logic (Feedback recording)
    .env: Credentials for AWS and OpenAI
architecture_diagram/: Contains the workflow diagram for the system
scripts/: Contains Python scripts for data migration
validation/: Contains the data files for validation
README.md: Project documentation
requirements.txt: Dependencies for the project

