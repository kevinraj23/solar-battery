"""
calibrate_report.py
===================
Tests building the document and checks the exact page count and page contents
using MS Word COM automation.
"""

import os
import win32com.client
from agent_doc_builder import build_full_report

DOCX_PATH = os.path.abspath(r"c:\Users\aravindhan\Desktop\crowd-source-faq\Solarbattery_moniter\Solar_Battery_Health_Monitor_Project_Report.docx")

def check_pages():
    build_full_report(DOCX_PATH)
    
    word = win32com.client.Dispatch("Word.Application")
    word.Visible = False
    try:
        doc = word.Documents.Open(DOCX_PATH)
        num_pages = doc.ComputeStatistics(2)
        print("\n" + "="*60)
        print(f"EXACT RENDERED WORD PAGE COUNT: {num_pages}")
        print("="*60)
        
        for i in range(1, num_pages + 1):
            rng_start = doc.GoTo(1, 1, i).Start
            rng_end = doc.GoTo(1, 1, i + 1).Start if i < num_pages else doc.Content.End
            rng = doc.Range(rng_start, rng_end)
            first_line = rng.Text.strip().split('\r')[0][:75]
            print(f"Page {i:2d}: {first_line}")
            
        doc.Close(False)
    finally:
        word.Quit()

if __name__ == "__main__":
    check_pages()
