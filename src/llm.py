import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

def generate_text(prompt):
    try:
        response = client.models.generate_content(
            model="gemini-flash-latest",
            contents=prompt,
        )
        return response.text
    except Exception as error:
        return "Sorry, the AI service is currently unavailable. Please try again in a moment. (Error: " + str(error) + ")"

def generate_resume_suggestions(resume_text, job_description, missing_skills):
    missing_skills_text = ", ".join(missing_skills)

    prompt = f"""You are an experienced recruiter and career coach.

Here is a candidate's resume:
{resume_text}

Here is the job description they are applying for:
{job_description}

The candidate is missing these skills that the job requires:
{missing_skills_text}

Based only on the information in the resume and job description, suggest 3 to 5 specific, practical improvements the candidate could make to their resume to better match this job.

Rules:
- Only use information already present in the resume. Do not invent skills, projects, or experience the candidate does not have.
- If an important skill is missing, suggest that the candidate gain or highlight it honestly - do not fabricate it.
- Be specific and actionable, not generic.
- Format the output as a numbered list of suggestions."""

    return generate_text(prompt)