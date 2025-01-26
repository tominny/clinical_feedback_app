import streamlit as st
import openai
from db.db_manager import DBManager
from utils.file_processing import extract_text_from_file
from utils.pdf_export import generate_feedback_pdf
import os
import base64

def show_logo():
    with open("images/NILE_Lab.jpg", "rb") as f:
        logo_data = f.read()
    encoded = base64.b64encode(logo_data).decode()
    st.markdown(
        f"""
        <a href="https://geiselmed.dartmouth.edu/thesen/" target="_blank">
            <img src="data:image/jpg;base64,{encoded}" 
                 alt="NILE Lab Logo" 
                 style="width: 150px;" />
        </a>
        """,
        unsafe_allow_html=True
    )

def main_page():
    # Show the logo on top
    show_logo()

    st.title("Clinical Note Feedback")

    openai.api_key = st.secrets["openai"]["api_key"]

    db = DBManager(
        host=st.secrets["database"]["host"],
        database=st.secrets["database"]["database"],
        user=st.secrets["database"]["user"],
        password=st.secrets["database"]["password"],
        port=st.secrets["database"]["port"]
    )

    if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
        st.warning("Please log in first.")
        return

    user_id = st.session_state["user_id"]

    # Upload logic, generate feedback logic, etc.
    st.markdown("### Upload Your Files")
    file1 = st.file_uploader("Upload File 1", type=["pdf", "docx", "txt"])
    file2 = st.file_uploader("Upload File 2", type=["pdf", "docx", "txt"])
    file3 = st.file_uploader("Upload File 3", type=["pdf", "docx", "txt"])
    ...

def run():
    main_page()
