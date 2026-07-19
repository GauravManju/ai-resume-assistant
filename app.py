import streamlit as st 
from src.extract_text import extract_text_from_pdf, extract_text_from_docx

st.title("AI Resume & Interview Assistant")

st.write("Welcome! This app will help you match your resume to a job description.")

uploaded_resume = st.file_uploader("Upload your resume", type=["pdf", "docx"])

if uploaded_resume is not None:
    file_name = uploaded_resume.name

    if file_name.endswith(".pdf"):
        resume_text = extract_text_from_pdf(uploaded_resume)
        st.success("Resume text extracted successfully!")
        st.text_area("Extracted resume text", resume_text, height=300)

    elif file_name.endswith(".docx"):
        resume_text = extract_text_from_docx(uploaded_resume)
        st.success("Resume text extracted successfully!")
        st.text_area("Extracted resume text", resume_text, height=300)

    else:
        st.error("Unsupported file type. Please upload a PDF or DOCX file.")
    
job_description = st.text_area("Paste the job description here")

if job_description:
    st.success("Job description received.")