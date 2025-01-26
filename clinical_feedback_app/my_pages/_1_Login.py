import streamlit as st
from db.db_manager import DBManager
from utils.security import check_password
import base64
import os

def show_logo():
    # Get the absolute path to THIS file's directory (my_pages/)
    this_file_dir = os.path.dirname(__file__)  
    # Move one level up (..) to the parent folder, then into images/
    logo_path = os.path.join(this_file_dir, "..", "images", "NILE_Lab.jpg")

    # Read the local image file as bytes
    with open(logo_path, "rb") as f:
        logo_data = f.read()
    # Encode to base64
    encoded = base64.b64encode(logo_data).decode()

    # Create a clickable image linking to the given URL
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

def login_page():
    show_logo()  # Show the clickable logo at the top

    st.title("Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    db = DBManager(
        host=st.secrets["database"]["host"],
        database=st.secrets["database"]["database"],
        user=st.secrets["database"]["user"],
        password=st.secrets["database"]["password"],
        port=st.secrets["database"]["port"]
    )

    if st.button("Login"):
        user = db.get_user_by_username(username)
        if user:
            hashed_password = user["hashed_password"]
            if check_password(password, hashed_password):
                st.session_state["logged_in"] = True
                st.session_state["user_id"] = user["user_id"]
                st.session_state["username"] = user["username"]
                st.success("Logged in successfully!")
            else:
                st.error("Invalid username or password.")
        else:
            st.error("Invalid username or password.")

def run():
    if "logged_in" in st.session_state and st.session_state["logged_in"]:
        st.write("You are already logged in. Go to the Main page from the sidebar.")
    else:
        login_page()
