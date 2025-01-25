import streamlit as st
from db.db_manager import DBManager

def main():
    st.set_page_config(page_title="Clinical Feedback App", layout="wide")

    # Initialize DB tables on startup (optional)
    db = DBManager(
        host=st.secrets["database"]["host"],
        database=st.secrets["database"]["database"],
        user=st.secrets["database"]["user"],
        password=st.secrets["database"]["password"],
        port=st.secrets["database"]["port"]
    )
    db.create_tables()

    # 1) Initialize "choice" in session state if it doesn't exist
    if "choice" not in st.session_state:
        st.session_state["choice"] = "Login"

    # 2) Build the sidebar radio using the current choice
    choice = st.sidebar.radio(
        "Go to",
        ["Login", "Sign Up", "**Get Feedback**"],
        index=["Login", "Sign Up", "Main"].index(st.session_state["choice"])
    )
    # Update session state with the new sidebar selection
    st.session_state["choice"] = choice

    # 3) Route to the chosen page
    if choice == "Login":
        import my_pages._1_Login as _1_Login
        _1_Login.run()
    elif choice == "Sign Up":
        import my_pages._2_Signup as _2_Signup
        _2_Signup.run()
    elif choice == "**Get Feedback**":
        import my_pages._3_Main as _3_Main
        _3_Main.run()

if __name__ == "__main__":
    main()
