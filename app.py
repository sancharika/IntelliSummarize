import streamlit as st
import blogger
import gist
import pdfplumber
import ats
import docx

st.set_page_config(page_title='AI Blogger', page_icon='🤖', layout='centered')

st.title("Next Gen Of SUMMARIZATION")

uploaded_file = st.file_uploader("Choose a document file", type=["pdf", "txt", "csv", "docx"])
text = ''
if uploaded_file is not None:
    st.write("File uploaded successfully!")

    file_extension = uploaded_file.name.split(".")[-1]

    if file_extension == "pdf":
        with pdfplumber.open(uploaded_file) as pdf:
            pages = pdf.pages
            for page in pages:
                text = page.extract_text()

    elif file_extension == "txt":
        text = uploaded_file.getvalue().decode("utf-8")
    
    elif file_extension == "docx":
        docx_text = docx.Document(uploaded_file)
        full_text = []
        for para in docx_text.paragraphs:
            full_text.append(para.text)
        text = "\n".join(full_text)

st.text_area("Extracted From Document",value=text)
st.session_state['doc_text'] = text


gist.run_gist(st.session_state['doc_text'])
