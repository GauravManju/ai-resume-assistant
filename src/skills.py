KNOWN_SKILLS = [
    "python",
    "java",
    "sql",
    "javascript",
    "html",
    "css",
    "react",
    "docker",
    "kubernetes",
    "aws",
    "azure",
    "git",
    "machine learning",
    "deep learning",
    "nlp",
    "pandas",
    "numpy",
    "tensorflow",
    "pytorch",
    "excel",
    "oracle",
    "mongodb",
    "postgresql",
    "mysql",
    "testing",
    "documentation",
    "linux",
    "bash",
    "rest api",
    "flask",
    "django",
    "spark",
    "hadoop",
    "tableau",
    "power bi",
    "data analysis",
    "communication",
    "project management",
    "agile",
    "scrum",
]


def extract_skills(text):
    text_lower = text.lower()

    found_skills = set()
    for skill in KNOWN_SKILLS:
        if skill in text_lower:
            found_skills.add(skill)

    return found_skills

def compare_skills(resume_text, job_description_text):
    resume_skills = extract_skills(resume_text)
    job_skills = extract_skills(job_description_text)

    matched_skills = job_skills & resume_skills
    missing_skills = job_skills - resume_skills

    return matched_skills, missing_skills

def calculate_score(matched_skills, job_skills):
    if len(job_skills) == 0:
        return 0

    score = len(matched_skills) / len(job_skills) * 100
    return round(score)