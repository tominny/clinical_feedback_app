import streamlit as st
from db.db_manager import DBManager
from utils.security import hash_password

def signup_page():
    # Add clickable logo at top
    st.markdown(
        """
        [![NILE Lab logo](../images/NILE_Lab.jpg)](https://geiselmed.dartmouth.edu/thesen/)
        """,
        unsafe_allow_html=True
    )

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
        # Check if username already exists
        user = db.get_user_by_username(username)
        if user:
            st.error("Username already exists, choose another.")
            return

        hashed_pw = hash_password(password)
        db.insert_user(username, hashed_pw)
        st.success("Account created successfully! Go to the Login page.")

def run():
    signup_page()
