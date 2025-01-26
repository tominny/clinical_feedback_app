
import streamlit as st
from db.db_manager import DBManager
from utils.security import hash_password
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

def signup_page():
    # Show logo
    show_logo()

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
        if not username or not password or not confirm_password:
            st.error("Please fill out all fields.")
            return
        if password != confirm_password:
            st.error("Passwords do not match.")
            return

        user = db.get_user_by_username(username)
        if user:
            st.error("Username already exists.")
            return

        hashed_pw = hash_password(password)
        db.insert_user(username, hashed_pw)
        st.success("Account created successfully! Go to the Login page.")

def run():
    signup_page()
