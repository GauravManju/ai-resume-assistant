import logging
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from pydantic import BaseModel, ValidationError

load_dotenv()

logger = logging.getLogger(__name__)

api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)


class JobDescriptionParse(BaseModel):
    core_requirements_text: str
    required_skill_groups: list[list[str]]
    preferred_skill_groups: list[list[str]]
    eligibility_requirements: list[str]


_JD_PARSE_PROMPT = """You are parsing a job description into structured data for a resume-matching tool.

Return JSON with these fields:
- core_requirements_text: the job description trimmed down to just the role's responsibilities and skill requirements. Remove all company boilerplate - "about the company" sections, benefits, equal opportunity statements, culture/mission blurbs, and anything not describing what the role actually needs.
- required_skill_groups: a list of groups, where each group is a list of alternative skill names the job treats as interchangeable (e.g. if the job says "React or Angular", that is one group: ["React", "Angular"]; if it says "Python" alone, that is a group with one item: ["Python"]). Only include groups from sections describing required/must-have skills. Keep each skill name to at most 4 words.
- preferred_skill_groups: same format as required_skill_groups, but only for skills explicitly described as preferred, nice-to-have, or a bonus.
- eligibility_requirements: any explicit non-skill eligibility requirements stated in the posting, quoted or closely paraphrased - for example visa sponsorship availability, residency/citizenship requirements, required security clearances, or similar hard gates. Empty list if none are stated.

Job description:
{job_description}
"""


def parse_job_description(job_description_text):
    prompt = _JD_PARSE_PROMPT.format(job_description=job_description_text)

    try:
        response = client.models.generate_content(
            model="gemini-flash-lite-latest",
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=JobDescriptionParse,
            ),
        )
    except Exception:
        logger.exception("Gemini call failed while parsing job description")
        return None

    try:
        parsed = JobDescriptionParse.model_validate_json(response.text)
    except (ValidationError, ValueError):
        logger.exception("Gemini returned an invalid job description structure")
        return None

    if not parsed.core_requirements_text.strip():
        return None

    def clean_groups(groups):
        cleaned = []
        for group in groups:
            terms = [term.strip() for term in group if term.strip() and len(term.split()) <= 4]
            if terms:
                cleaned.append(terms)
        return cleaned

    return {
        "core_requirements_text": parsed.core_requirements_text,
        "required_skill_groups": clean_groups(parsed.required_skill_groups),
        "preferred_skill_groups": clean_groups(parsed.preferred_skill_groups),
        "eligibility_requirements": [e.strip() for e in parsed.eligibility_requirements if e.strip()],
    }


def generate_text(prompt):
    try:
        response = client.models.generate_content(
            model="gemini-flash-lite-latest",
            contents=prompt,
        )
        return response.text
    except Exception as error:
        logger.exception("Gemini generate_content call failed")
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

def generate_interview_questions(resume_text, job_description, missing_skills):
    missing_skills_text = ", ".join(missing_skills)

    prompt = f"""You are an experienced technical interviewer and hiring manager.

Here is the candidate's resume:
{resume_text}

Here is the job description they are applying for:
{job_description}

Skills the job requires that are NOT on the candidate's resume:
{missing_skills_text}

Generate 6 interview questions this candidate should prepare for. Include a mix of:
- Technical questions based on the candidate's actual skills and projects
- Behavioural questions
- Situational or problem-solving questions

Rules:
- Never invent projects, skills, or work experience that are not in the resume.
- For skills the job requires but the resume lacks, ask learning-oriented questions instead of assuming experience. For example: "This role uses Docker. What do you know about it, and how would you approach learning it?"
- Every question must connect to either the resume or the job description.
- Keep questions realistic - the kind a real hiring manager would actually ask.
- Format as a numbered list. After each question, add a short italic note explaining what the interviewer is assessing."""

    return generate_text(prompt)