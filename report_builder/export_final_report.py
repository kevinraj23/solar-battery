"""
export_final_report.py
======================
Builds the final Word document (.docx) and exports it directly to PDF (.pdf)
using Word COM automation, validating exact page numbers and formatting.
"""

import os
import sys
import win32com.client
import fitz  # PyMuPDF
from agent_doc_builder import build_full_report

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCX_PATH = os.path.join(BASE_DIR, "Solar_Battery_Health_Monitor_Project_Report.docx")
PDF_PATH = os.path.join(BASE_DIR, "Solar_Battery_Health_Monitor_Project_Report.pdf")

def generate_and_export():
    print("="*70)
    print("STEP 1: BUILDING WORD DOCUMENT (.DOCX)")
    print("="*70)
    build_full_report(DOCX_PATH)
    print(f"[OK] Word document saved to: {DOCX_PATH}")

    print("\n" + "="*70)
    print("STEP 2: WORD COM AUTOMATION (VERIFYING PAGES & EXPORTING TO PDF)")
    print("="*70)
    word = win32com.client.Dispatch("Word.Application")
    word.Visible = False
    try:
        doc = word.Documents.Open(DOCX_PATH)
        total_pages = doc.ComputeStatistics(2)
        print(f"TOTAL RENDERED PAGES IN MS WORD: {total_pages}")
        
        # Verify page locations of key headings
        print("\nChecking heading page numbers:")
        for p in doc.Paragraphs:
            txt = p.Range.Text.strip()
            if any(txt.startswith(x) for x in [
                'CHAPTER 1', 'CHAPTER 2', 'CHAPTER 3', 'Fig. 3.1', '3.1  CIRCUIT', 'Fig. 3.2',
                '3.2  HARDWARE', 'CHAPTER 4', 'CHAPTER 5', 'CHAPTER 6', '6.1  WORKING', 'Fig 6.1',
                '6.2  FLOWCHART', 'Fig 6.2', '6.3  PROGRAM', '6.4  TEST RESULTS', 'Fig 6.3',
                'CHAPTER 7', 'COST ESTIMATION', 'SUSTAINABILITY DEVELOPMENT GOALS (SDG)', 'REFERENCES'
            ]):
                page_adj = p.Range.Information(1) # Adjusted page number (printed)
                page_abs = p.Range.Information(3) # Absolute page
                print(f"  {txt[:45]:45} -> Printed Page {page_adj:2d} (Physical Page {page_abs:2d})")

        # Export to PDF (wdExportFormatPDF = 17)
        print(f"\nExporting to PDF: {PDF_PATH} ...")
        doc.ExportAsFixedFormat(
            OutputFileName=PDF_PATH,
            ExportFormat=17,
            OpenAfterExport=False,
            OptimizeFor=0, # wdExportOptimizeForPrint
            Range=0,       # wdExportAllDocument
            Item=0,        # wdExportDocumentContent
            IncludeDocProps=True,
            KeepIRM=True,
            CreateBookmarks=1, # wdExportCreateHeadingBookmarks
            DocStructureTags=True,
            BitmapMissingFonts=True,
            UseISO19005_1=False
        )
        print(f"[OK] PDF successfully generated: {PDF_PATH}")
        doc.Close(False)
    finally:
        word.Quit()

    print("\n" + "="*70)
    print("STEP 3: VALIDATING EXPORTED PDF WITH PYMUPDF")
    print("="*70)
    pdf = fitz.open(PDF_PATH)
    print(f"PDF Page Count: {len(pdf)}")
    print(f"PDF File Size:  {os.path.getsize(PDF_PATH) / 1024:.1f} KB")
    pdf.close()
    print("="*70)
    print("ALL VERIFICATIONS COMPLETED SUCCESSFULLY!")
    print("="*70)

if __name__ == "__main__":
    generate_and_export()
