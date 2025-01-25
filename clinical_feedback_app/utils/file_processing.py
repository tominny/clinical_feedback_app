# -*- coding: utf-8 -*-
"""
Created on Sat Jan 25 10:59:06 2025

@author: f006q7g
"""

# file_processing.py

import docx2txt
import PyPDF2
import os

def extract_text_from_file(file):
    """
    file: a Streamlit file_uploader object or path
    Returns the extracted text as a string.
    """
    # Check the file name or MIME type
    file_name = file.name.lower()
    if file_name.endswith('.txt'):
        return file.read().decode('utf-8', errors='ignore')
    elif file_name.endswith('.docx'):
        # Streamlit file_uploader gives a file-like object
        # docx2txt requires a path or file-like, so we might do:
        with open(file.name, "wb") as temp_file:
            temp_file.write(file.getvalue())
        text = docx2txt.process(file.name)
        os.remove(file.name)  # cleanup
        return text
    elif file_name.endswith('.pdf'):
        pdf_reader = PyPDF2.PdfReader(file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
        return text
    else:
        return ""  # or raise an Exception for unsupported format
