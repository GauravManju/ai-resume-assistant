import streamlit as st
from src.extract_text import extract_text_from_pdf, extract_text_from_docx
from src.skills import compare_skills, calculate_score, calculate_final_score, score_skill_groups, calculate_group_final_score
from src.semantic import calculate_semantic_similarity
from src.llm import generate_resume_suggestions, generate_interview_questions, parse_job_description

st.set_page_config(
    page_title="AI Resume & Interview Assistant",
    page_icon="📄",
    layout="wide",
)


@st.cache_data(show_spinner=False)
def get_semantic_score(resume_text, job_description):
    return calculate_semantic_similarity(resume_text, job_description)


@st.cache_data(show_spinner=False)
def get_resume_suggestions(resume_text, job_description, missing_skills):
    return generate_resume_suggestions(resume_text, job_description, missing_skills)


@st.cache_data(show_spinner=False)
def get_interview_questions(resume_text, job_description, missing_skills):
    return generate_interview_questions(resume_text, job_description, missing_skills)


@st.cache_data(show_spinner=False)
def get_job_description_parse(job_description):
    return parse_job_description(job_description)


def format_group(group):
    return " or ".join(group)


st.title("AI Resume & Interview Assistant")

st.write("Welcome! This app will help you match your resume to a job description.")

uploaded_resume = st.file_uploader("Upload your resume", type=["pdf", "docx"])

resume_text = None

if uploaded_resume is not None:
    file_name = uploaded_resume.name

    try:
        if file_name.endswith(".pdf"):
            resume_text = extract_text_from_pdf(uploaded_resume)
        elif file_name.endswith(".docx"):
            resume_text = extract_text_from_docx(uploaded_resume)
        else:
            st.error("Unsupported file type. Please upload a PDF or DOCX file.")
    except Exception as error:
        st.error(f"Couldn't read that file - it may be corrupted or password-protected. ({error})")

    if resume_text is not None and not resume_text.strip():
        st.warning(
            "We couldn't find any text in that file - it may be a scanned image "
            "rather than a text-based document. Try uploading a text-based PDF or DOCX instead."
        )
        resume_text = None
    elif resume_text is not None:
        st.success("Resume text extracted successfully!")
        with st.expander("View extracted resume text"):
            st.text_area("Extracted resume text", resume_text, height=300)

job_description = st.text_area("Paste the job description here")

if job_description:
    st.success("Job description received.")

