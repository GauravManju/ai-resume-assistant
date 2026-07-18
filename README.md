# AI Resume & Interview Assistant 

An AI-powered assistant that helps job-seekers understand how well their resume matches a specific job description, identifies missing skills, and (in later versions) suggests improvements and generates interview questions.

## Problem

Job-seekers can't easily tell how well their resume fits a specific job, which skills or keywords they're missing, or how to improve - so they often apply blindly and get rejected without understanding why.

## Features

### MVP (current focus)

- Upload a resume in PDF or DOCX format
- Paste or type a job description
- Extract text from the resume
- Extract skills from the resume and job description
- Compare them and identify missing skills
- Calculate a transparent, explainable match score
- Display results in a clean web interface

### Planned (later versions)

- LLM-based resume improvement suggestions
- Role-specific interview question generation
- STAR-style answer guidance
- Learning recommendations for missing skills
- Saved analysis history

## Tech Stack

- **Python** — core programming language
- **Streamlit** — web interface (pure-Python UI)
- **PyMuPDF** — extract text from PDF resumes
- **python-docx** — extract text from DOCX resumes
- **scikit-learn** — supporting ML utilities for matching
- **sentence-transformers** — semantic similarity via embeddings
- **Git & GitHub** — version control and hosting