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
    # Show the clickable logo at the top
    show_logo()

    st.title("Clinical Note Feedback")

    # Set OpenAI API key
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

    st.markdown("### Upload Your Files")
    file1 = st.file_uploader("Upload File 1 (**Clinical Note**)", type=["pdf", "docx", "txt"])
    file2 = st.file_uploader("Upload File 2 (**Patient Case File**)", type=["pdf", "docx", "txt"])
    file3 = st.file_uploader("Upload File 3 (**Interview Transcript**)", type=["pdf", "docx", "txt"])

    if st.button("Generate Feedback"):
        if not file1 or not file2 or not file3:
            st.error("Please upload all three files before generating feedback.")
        else:
            file1_text = extract_text_from_file(file1)
            file2_text = extract_text_from_file(file2)
            file3_text = extract_text_from_file(file3)

            # Example prompt that includes the file texts
            prompt = f"""
            You are assessing a year 1 medical student case write-up and their clinical reasoning and differential diagnosis. 
            Evaluate, and provide constructive 
            formative feedback on the clinical note, based on the history, physical exam, and test data 
            provided in the patient case file. Seperately, give feedback on the student's interview approach 
            in terms of flow, relevant questions asked based on the Chief Concern and differential diagnosis, thoroughness of the other 
            relevant portions of the history gathered, and display of verbal empathy. Be supportive yet 
            demand excellence.
            CLinical Note written by the student:
            \"\"\"
            {file1_text}
            \"\"\"
            Patient case file:
            \"\"\"
            {file2_text}
            \"\"\"
            Transcript of the student-patient clinical encounter:
            \"\"\"
            {file3_text}
            \"\"\"
            For each of the 3 categories in the clincial note (1. History, 2.Physical Examination and diagnostics, 3. Datra Interpretation), 
            list feedback as: a) Strengths, b) Areas for Improvement, c) Suggestions. Be very detailed in your feedback.
            For each critique you make in 'Areas for Improvement', explain why this is relevant to this patient's presentation.
            """
            with st.spinner("Studying the case. Reading your note. Thinking about what you wrote..."):
                response = openai.chat.completions.create(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": "You are an experienced medical educator preparing medical students for STEP 1 and clincial rotations."},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=1500,
                    temperature=0
                )

            feedback_text = response.choices[0].message.content
            st.session_state["feedback"] = feedback_text

            # Save in DB
            db.save_upload_and_feedback(user_id, file1_text, file2_text, file3_text, feedback_text)
            st.success("Feedback generated and saved!")

    if "feedback" in st.session_state:
        st.markdown("### Feedback")
        st.write(st.session_state["feedback"])

        if st.button("Download Feedback as PDF"):
            pdf_file_name = generate_feedback_pdf(st.session_state["feedback"])
            with open(pdf_file_name, "rb") as f:
                st.download_button(
                    label="Download PDF",
                    data=f,
                    file_name=pdf_file_name,
                    mime="application/pdf"
                )

    st.markdown("### Previous Feedback")
    previous_uploads = db.get_user_uploads(user_id)
    for upload in previous_uploads:
        with st.expander(f"Upload ID: {upload['upload_id']} (created at {upload['created_at']})"):
            st.subheader("Feedback:")
            st.write(upload["feedback"])

            st.subheader("Retrieve Uploaded Files as Text:")
            col1, col2, col3 = st.columns(3)

            with col1:
                st.download_button(
                    label="Download File 1 Text",
                    data=upload["file1_text"] or "",
                    file_name=f"file1_text_{upload['upload_id']}.txt",
                    mime="text/plain"
                )
            with col2:
                st.download_button(
                    label="Download File 2 Text",
                    data=upload["file2_text"] or "",
                    file_name=f"file2_text_{upload['upload_id']}.txt",
                    mime="text/plain"
                )
            with col3:
                st.download_button(
                    label="Download File 3 Text",
                    data=upload["file3_text"] or "",
                    file_name=f"file3_text_{upload['upload_id']}.txt",
                    mime="text/plain"
                )

def run():
    main_page()
