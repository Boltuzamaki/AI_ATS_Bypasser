from io import BytesIO

import streamlit as st

from app.src.docprocessor.document_transformer import add_hidden_text_to_pdf
from app.src.llm.llm_generator import process_llm_request

st.set_page_config(page_title="AI ATS Bypasser")


def main():
    st.title("AI ATS Bypasser")

    st.sidebar.title("Configuration")
    openai_api_key = st.sidebar.text_input("OpenAI API Key", type="password")
    model_choice = st.sidebar.selectbox(
        "Choose model", ["gpt-4o", "gpt-4o-mini"]
    )

    uploaded_file = st.file_uploader("Upload a PDF", type="pdf")
    job_description = st.text_area("Paste job description here")
    output_filename = st.text_input(
        "Enter output PDF filename (e.g., output.pdf)"
    )

    if st.button("Generate and Download PDF"):
        if (
            uploaded_file
            and openai_api_key
            and job_description
            and output_filename
        ):
            hidden_text = process_llm_request(
                job_description, openai_api_key, model_choice
            )
            uploaded_pdf = BytesIO(uploaded_file.read())
            output_pdf = add_hidden_text_to_pdf(
                uploaded_pdf,
                hidden_text,
            )
            st.download_button(
                label="Download Modified PDF",
                data=output_pdf,
                file_name=output_filename,
                mime="application/pdf",
            )
        else:
            st.error(
                (
                    "Please complete all fields: API Key, Job Description, "
                    "PDF upload, and Output filename."
                )
            )


if __name__ == "__main__":
    main()