if resume_text and job_description:
    with st.spinner("Analyzing job description..."):
        jd_parse = get_job_description_parse(job_description)

    if jd_parse:
        group_scores = score_skill_groups(
            resume_text, jd_parse["required_skill_groups"], jd_parse["preferred_skill_groups"]
        )
        semantic_score = get_semantic_score(resume_text, jd_parse["core_requirements_text"])
        final_score = calculate_group_final_score(
            group_scores["required_ratio"], group_scores["preferred_ratio"], semantic_score
        )
        missing_skills_tuple = tuple(
            format_group(g) for g in group_scores["required_missing"] + group_scores["preferred_missing"]
        )
    else:
        matched_skills, missing_skills = compare_skills(resume_text, job_description)
        job_skills = matched_skills | missing_skills

        skill_score = calculate_score(matched_skills, job_skills)
        semantic_score = get_semantic_score(resume_text, job_description)
        final_score = calculate_final_score(skill_score, semantic_score)
        missing_skills_tuple = tuple(sorted(missing_skills))

    st.header("Results")

    tab1, tab2, tab3 = st.tabs(["Match Analysis", "Resume Suggestions", "Interview Questions"])

    with tab1:
        st.metric("Overall Match Score", str(final_score) + "%")
        st.progress(final_score / 100)

        if final_score >= 70:
            st.success("Strong match - your resume aligns well with this job.")
        elif final_score >= 40:
            st.warning("Moderate match - there's room to improve your alignment.")
        else:
            st.error("Weak match - consider whether this role fits your current profile.")

        if jd_parse:
            st.subheader("Score breakdown")
            st.write("Required skills: " + str(round(group_scores["required_ratio"] * 100)) + "%")
            st.write("Preferred skills: " + str(round(group_scores["preferred_ratio"] * 100)) + "%")
            st.write("Semantic (meaning) match: " + str(round(semantic_score * 100)) + "%")

            st.subheader("Required skills you have")
            if group_scores["required_matched"]:
                st.write(", ".join(format_group(g) for g in group_scores["required_matched"]))
            else:
                st.write("None detected.")

            st.subheader("Required skills you're missing")
            if group_scores["required_missing"]:
                for g in group_scores["required_missing"]:
                    st.write("You need one of: " + format_group(g))
            else:
                st.write("None - your resume covers all the required skills we detected.")

            st.subheader("Preferred skills you have")
            if group_scores["preferred_matched"]:
                st.write(", ".join(format_group(g) for g in group_scores["preferred_matched"]))
            else:
                st.write("None detected.")

            st.subheader("Preferred skills you're missing")
            if group_scores["preferred_missing"]:
                for g in group_scores["preferred_missing"]:
                    st.write("You need one of: " + format_group(g))
            else:
                st.write("None - your resume covers all the preferred skills we detected.")

            if jd_parse["eligibility_requirements"]:
                st.subheader("Eligibility considerations")
                st.info("\n".join("- " + e for e in jd_parse["eligibility_requirements"]))
        else:
            st.subheader("Score breakdown")
            st.write("Skill match: " + str(skill_score) + "%")
            st.write("Semantic (meaning) match: " + str(round(semantic_score * 100)) + "%")

            st.subheader("Skills you have that match the job")
            st.write(", ".join(sorted(matched_skills)))

            st.subheader("Skills the job wants that are missing from your resume")
            if missing_skills:
                st.write(", ".join(sorted(missing_skills)))
            else:
                st.write("None - your resume covers all the skills we detected in the job description.")

    with tab2:
        st.subheader("AI-powered resume suggestion")
        with st.spinner("Generating suggestion..."):
            suggestions = get_resume_suggestions(resume_text, job_description, missing_skills_tuple)
        st.write(suggestions)

    with tab3:
        st.subheader("Interview questions to prepare for")

        if st.button("Generate interview questions"):
            with st.spinner("Generating interview questions..."):
                questions = get_interview_questions(resume_text, job_description, missing_skills_tuple)
            st.session_state.questions = questions

        if "questions" in st.session_state:
            st.write(st.session_state.questions)

    questions_for_report = st.session_state.get("questions", "Not generated - click the button in the Interview Questions tab.")

    if jd_parse:
        score_breakdown_report = f"""Required skills: {round(group_scores["required_ratio"] * 100)}%
Preferred skills: {round(group_scores["preferred_ratio"] * 100)}%
Semantic (meaning) match: {round(semantic_score * 100)}%

REQUIRED SKILLS YOU HAVE
{", ".join(format_group(g) for g in group_scores["required_matched"]) or "None detected."}

REQUIRED SKILLS YOU'RE MISSING
{chr(10).join("You need one of: " + format_group(g) for g in group_scores["required_missing"]) or "None."}

PREFERRED SKILLS YOU HAVE
{", ".join(format_group(g) for g in group_scores["preferred_matched"]) or "None detected."}

PREFERRED SKILLS YOU'RE MISSING
{chr(10).join("You need one of: " + format_group(g) for g in group_scores["preferred_missing"]) or "None."}

ELIGIBILITY CONSIDERATIONS
{chr(10).join("- " + e for e in jd_parse["eligibility_requirements"]) or "None stated."}"""
    else:
        score_breakdown_report = f"""Skill match: {skill_score}%
Semantic (meaning) match: {round(semantic_score * 100)}%

SKILLS YOU HAVE THAT MATCH THE JOB
{", ".join(sorted(matched_skills))}

SKILLS MISSING FROM YOUR RESUME
{", ".join(sorted(missing_skills))}"""

    report = f"""AI RESUME & INTERVIEW ASSISTANT - ANALYSIS REPORT

OVERALL MATCH SCORE: {final_score}%

SCORE BREAKDOWN
{score_breakdown_report}

RESUME SUGGESTIONS
{suggestions}

INTERVIEW QUESTIONS TO PREPARE FOR
{questions_for_report}
"""

    st.download_button(
        label="Download full report",
        data=report,
        file_name="resume_analysis_report.txt",
        mime="text/plain",
    )
