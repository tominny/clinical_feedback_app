# -*- coding: utf-8 -*-
"""
Created on Sat Jan 25 10:59:22 2025

@author: f006q7g
"""

# pdf_export.py

from fpdf import FPDF
import time

def generate_feedback_pdf(feedback_text, output_filename="feedback.pdf"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # Wrap text to multiple lines
    lines = feedback_text.split('\n')
    for line in lines:
        pdf.multi_cell(0, 10, line)
    
    pdf_file_name = f"{int(time.time())}_{output_filename}"
    pdf.output(pdf_file_name)
    return pdf_file_name
