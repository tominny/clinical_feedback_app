import streamlit as st
from db.db_manager import DBManager
from utils.security import check_password

def login_page():
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

                # Switch to "Main" and force a page reload (JavaScript)
                st.session_state["choice"] = "Main"
                st.write(
                    """
                    <script>
                    window.location.reload();
                    </script>
                    """,
                    unsafe_allow_html=True
                )

            else:
                st.error("Invalid username or password.")
        else:
            st.error("Invalid username or password.")

def run():
    if "logged_in" in st.session_state and st.session_state["logged_in"]:
        st.write("You are already logged in.")
        st.write("Go to the Main page from the sidebar.")
    else:
        login_page()
