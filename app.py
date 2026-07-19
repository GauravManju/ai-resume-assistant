import streamlit as st 

st.title("AI Resume & Interview Assistant")

st.write("Welcome! This app will help you match your resume to a job description.")

uploaded_resume = st.file_uploader("Upload your resume", type=["pdf", "docx"])

if uploaded_resume is not None:
    file_name = uploaded_resume.name

    if file_name.endswith(".pdf") or file_name.endswith(".docx"):
        st.success("File Received: " + file_name)
    else:
        st.error("Unsupported file type. Please upload a PDF or DOCX file.")
    
job_description = st.text_area("Paste the job description here")

if job_description:
    st.success("Job description received.")