import streamlit as st
import openai
from db.db_manager import DBManager
from utils.file_processing import extract_text_from_file
from utils.pdf_export import generate_feedback_pdf
import os

def main_page():
    st.title("Clinical Note Feedback")

    # Set the OpenAI API key from secrets
    openai.api_key = st.secrets["openai"]["api_key"]

    db = DBManager(
        host=st.secrets["database"]["host"],
        database=st.secrets["database"]["database"],
        user=st.secrets["database"]["user"],
        password=st.secrets["database"]["password"],
        port=st.secrets["database"]["port"]
    )

    # Check if user is logged in
    if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
        st.warning("Please log in first.")
        return

    user_id = st.session_state["user_id"]

    st.markdown("### Upload Your Files")
    file1 = st.file_uploader("Upload File 1 (**Clinical Note/Write-Up**)", type=["pdf", "docx", "txt"])
    file2 = st.file_uploader("Upload File 2 (**Patient Case File**)", type=["pdf", "docx", "txt"])
    file3 = st.file_uploader("Upload File 3 (**Interview Transcript**)", type=["pdf", "docx", "txt"])

    if st.button("Generate Feedback"):
        if not file1 or not file2 or not file3:
            st.error("Please upload all three files before generating feedback.")
        else:
            # Extract text from each file
            file1_text = extract_text_from_file(file1)
            file2_text = extract_text_from_file(file2)
            file3_text = extract_text_from_file(file3)

            # (CHANGED HERE) Construct the prompt, including the file contents
            prompt = f"""
You are teaching medical students in the preclerkship phase of the MD program. 
Your goal is to assess, evaluate, and provide constructive formative feedback on the clinical note,
based on the patient case file, and also give feedback on the student's interview approach.
Be supportive yet demand excellence.
Here is the student's clinical note (File 1):
\"\"\"
{file1_text}
\"\"\"

Here is the patient case file (File 2):
\"\"\"
{file2_text}
\"\"\"

Here is the interview transcript (File 3):
\"\"\"
{file3_text}
\"\"\"

For each of the 3 categories in the clincial note (History, Physical Examination and diagnostics, Datra Interpretation), list feedback as:
a) Strengths,
b) Areas for Improvement,
c) Suggestions.
Be very detailed in your feedback.

Then provide constructive feedback about how the interview was conducted and the info gathered.
Again, list:
a) Strengths,
b) Areas for Improvement,
c) Suggestions.
Be very detailed.
"""

            # Use the new openai>=1.0.0 method
            with st.spinner("Generating feedback..."):
                response = openai.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {
                            "role": "system",
                            "content": "You are an experienced medical educator and course director at a US medical school."
                        },
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=1500,
                    temperature=0
                )

            feedback_text = response.choices[0].message.content
            st.session_state["feedback"] = feedback_text

            # Save in the database
            db.save_upload_and_feedback(user_id, file1_text, file2_text, file3_text, feedback_text)
            st.success("Feedback generated and saved!")

    # Show feedback if it exists in session
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

    # Previous Feedback
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
