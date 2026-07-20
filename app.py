import streamlit as st 
from src.extract_text import extract_text_from_pdf, extract_text_from_docx
from src.skills import compare_skills, calculate_score, extract_skills, calculate_final_score
from src.semantic import calculate_semantic_similarity

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

if uploaded_resume is not None and job_description:
    matched_skills, missing_skills = compare_skills(resume_text, job_description)
    job_skills = extract_skills(job_description)

    skill_score = calculate_score(matched_skills, job_skills)
    semantic_score = calculate_semantic_similarity(resume_text, job_description)
    final_score = calculate_final_score(skill_score, semantic_score)

    st.header("Results")
    st.metric("Overall Match Score", str(final_score) + "%")

    st.subheader("Score breakdown")
    st.write("Skill match: " + str(skill_score) + "%")
    st.write("Semantic (meaning) match: " + str(round(semantic_score * 100)) + "%")

    st.subheader("Skills you have that match the job")
    st.write(matched_skills)

    st.subheader("Skills the job wants that are missing from your resume")
    st.write(missing_skills)