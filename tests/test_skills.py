from src.skills import extract_skills
from src.skills import extract_skills, compare_skills, calculate_score, calculate_final_score


def test_extract_skills_finds_known_skills():
    text = "I have experience with Python, SQL, and Docker."
    result = extract_skills(text)

    assert "python" in result
    assert "sql" in result
    assert "docker" in result

from src.skills import extract_skills, compare_skills, calculate_score, calculate_final_score


def test_extract_skills_ignores_unknown_words():
    text = "I enjoy hiking and cooking on weekends."
    result = extract_skills(text)

    assert result == set()


def test_compare_skills_finds_matched_and_missing():
    resume = "I know Python and SQL."
    job = "We need Python, Docker, and AWS."

    matched, missing = compare_skills(resume, job)

    assert "python" in matched
    assert "docker" in missing
    assert "aws" in missing
    assert "python" not in missing


def test_calculate_score_basic():
    matched = {"python", "sql"}
    job_skills = {"python", "sql", "docker", "aws"}

    score = calculate_score(matched, job_skills)

    assert score == 50


def test_calculate_score_handles_empty_job_skills():
    matched = set()
    job_skills = set()

    score = calculate_score(matched, job_skills)

    assert score == 0


def test_final_score_weighting():
    score = calculate_final_score(80, 0.5)

    assert score == 71