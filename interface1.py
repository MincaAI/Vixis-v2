import streamlit as st
from navbar import navbar
from helpers.fetchApi import fetch_attachment_data, fetch_data
from helpers.generateDocx import generate_docx
from runAgent import run_agent
import json

# API URLs
API_ATTACHMENT = "https://cloud.flowiseai.com/api/v1/attachments/fecc2cff-f971-401e-8eeb-de68484888d1/b3828dd6-59a3-4fe2-a9ac-884c9a4f8746"
API_STOCK_ANALYSIS_1 = "https://cloud.flowiseai.com/api/v1/prediction/a3b63d2d-3f5f-4e40-97f7-e2d0f9f4c8e9"
API_STOCK_ANALYSIS_2 = "https://cloud.flowiseai.com/api/v1/prediction/5a92d92a-a6ea-4d88-bbe6-2c16f3d50e9f"
API_PDF_ANALYSIS = "https://cloud.flowiseai.com/api/v1/prediction/52416925-02e2-4139-9fc0-457dd97e79ee"
API_REPORT_GENERATION = "https://cloud.flowiseai.com/api/v1/prediction/f80e1f89-b069-4139-b93b-19042ec800a2"

def interface1():
    """Streamlit interface for generating financial reports."""

    # navbar()

    # Initialize session state
    for key in ["output4", "output5", "output6"]:
        if key not in st.session_state:
            st.session_state[key] = ""

    # User input for market analysis
    st.subheader("Entrez votre prompt")
    prompt = st.text_area("Analyse d'une entreprise", 
                          placeholder="Entrez le nom de l'entreprise\nEntrez le secteur de l'entreprise", 
                          height=100, key="prompt2")
    prompt_lines = [p.strip() for p in prompt.split("\n") if p.strip()]

    # File uploader
    uploaded_files = st.file_uploader("Télécharger des fichiers PDF", accept_multiple_files=True, type=["pdf"], key="pdf_uploader")
    files = [("files", (file.name, file, file.type)) for file in uploaded_files]
    file_content = fetch_attachment_data(API_ATTACHMENT, files=files) if uploaded_files else None
    print("file_content", file_content)

    # Stock Analysis Agents
    col1, col2, col3 = st.columns([5,3,3])


    if prompt_lines:
            run_agent(col1,"Agent Données Financières", prompt_lines[0], API_STOCK_ANALYSIS_1, "output4", "update1")


    if len(prompt_lines) > 0:
            run_agent(col2,"Agent Actualité", "\n".join(prompt_lines[:2]), API_STOCK_ANALYSIS_2, "output5", "update2")


    if file_content:
            run_agent(col3,"Agent Analyste", "\n".join(prompt_lines[:2]), API_PDF_ANALYSIS, "output6", "update3", uploads=file_content)

    
    # Ensure all outputs are available before generating the report
    if any([st.session_state.output4, st.session_state.output5, st.session_state.output6]):
    # if True:
        st.subheader("📂 Agent Note d’Analyse")

        # Placeholders
        download_btn_placeholder = st.empty()
        genReport_placeholder = st.empty()
        outputFile_placeholder = st.empty()

        with genReport_placeholder:
            with st.status("L’agent est prêt ...", expanded=True) as status:
                if st.button("🔄 Générez la note d’analyse"):
                    
                    report_query = {
                        "question": (
                            "Tu es un analyste financier senior chez VIXIS. Rédige une note d’analyse approfondie sur une seule entreprise, à destination d’investisseurs professionnels.\n\n"
                            "Voici les informations à ta disposition :\n\n"
                            f"📊 Données financières :\n{st.session_state.output4}\n\n"
                            f"📰 Actualité récente :\n{st.session_state.output5}\n\n"
                            f"📄 Synthèse externe (rapports PDF) :\n{st.session_state.output6}\n\n"
                            "Rédige un rapport professionnel en analysant activement ces informations, sans les résumer passivement. Structure-le en paragraphes clairs :\n"
                            
                            "Mentionne la date du jour, évite toute redondance et produis un contenu fluide, structuré, professionnel."
                        )
                    }# Fetch generated report
                    
                    st.session_state.generated_report_2 = fetch_data(API_REPORT_GENERATION, report_query)

                    # Generate a DOCX file
                    st.session_state.docx_file_2 = generate_docx(st.session_state.generated_report_2)

                    # Update status
                    status.update(label="✅ Report generated!", state="complete", expanded=False)
                    st.session_state.generated_report_2 = st.session_state.generated_report_2.replace("```markdown", "").replace("```", "")

        # Ensure report output and download button persist
        if "generated_report_2" in st.session_state and "docx_file_2" in st.session_state:
            with download_btn_placeholder:
                st.download_button(
                    "📥 Téléchargez la note d’analyse en DOCX",
                    data=st.session_state.docx_file_2,
                    file_name="report.docx",
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                )
            
            outputFile_placeholder.write(st.session_state.generated_report_2)  # Display generated report
