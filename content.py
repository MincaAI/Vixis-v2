import streamlit as st
from navbar import navbar
from helpers.fetchApi import *
from helpers.generateDocx import *

from io import BytesIO
from docx import Document

def interface():
    st.set_page_config(page_title="Financial Report Generator", layout="wide")
    navbar()

    # Initialize session state for outputs if not already set
    if "output1" not in st.session_state:
        st.session_state.output1 = ""
    if "output2" not in st.session_state:
        st.session_state.output2 = ""
    if "output3" not in st.session_state:
        st.session_state.output3 = ""

    col1, col2, col3 = st.columns([6,6,6])

    ### Column 1: Web Scraper
    with col1:
        st.subheader("Companies & Indices")
        prompt1 = st.text_area(
            "List of Companies & Indices",
            placeholder="NVIDIA, Apple Inc, Amazon, Microsoft, etc...",
            height=100,
            key="prompt1"
        )

        st.subheader("Agent Stock Options")
        agent1_placeholder = st.empty()
        output1_placeholder = st.empty()  # Placeholder for dynamic output
        output1_placeholder.write(st.session_state.output1)  # Persist output

        with agent1_placeholder:
            with st.status("Agent is ready ...", expanded=True) as status:
                if st.button("Run prompt", key="update1"):
                    if prompt1.strip():
                        st.session_state.output1 = fetch_data(
                            "https://mincaai-1.app.flowiseai.com/api/v1/prediction/b40044b1-c01e-4dc3-a60e-b4bf6c00dc96",
                            {"question": prompt1}
                        )
                        output1_placeholder.write(st.session_state.output1)
                        status.update(label="Download complete!", state="complete", expanded=False)
                    else:
                        st.warning("Please enter a valid company or index.")
                        status.update(label="Please enter a valid company or index.", state="error", expanded=False)

    ### Column 2: Stock Options
    with col2:
        st.subheader("Stocks")
        prompt2 = st.text_area(
            "Market analysis for tech stocks",
            placeholder="Enter list of stocks (i.e, AI, Tech, etc.)",
            height=100,
            key="prompt2"
        )

        st.subheader("Agent Webscraper")
        agent2_placeholder = st.empty()
        output2_placeholder = st.empty()
        output2_placeholder.write(st.session_state.output2)  # Persist output

        with agent2_placeholder:
            with st.status("Agent is ready ...", expanded=True) as status:
                if st.button("Run prompt", key="update2"):
                    if prompt2.strip():
                        st.session_state.output2 = fetch_data(
                            "https://mincaai.app.flowiseai.com/api/v1/prediction/def0efd9-158a-46a3-b334-5e061d6dc535",
                            {"question": prompt2}
                        )
                        output2_placeholder.write(st.session_state.output2)
                        status.update(label="Download complete!", state="complete", expanded=False)
                    else:
                        st.warning("Please enter a list of stocks.")
                        status.update(label="Please enter a list of stocks.", state="error", expanded=False)

    ### Column 3: Analysis Engine
    with col3:
        st.subheader("PDF File")
        uploaded_file = st.file_uploader("Upload PDF file", type=["pdf"], key="pdf_uploader")

        st.subheader("Agent PDF Analysis")
        agent3_placeholder = st.empty()
        output3_placeholder = st.empty()
        output3_placeholder.write(st.session_state.output3)  # Persist output

        with agent3_placeholder:
            with st.status("Agent is ready ...", expanded=True) as status:
                if st.button("🔍 Analyze PDF", key="update3"):
                    if uploaded_file:
                        files = {"files": (uploaded_file.name, uploaded_file, uploaded_file.type)}

                        # Flowise API for analysis
                        API_URL = "https://mincaai-1.app.flowiseai.com/api/v1/attachments/7d7fcbbd-d20f-4f06-a2cc-daefb9accd8c/bd13aae3-c806-46e0-8095-d48c9ccfea08"
                        fileContent = fetch_attachment_data(API_URL, files=files)

                        st.session_state.output3 = fetch_data(
                            "https://mincaai-1.app.flowiseai.com/api/v1/prediction/7d7fcbbd-d20f-4f06-a2cc-daefb9accd8c",
                            {"question": fileContent}
                        )

                        output3_placeholder.write(st.session_state.output3)
                        status.update(label="✅ Analysis complete!", state="complete", expanded=False)
                    else:
                        st.warning("⚠️ Please upload a PDF file.")
                        status.update(label="❌ Please upload a PDF file.", state="error", expanded=False)

    # Button to generate report, input is the 3 outputs, at least one must be non-empty, fetch another api to create new output
    
    st.subheader("📂 Agent Document Generator")
    download_btn_placeholder = st.empty()  
    genReport_placeholder = st.empty()
    outputFile_placeholder = st.empty()
    
    # Placeholder for download button

    
    if any([st.session_state.output1, st.session_state.output2, st.session_state.output3]):
        with genReport_placeholder:
            with st.status("Agent is ready ...", expanded=True) as status:
                if st.button("🔄 Generate Report"):   
                    API_URL = "https://mincaai-1.app.flowiseai.com/api/v1/prediction/131cac63-bc31-4ccb-9c9a-8304f78fe8ed"
                    reportContent = fetch_data(API_URL, {
                        "question": f"Stock prices: {st.session_state.output1}\nSectors: {st.session_state.output2}\nReport analysis: {st.session_state.output3}"
                    })

                    # Save report content in session state
                    st.session_state.generated_report = reportContent  

                    # Generate DOCX file
                    st.session_state.docx_file = generate_docx(reportContent)

                    status.update(label="✅ Report generated!", state="complete", expanded=False)

        # Ensure report and download button persist
        if "generated_report" in st.session_state and "docx_file" in st.session_state:
            with download_btn_placeholder:
                st.download_button(
                    label="📥 Download Report as DOCX",
                    data=st.session_state.docx_file,
                    file_name="report.docx",
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                )

            outputFile_placeholder.write(st.session_state.generated_report)

    else:
        st.error("Please validate at least one agent before generating the report.")

