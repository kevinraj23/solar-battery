"""
agent_doc_builder.py
====================
Master Orchestrator Agent that synthesizes content, layout, tables, component images,
and diagram placeholders to generate the complete Word Document (.docx) report.
"""

import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

# Import specialized sub-agents
from agent_layout_styler import (
    configure_document_styles,
    add_body_section,
    add_chapter_header,
    add_unnum_title,
    add_heading_1,
    add_heading_2,
    add_paragraph,
    add_bullet_point,
    add_caption,
    FONT_NAME,
    BODY_FONT_SIZE,
    CHAPTER_FONT_SIZE,
    HEADING_FONT_SIZE
)
from agent_figure_formatter import (
    add_component_image,
    add_image_placeholder
)
from agent_table_builder import (
    build_toc_table_page1,
    build_toc_table_page2,
    build_list_of_figures_table,
    build_test_table_1,
    build_test_table_2,
    build_test_table_3,
    build_cost_estimation_table
)
from agent_program_formatter import add_program_listing
import agent_content_drafter as content

def build_full_report(output_path):
    print("[DOC_BUILDER] Initializing python-docx document...")
    doc = docx.Document()
    
    # -------------------------------------------------------------
    # 1. CONFIGURE SECTION 1: PRELIMINARY PAGES (ROMAN v, vi, vii, viii)
    # -------------------------------------------------------------
    configure_document_styles(doc)

    images_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "images")

    # =============================================================
    # PAGE v: ABSTRACT
    # =============================================================
    print("[DOC_BUILDER] Building Page v: ABSTRACT...")
    add_unnum_title(doc, "ABSTRACT")
    add_paragraph(doc, content.ABSTRACT_P1)
    add_paragraph(doc, content.ABSTRACT_P2)
    add_paragraph(doc, content.ABSTRACT_P3)
    add_paragraph(doc, content.ABSTRACT_P4)
    doc.add_page_break()

    # =============================================================
    # PAGE vi: TABLE OF CONTENTS (Part 1)
    # =============================================================
    print("[DOC_BUILDER] Building Page vi: TABLE OF CONTENTS (Part 1)...")
    add_unnum_title(doc, "TABLE OF CONTENTS")
    build_toc_table_page1(doc)
    doc.add_page_break()

    # =============================================================
    # PAGE vii: TABLE OF CONTENTS (Part 2)
    # =============================================================
    print("[DOC_BUILDER] Building Page vii: TABLE OF CONTENTS (Part 2)...")
    add_unnum_title(doc, "TABLE OF CONTENTS (CONTINUED)")
    build_toc_table_page2(doc)
    doc.add_page_break()

    # =============================================================
    # PAGE viii: LIST OF FIGURES
    # =============================================================
    print("[DOC_BUILDER] Building Page viii: LIST OF FIGURES...")
    add_unnum_title(doc, "LIST OF FIGURES")
    build_list_of_figures_table(doc)

    # -------------------------------------------------------------
    # 2. CONFIGURE SECTION 2: ARABIC NUMERALS (Starts at Page 1)
    # -------------------------------------------------------------
    add_body_section(doc)

    # =============================================================
    # PAGE 1: LIST OF ABBREVIATIONS
    # =============================================================
    print("[DOC_BUILDER] Building Page 1: LIST OF ABBREVIATIONS...")
    add_unnum_title(doc, "LIST OF ABBREVIATIONS")
    for abbr, full_form in content.LIST_OF_ABBREVIATIONS:
        p_abbr = doc.add_paragraph()
        p_abbr.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p_abbr.paragraph_format.line_spacing = 1.2
        p_abbr.paragraph_format.space_after = Pt(2)
        p_abbr.paragraph_format.space_before = Pt(1)
        r_bullet = p_abbr.add_run("•  ")
        r_bullet.font.name = FONT_NAME
        r_bullet.font.size = BODY_FONT_SIZE
        r_abbr = p_abbr.add_run(f"{abbr:8} –  ")
        r_abbr.font.name = FONT_NAME
        r_abbr.font.size = BODY_FONT_SIZE
        r_abbr.font.bold = True
        r_full = p_abbr.add_run(full_form)
        r_full.font.name = FONT_NAME
        r_full.font.size = BODY_FONT_SIZE
    doc.add_page_break()

    # =============================================================
    # PAGE 2: CHAPTER 1 INTRODUCTION (1.1 GENERAL, 1.2 OBJECTIVES lead)
    # =============================================================
    print("[DOC_BUILDER] Building Page 2: CHAPTER 1 INTRODUCTION...")
    add_chapter_header(doc, "1", "INTRODUCTION")
    add_heading_1(doc, "1.1", "GENERAL")
    add_paragraph(doc, content.CH1_1_GENERAL_P1)
    add_paragraph(doc, content.CH1_1_GENERAL_P2)
    add_heading_1(doc, "1.2", "OBJECTIVES")
    add_paragraph(doc, content.CH1_2_OBJECTIVES_LEAD)
    doc.add_page_break()

    # =============================================================
    # PAGE 3: 1.2 OBJECTIVES (cont.), 1.3 PROBLEM STATEMENT
    # =============================================================
    print("[DOC_BUILDER] Building Page 3: 1.2 OBJECTIVES (cont.), 1.3 PROBLEM STATEMENT...")
    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p_sub.paragraph_format.space_before = Pt(2)
    p_sub.paragraph_format.space_after = Pt(4)
    r_sub = p_sub.add_run("The specific technical objectives of the project are:")
    r_sub.font.name = FONT_NAME
    r_sub.font.size = BODY_FONT_SIZE
    r_sub.font.bold = True

    for text_val in content.CH1_2_OBJECTIVES_BULLETS:
        add_bullet_point(doc, text_val)

    add_heading_1(doc, "1.3", "PROBLEM STATEMENT")
    add_paragraph(doc, content.CH1_3_PROBLEM_STATEMENT_P1)
    for text_val in content.CH1_3_PROBLEM_BULLETS_P3:
        add_bullet_point(doc, text_val)
    doc.add_page_break()

    # =============================================================
    # PAGE 4: 1.4 DISADVANTAGES OF EXISTING SYSTEM, 1.5 PROPOSED SYSTEM (p1)
    # =============================================================
    print("[DOC_BUILDER] Building Page 4: 1.4 DISADVANTAGES OF EXISTING SYSTEM, 1.5 PROPOSED SYSTEM...")
    add_bullet_point(doc, content.CH1_3_PROBLEM_BULLET_P4)
    
    p_trans = doc.add_paragraph()
    p_trans.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_trans.paragraph_format.line_spacing = 1.5
    p_trans.paragraph_format.space_before = Pt(2)
    p_trans.paragraph_format.space_after = Pt(4)
    r_trans = p_trans.add_run("Therefore, a smart system is required to monitor battery storage, predict runtime using machine learning, detect solar panel soiling, and support remote monitoring through IoT technology.")
    r_trans.font.name = FONT_NAME
    r_trans.font.size = BODY_FONT_SIZE

    add_heading_1(doc, "1.4", "DISADVANTAGES OF EXISTING SYSTEM")
    p_dis = doc.add_paragraph()
    p_dis.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_dis.paragraph_format.line_spacing = 1.5
    p_dis.paragraph_format.space_after = Pt(4)
    r_dis = p_dis.add_run("The existing solar battery monitoring systems have the following disadvantages:")
    r_dis.font.name = FONT_NAME
    r_dis.font.size = BODY_FONT_SIZE

    for text_val in content.CH1_4_DISADVANTAGES_BULLETS:
        add_bullet_point(doc, text_val)

    add_heading_1(doc, "1.5", "PROPOSED SYSTEM")
    add_paragraph(doc, content.CH1_5_PROPOSED_SYSTEM_P1)
    doc.add_page_break()

    # =============================================================
    # PAGE 5: 1.5 PROPOSED SYSTEM (cont.)
    # =============================================================
    print("[DOC_BUILDER] Building Page 5: 1.5 PROPOSED SYSTEM (cont.)...")
    add_paragraph(doc, content.CH1_5_PROPOSED_SYSTEM_P2)
    add_paragraph(doc, content.CH1_5_PROPOSED_SYSTEM_P3)
    add_paragraph(doc, content.CH1_5_PROPOSED_SYSTEM_P4)
    doc.add_page_break()

    # =============================================================
    # PAGE 6: CHAPTER 2 LITERATURE SURVEY (2.1, 2.2)
    # =============================================================
    print("[DOC_BUILDER] Building Page 6: CHAPTER 2 LITERATURE SURVEY (2.1, 2.2)...")
    add_chapter_header(doc, "2", "LITERATURE SURVEY")
    
    # 2.1
    p_sec1 = doc.add_paragraph()
    p_sec1.paragraph_format.space_before = Pt(10)
    p_sec1.paragraph_format.space_after = Pt(4)
    r_sec1 = p_sec1.add_run("2.1. Home Automation-Based Environmental Alert System (Matthias Mielke and Rainer Bruck, 2016)")
    r_sec1.font.name = FONT_NAME
    r_sec1.font.size = HEADING_FONT_SIZE
    r_sec1.font.bold = True
    add_paragraph(doc, content.CH2_1_TEXT)

    # 2.2
    p_sec2 = doc.add_paragraph()
    p_sec2.paragraph_format.space_before = Pt(10)
    p_sec2.paragraph_format.space_after = Pt(4)
    r_sec2 = p_sec2.add_run("2.2. Dynamic Lighting and Augmented Reality Smart Home System (Abhirup Bose et al., 2020)")
    r_sec2.font.name = FONT_NAME
    r_sec2.font.size = HEADING_FONT_SIZE
    r_sec2.font.bold = True
    add_paragraph(doc, content.CH2_2_TEXT)
    doc.add_page_break()

    # =============================================================
    # PAGE 7: 2.3, 2.4
    # =============================================================
    print("[DOC_BUILDER] Building Page 7: 2.3, 2.4...")
    # 2.3
    p_sec3 = doc.add_paragraph()
    p_sec3.paragraph_format.space_before = Pt(8)
    p_sec3.paragraph_format.space_after = Pt(4)
    r_sec3 = p_sec3.add_run("2.3. Smart Emergency Safety Alert System (Daniel Kiguwa, 2023)")
    r_sec3.font.name = FONT_NAME
    r_sec3.font.size = HEADING_FONT_SIZE
    r_sec3.font.bold = True
    add_paragraph(doc, content.CH2_3_TEXT)

    # 2.4
    p_sec4 = doc.add_paragraph()
    p_sec4.paragraph_format.space_before = Pt(10)
    p_sec4.paragraph_format.space_after = Pt(4)
    r_sec4 = p_sec4.add_run("2.4. Internet of Things-Based Gas and Environmental Monitoring (M. Adamu Islam Mashuri et al., 2025)")
    r_sec4.font.name = FONT_NAME
    r_sec4.font.size = HEADING_FONT_SIZE
    r_sec4.font.bold = True
    add_paragraph(doc, content.CH2_4_TEXT)
    doc.add_page_break()

    # =============================================================
    # PAGE 8: 2.5
    # =============================================================
    print("[DOC_BUILDER] Building Page 8: 2.5...")
    p_sec5 = doc.add_paragraph()
    p_sec5.paragraph_format.space_before = Pt(8)
    p_sec5.paragraph_format.space_after = Pt(4)
    r_sec5 = p_sec5.add_run("2.5. Inclusive Emergency Alerts Using Visual and Cloud Notifications (Utkarsha Kshirsagar et al., 2025)")
    r_sec5.font.name = FONT_NAME
    r_sec5.font.size = HEADING_FONT_SIZE
    r_sec5.font.bold = True
    add_paragraph(doc, content.CH2_5_TEXT)
    add_paragraph(doc, content.CH2_SUMMARY_TEXT)
    doc.add_page_break()

    # =============================================================
    # PAGE 9: CHAPTER 3 SYSTEM CONSIDERATION (Overview p1)
    # =============================================================
    print("[DOC_BUILDER] Building Page 9: CHAPTER 3 SYSTEM CONSIDERATION (p1)...")
    add_chapter_header(doc, "3", "SYSTEM CONSIDERATION")
    add_paragraph(doc, content.CH3_P1)
    add_paragraph(doc, content.CH3_P2)
    doc.add_page_break()

    # =============================================================
    # PAGE 10: SYSTEM CONSIDERATION (Overview p2)
    # =============================================================
    print("[DOC_BUILDER] Building Page 10: SYSTEM CONSIDERATION (p2)...")
    add_paragraph(doc, content.CH3_P3)
    add_paragraph(doc, content.CH3_P4)
    doc.add_page_break()

    # =============================================================
    # PAGE 11: SYSTEM CONSIDERATION & Fig. 3.1 Block Diagram
    # =============================================================
    print("[DOC_BUILDER] Building Page 11: Fig. 3.1 Block Diagram of Proposed Method...")
    add_paragraph(doc, content.CH3_P5)
    
    # Actual Fig 3.1 Block Diagram
    img_block = os.path.join(images_dir, "fig_3_1_block_diagram.jpg")
    add_component_image(doc, img_block, "Fig. 3.1 Block diagram of Proposed Method", width_inches=5.2)
    doc.add_page_break()

    # =============================================================
    # PAGE 12: 3.1 CIRCUIT DIAGRAM (Circuit Interconnection p1)
    # =============================================================
    print("[DOC_BUILDER] Building Page 12: 3.1 CIRCUIT DIAGRAM (p1)...")
    add_heading_1(doc, "3.1", "CIRCUIT DIAGRAM")
    add_paragraph(doc, content.CH3_CIRCUIT_P1)
    add_paragraph(doc, content.CH3_CIRCUIT_P2)
    add_paragraph(doc, content.CH3_CIRCUIT_P3)
    doc.add_page_break()

    # =============================================================
    # PAGE 13: 3.1 CIRCUIT DIAGRAM (cont.) & Fig. 3.2 Circuit Diagram
    # =============================================================
    print("[DOC_BUILDER] Building Page 13: Fig. 3.2 Circuit Diagram of Proposed method...")
    add_paragraph(doc, content.CH3_CIRCUIT_P4)
    
    # Actual Fig 3.2 Circuit Diagram
    img_circuit = os.path.join(images_dir, "fig_3_2_circuit_diagram.jpg")
    add_component_image(doc, img_circuit, "Fig. 3.2 Circuit Diagram of Proposed method", width_inches=5.2)
    doc.add_page_break()

    # =============================================================
    # PAGE 14: 3.2 HARDWARE SPECIFICATIONS, 3.2.1 Arduino Nano & Fig. 3.3
    # =============================================================
    print("[DOC_BUILDER] Building Page 14: 3.2.1 Arduino Nano Microcontroller & Fig 3.3...")
    add_heading_1(doc, "3.2", "HARDWARE SPECIFICATIONS")
    add_heading_2(doc, "3.2.1", "Arduino Nano Microcontroller")
    add_paragraph(doc, content.CH3_2_1_TEXT)

    img_nano = os.path.join(images_dir, "fig_3_3_arduino_nano.jpg")
    add_component_image(doc, img_nano, "Fig. 3.3 Arduino Nano Microcontroller", width_inches=2.2)
    doc.add_page_break()

    # =============================================================
    # PAGE 15: 3.2.2 Solar Photovoltaic Panel & Fig. 3.4
    # =============================================================
    print("[DOC_BUILDER] Building Page 15: 3.2.2 Solar Photovoltaic Panel & Fig 3.4...")
    add_heading_2(doc, "3.2.2", "Solar Photovoltaic Panel")
    add_paragraph(doc, content.CH3_2_2_TEXT)

    img_solar = os.path.join(images_dir, "fig_3_4_solar_panel.jpg")
    add_component_image(doc, img_solar, "Fig. 3.4 Solar Photovoltaic Panel", width_inches=2.2)
    doc.add_page_break()

    # =============================================================
    # PAGE 16: 3.2.3 18650 Battery Cell & Fig. 3.5, 3.2.4 ACS712 Sensor & Fig. 3.6
    # =============================================================
    print("[DOC_BUILDER] Building Page 16: 3.2.3 Battery Cell & 3.2.4 ACS712 Sensor...")
    add_heading_2(doc, "3.2.3", "18650 Lithium-ion Battery Cell")
    add_paragraph(doc, content.CH3_2_3_TEXT)

    img_bat = os.path.join(images_dir, "fig_3_5_battery_cell.jpg")
    add_component_image(doc, img_bat, "Fig. 3.5 18650 Lithium-ion Battery Cell", width_inches=1.8)

    add_heading_2(doc, "3.2.4", "ACS712 Current Sensor Module")
    add_paragraph(doc, content.CH3_2_4_TEXT)

    img_cur = os.path.join(images_dir, "fig_3_6_current_sensor.jpg")
    add_component_image(doc, img_cur, "Fig. 3.6 ACS712 Current Sensor Module", width_inches=1.8)
    doc.add_page_break()

    # =============================================================
    # PAGE 17: 3.2.5 LM35 Sensor & Fig. 3.7, 3.2.6 Edge Gateway & Fig. 3.8
    # =============================================================
    print("[DOC_BUILDER] Building Page 17: 3.2.5 LM35 Sensor & 3.2.6 Edge Gateway...")
    add_heading_2(doc, "3.2.5", "LM35 Precision Temperature Sensor")
    add_paragraph(doc, content.CH3_2_5_TEXT)

    img_temp = os.path.join(images_dir, "fig_3_7_temp_sensor.jpg")
    add_component_image(doc, img_temp, "Fig. 3.7 LM35 Precision Temperature Sensor", width_inches=1.6)

    add_heading_2(doc, "3.2.6", "IoT Edge Gateway and Cloud Communication")
    add_paragraph(doc, content.CH3_2_6_TEXT)

    img_gw = os.path.join(images_dir, "fig_3_8_iot_gateway.jpg")
    add_component_image(doc, img_gw, "Fig. 3.8 IoT Edge Gateway and Cloud Communication", width_inches=2.0)
    doc.add_page_break()

    # =============================================================
    # PAGE 18: CHAPTER 4 METHODOLOGY (4.1 EXISTING METHODOLOGY)
    # =============================================================
    print("[DOC_BUILDER] Building Page 18: CHAPTER 4 METHODOLOGY (4.1)...")
    add_chapter_header(doc, "4", "METHODOLOGY")
    add_heading_1(doc, "4.1", "EXISTING METHODOLOGY")
    add_paragraph(doc, content.CH4_1_TEXT_P1)
    add_paragraph(doc, content.CH4_1_TEXT_P2)
    add_paragraph(doc, content.CH4_1_TEXT_P3)
    doc.add_page_break()

    # =============================================================
    # PAGE 19: 4.2 PROPOSED METHODOLOGY (Stages 1 to 4)
    # =============================================================
    print("[DOC_BUILDER] Building Page 19: 4.2 PROPOSED METHODOLOGY (Stages 1 to 4)...")
    add_heading_1(doc, "4.2", "PROPOSED METHODOLOGY")
    add_paragraph(doc, content.CH4_2_LEAD)
    add_bullet_point(doc, content.CH4_2_STAGE_1[1], bold_prefix=content.CH4_2_STAGE_1[0])
    add_bullet_point(doc, content.CH4_2_STAGE_2[1], bold_prefix=content.CH4_2_STAGE_2[0])
    add_bullet_point(doc, content.CH4_2_STAGE_3[1], bold_prefix=content.CH4_2_STAGE_3[0])
    add_bullet_point(doc, content.CH4_2_STAGE_4[1], bold_prefix=content.CH4_2_STAGE_4[0])
    doc.add_page_break()

    # =============================================================
    # PAGE 20: 4.2 PROPOSED METHODOLOGY (Stages 5 to 7), 4.3 ADVANTAGES
    # =============================================================
    print("[DOC_BUILDER] Building Page 20: 4.2 PROPOSED METHODOLOGY (Stages 5 to 7), 4.3 ADVANTAGES...")
    add_bullet_point(doc, content.CH4_2_STAGE_5[1], bold_prefix=content.CH4_2_STAGE_5[0])
    add_bullet_point(doc, content.CH4_2_STAGE_6[1], bold_prefix=content.CH4_2_STAGE_6[0])
    add_bullet_point(doc, content.CH4_2_STAGE_7[1], bold_prefix=content.CH4_2_STAGE_7[0])

    add_heading_1(doc, "4.3", "ADVANTAGES")
    p_adv = doc.add_paragraph()
    p_adv.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_adv.paragraph_format.line_spacing = 1.5
    p_adv.paragraph_format.space_after = Pt(4)
    r_adv = p_adv.add_run("The proposed Smart Solar Battery Health Monitor delivers distinct technical advantages:")
    r_adv.font.name = FONT_NAME
    r_adv.font.size = BODY_FONT_SIZE

    for bold_pre, text_val in content.CH4_3_ADVANTAGES_BULLETS:
        add_bullet_point(doc, text_val, bold_prefix=bold_pre)
    doc.add_page_break()

    # =============================================================
    # PAGE 21: 4.4 DISADVANTAGES, 4.5 APPLICATIONS
    # =============================================================
    print("[DOC_BUILDER] Building Page 21: 4.4 DISADVANTAGES, 4.5 APPLICATIONS...")
    add_heading_1(doc, "4.4", "DISADVANTAGES")
    p_dis2 = doc.add_paragraph()
    p_dis2.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_dis2.paragraph_format.line_spacing = 1.5
    p_dis2.paragraph_format.space_after = Pt(4)
    r_dis2 = p_dis2.add_run("The system considers the following practical constraints and engineering trade-offs:")
    r_dis2.font.name = FONT_NAME
    r_dis2.font.size = BODY_FONT_SIZE

    for bold_pre, text_val in content.CH4_4_DISADVANTAGES_BULLETS:
        add_bullet_point(doc, text_val, bold_prefix=bold_pre)

    add_heading_1(doc, "4.5", "APPLICATIONS")
    p_app = doc.add_paragraph()
    p_app.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_app.paragraph_format.line_spacing = 1.5
    p_app.paragraph_format.space_after = Pt(4)
    r_app = p_app.add_run("The developed cyber-physical monitor is directly applicable across a wide range of real-world energy domains:")
    r_app.font.name = FONT_NAME
    r_app.font.size = BODY_FONT_SIZE

    for bold_pre, text_val in content.CH4_5_APPLICATIONS_BULLETS:
        add_bullet_point(doc, text_val, bold_prefix=bold_pre)
    doc.add_page_break()

    # =============================================================
    # PAGE 22: CHAPTER 5 SOFTWARE IMPLEMENTATION
    # =============================================================
    print("[DOC_BUILDER] Building Page 22: CHAPTER 5 SOFTWARE IMPLEMENTATION...")
    add_chapter_header(doc, "5", "SOFTWARE IMPLEMENTATION")
    for title_line, body_line in content.CH5_SECTIONS:
        p_hdr = doc.add_paragraph()
        p_hdr.paragraph_format.space_before = Pt(8)
        p_hdr.paragraph_format.space_after = Pt(2)
        r_hdr = p_hdr.add_run(title_line)
        r_hdr.font.name = FONT_NAME
        r_hdr.font.size = HEADING_FONT_SIZE
        r_hdr.font.bold = True
        
        add_paragraph(doc, body_line)
    doc.add_page_break()

    # =============================================================
    # PAGE 23: CHAPTER 6 WORKING AND PROGRAM, 6.1 WORKING & Fig 6.1
    # =============================================================
    print("[DOC_BUILDER] Building Page 23: CHAPTER 6 WORKING & Fig 6.1 Hardware Kit...")
    add_chapter_header(doc, "6", "WORKING AND PROGRAM")
    add_heading_1(doc, "6.1", "WORKING")
    add_paragraph(doc, content.CH6_WORKING_TEXT)

    # Actual Fig 6.1 Hardware Kit
    img_hw = os.path.join(images_dir, "fig_6_1_hardware_kit.jpg")
    add_component_image(doc, img_hw, "Fig 6.1 Hardware Kit", width_inches=4.8)
    doc.add_page_break()

    # =============================================================
    # PAGE 24: 6.2 FLOWCHART & Fig 6.2
    # =============================================================
    print("[DOC_BUILDER] Building Page 24: 6.2 FLOWCHART & Fig 6.2 Flowchart...")
    add_heading_1(doc, "6.2", "FLOWCHART")
    add_paragraph(doc, content.CH6_FLOWCHART_TEXT)

    # Actual Fig 6.2 Flowchart
    img_flow = os.path.join(images_dir, "fig_6_2_flowchart.jpg")
    add_component_image(doc, img_flow, "Fig 6.2 Flowchart", width_inches=3.8)
    doc.add_page_break()

    # =============================================================
    # PAGE 25: 6.3 PROGRAM (ARDUINO CODE ON 1 PAGE)
    # =============================================================
    print("[DOC_BUILDER] Building Section 6.3: PROGRAM (Full-width, multi-page Arduino C/C++ firmware)...")
    add_heading_1(doc, "6.3", "PROGRAM")
    add_program_listing(doc)
    doc.add_page_break()

    # =============================================================
    # PAGE 26: 6.4 TEST RESULTS (Working Model Photo, Table 1, Table 2)
    # =============================================================
    print("[DOC_BUILDER] Building Section 6.4: TEST RESULTS (Photo of Working Model & Test Tables)...")
    add_heading_1(doc, "6.4", "TEST RESULTS")
    add_paragraph(doc, content.CH6_TEST_RESULTS_LEAD)

    # Actual Fig 6.3 Photo of Working Model
    img_model = os.path.join(images_dir, "fig_6_3_working_model.jpg")
    add_component_image(doc, img_model, "Fig 6.3 Photo of working model", width_inches=2.8)
    doc.add_page_break()

    build_test_table_1(doc)
    build_test_table_2(doc)
    doc.add_page_break()

    # =============================================================
    # PAGE 27: 6.4 TEST RESULTS (cont. Table 3 & Narrative)
    # =============================================================
    print("[DOC_BUILDER] Building Page 27: Table 3 Edge ML Prognostics & Telegram Messaging...")
    build_test_table_3(doc)
    add_paragraph(doc, content.CH6_TEST_RESULTS_DISC_P1)
    add_paragraph(doc, content.CH6_TEST_RESULTS_DISC_P2)
    doc.add_page_break()

    # =============================================================
    # PAGE 28: CHAPTER 7 CONCLUSION AND FUTURE WORK
    # =============================================================
    print("[DOC_BUILDER] Building Page 28: CHAPTER 7 CONCLUSION AND FUTURE WORK...")
    add_chapter_header(doc, "7", "CONCLUSION AND FUTURE WORK")
    add_heading_1(doc, "7.1", "CONCLUSION")
    add_paragraph(doc, content.CH7_CONCLUSION_TEXT)

    add_heading_1(doc, "7.2", "FUTURE SCOPE")
    for text_val in content.CH7_FUTURE_SCOPE_BULLETS:
        add_bullet_point(doc, text_val)
    doc.add_page_break()

    # =============================================================
    # PAGE 29: COST ESTIMATION
    # =============================================================
    print("[DOC_BUILDER] Building Page 29: COST ESTIMATION...")
    add_unnum_title(doc, "COST ESTIMATION")
    add_paragraph(doc, content.COST_ESTIMATION_LEAD)
    build_cost_estimation_table(doc)
    add_paragraph(doc, content.COST_ESTIMATION_SUMMARY)
    doc.add_page_break()

    # =============================================================
    # PAGE 30: SUSTAINABILITY DEVELOPMENT GOALS (Part 1)
    # =============================================================
    print("[DOC_BUILDER] Building Page 30: SUSTAINABILITY DEVELOPMENT GOALS (p1)...")
    add_unnum_title(doc, "SUSTAINABILITY DEVELOPMENT GOALS (SDG)")

    # Insert SDG Graphic Banner
    sdg_img = os.path.join(images_dir, "sdg_banner.png")
    if os.path.exists(sdg_img):
        p_sdg = doc.add_paragraph()
        p_sdg.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_sdg.paragraph_format.space_before = Pt(2)
        p_sdg.paragraph_format.space_after = Pt(6)
        r_sdg = p_sdg.add_run()
        r_sdg.add_picture(sdg_img, width=Inches(5.2))

    # SDG 7
    p_h7 = doc.add_paragraph()
    p_h7.paragraph_format.space_before = Pt(8)
    p_h7.paragraph_format.space_after = Pt(2)
    r_h7 = p_h7.add_run(content.SDG_7_TITLE)
    r_h7.font.name = FONT_NAME
    r_h7.font.size = HEADING_FONT_SIZE
    r_h7.font.bold = True
    add_paragraph(doc, content.SDG_7_BODY)

    # SDG 9
    p_h9 = doc.add_paragraph()
    p_h9.paragraph_format.space_before = Pt(8)
    p_h9.paragraph_format.space_after = Pt(2)
    r_h9 = p_h9.add_run(content.SDG_9_TITLE)
    r_h9.font.name = FONT_NAME
    r_h9.font.size = HEADING_FONT_SIZE
    r_h9.font.bold = True
    add_paragraph(doc, content.SDG_9_BODY)
    doc.add_page_break()

    # =============================================================
    # PAGE 31: SUSTAINABILITY DEVELOPMENT GOALS (Part 2)
    # =============================================================
    print("[DOC_BUILDER] Building Page 31: SUSTAINABILITY DEVELOPMENT GOALS (p2)...")
    # SDG 12
    p_h12 = doc.add_paragraph()
    p_h12.paragraph_format.space_before = Pt(8)
    p_h12.paragraph_format.space_after = Pt(2)
    r_h12 = p_h12.add_run(content.SDG_12_TITLE)
    r_h12.font.name = FONT_NAME
    r_h12.font.size = HEADING_FONT_SIZE
    r_h12.font.bold = True
    add_paragraph(doc, content.SDG_12_BODY)

    # SDG 13
    p_h13 = doc.add_paragraph()
    p_h13.paragraph_format.space_before = Pt(8)
    p_h13.paragraph_format.space_after = Pt(2)
    r_h13 = p_h13.add_run(content.SDG_13_TITLE)
    r_h13.font.name = FONT_NAME
    r_h13.font.size = HEADING_FONT_SIZE
    r_h13.font.bold = True
    add_paragraph(doc, content.SDG_13_BODY)

    add_paragraph(doc, content.SDG_SUMMARY)
    doc.add_page_break()

    # =============================================================
    # PAGE 32: REFERENCES
    # =============================================================
    print("[DOC_BUILDER] Building Page 32: REFERENCES...")
    add_unnum_title(doc, "REFERENCES")
    for ref_entry in content.REFERENCES:
        p_ref = doc.add_paragraph()
        p_ref.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p_ref.paragraph_format.line_spacing = 1.3
        p_ref.paragraph_format.space_after = Pt(6)
        p_ref.paragraph_format.space_before = Pt(2)
        r_ref = p_ref.add_run(ref_entry)
        r_ref.font.name = FONT_NAME
        r_ref.font.size = Pt(11)

    # Save document
    print(f"[DOC_BUILDER] Saving completed report to {output_path}...")
    doc.save(output_path)
    print(f"[DOC_BUILDER] SUCCESS: Report saved to {output_path}!")

if __name__ == "__main__":
    out_file = r"c:\Users\aravindhan\Desktop\crowd-source-faq\Solarbattery_moniter\Solar_Battery_Health_Monitor_Project_Report.docx"
    build_full_report(out_file)
