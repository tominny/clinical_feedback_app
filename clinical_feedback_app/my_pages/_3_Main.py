import streamlit as st
import openai
from db.db_manager import DBManager
from utils.file_processing import extract_text_from_file
from utils.pdf_export import generate_feedback_pdf
import os
import base64

def show_logo():
    this_file_dir = os.path.dirname(__file__)
    logo_path = os.path.join(this_file_dir, "..", "images", "NILE_Lab.jpg")
    with open(logo_path, "rb") as f:
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
    show_logo()  # display the logo

    st.title("Clinical Note Feedback")
    # ... the rest of your code ...

def run():
    main_page()
