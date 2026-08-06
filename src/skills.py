import json
import os
import re

# Fallback used only if src/data/known_skills.json hasn't been generated yet.
# Run `python -m scripts.generate_skills` to (re)populate that file from Gemini.
_FALLBACK_SKILLS = [
    "python", "java", "sql", "javascript", "html", "css", "react",
    "docker", "kubernetes", "aws", "azure", "git",
    "machine learning", "deep learning", "nlp",
    "pandas", "numpy", "tensorflow", "pytorch",
    "excel", "oracle", "mongodb", "postgresql", "mysql",
    "testing", "documentation", "linux", "bash", "rest api",
    "flask", "django", "spark", "hadoop", "tableau", "power bi",
    "data analysis", "communication", "project management",
    "agile", "scrum",
]

_KNOWN_SKILLS_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "data", "known_skills.json"
)


def _load_known_skills():
    try:
        with open(_KNOWN_SKILLS_PATH) as f:
            skills = json.load(f)
        if isinstance(skills, list) and skills:
            return skills
    except (FileNotFoundError, json.JSONDecodeError):
        pass
    return _FALLBACK_SKILLS


KNOWN_SKILLS = _load_known_skills()


def _build_skill_pattern(skill):
    # Tolerates punctuation/spacing variants within a term (e.g. "Node.js" vs
    # "nodejs", "Spring Boot" vs "springboot") while the outer word-boundary
    # anchors still block accidental substring matches inside unrelated words
    # (e.g. "react" must not match inside "reaction").
    body = r"[\s\-./]{0,2}".join(re.escape(c) for c in skill.lower() if c.isalnum())
    return re.compile(r"(?<![a-z0-9])" + body + r"(?![a-z0-9])")


_SKILL_PATTERNS = {skill: _build_skill_pattern(skill) for skill in KNOWN_SKILLS}


def extract_skills(text):
    text_lower = text.lower()

    found_skills = set()
    for skill, pattern in _SKILL_PATTERNS.items():
        if pattern.search(text_lower):
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

def calculate_final_score(skill_score, semantic_score):
    semantic_percentage = semantic_score * 100

    final_score = (0.7 * skill_score) + (0.3 * semantic_percentage)

    return round(final_score)


def _group_ratio(groups, resume_text):
    if not groups:
        return 1.0, [], []

    text_lower = resume_text.lower()
    matched, missing = [], []
    for group in groups:
        if any(_build_skill_pattern(term).search(text_lower) for term in group):
            matched.append(group)
        else:
            missing.append(group)

    return len(matched) / len(groups), matched, missing


def score_skill_groups(resume_text, required_groups, preferred_groups):
    required_ratio, required_matched, required_missing = _group_ratio(required_groups, resume_text)
    preferred_ratio, preferred_matched, preferred_missing = _group_ratio(preferred_groups, resume_text)

    return {
        "required_ratio": required_ratio,
        "required_matched": required_matched,
        "required_missing": required_missing,
        "preferred_ratio": preferred_ratio,
        "preferred_matched": preferred_matched,
        "preferred_missing": preferred_missing,
    }


def calculate_group_final_score(required_ratio, preferred_ratio, semantic_score):
    final_score = (0.60 * required_ratio * 100) + (0.15 * preferred_ratio * 100) + (0.25 * semantic_score * 100)
    return round(final_score)