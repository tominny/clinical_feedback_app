import streamlit as st
from db.db_manager import DBManager
from utils.security import hash_password
import base64
import os

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

def signup_page():
    show_logo()  # display the logo at top

    st.title("Sign Up")
    username = st.text_input("Choose a Username")
    password = st.text_input("Choose a Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")

    db = DBManager(
        host=st.secrets["database"]["host"],
        database=st.secrets["database"]["database"],
        user=st.secrets["database"]["user"],
        password=st.secrets["database"]["password"],
        port=st.secrets["database"]["port"]
    )

    if st.button("Sign Up"):
        # ... your signup logic ...
        pass

def run():
    signup_page()
