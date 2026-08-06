from src.skills import (
    extract_skills,
    compare_skills,
    calculate_score,
    calculate_final_score,
    score_skill_groups,
    calculate_group_final_score,
)


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


def test_extract_skills_matches_punctuation_variants():
    text = "Back-end experience with Java/Spring Boot or Node.js required."
    result = extract_skills(text)

    assert "springboot" in result
    assert "nodejs" in result


def test_extract_skills_does_not_false_positive_on_similar_words():
    text = (
        "The team's reaction to the escalating deadline was to embrace a "
        "kafkaesque, resparkling, vagile, yogasana-inspired workflow."
    )
    result = extract_skills(text)

    assert "react" not in result
    assert "scala" not in result
    assert "kafka" not in result
    assert "spark" not in result
    assert "agile" not in result
    assert "asana" not in result


def test_score_skill_groups_or_group_satisfied_by_one_alternative():
    resume = "Experienced with React and REST APIs."
    required_groups = [["react", "angular"]]

    result = score_skill_groups(resume, required_groups, [])

    assert result["required_ratio"] == 1.0
    assert result["required_matched"] == [["react", "angular"]]
    assert result["required_missing"] == []


def test_score_skill_groups_or_group_fully_missing():
    resume = "Experienced with Vue and REST APIs."
    required_groups = [["react", "angular"]]

    result = score_skill_groups(resume, required_groups, [])

    assert result["required_ratio"] == 0.0
    assert result["required_missing"] == [["react", "angular"]]


def test_score_skill_groups_empty_groups_are_vacuously_satisfied():
    result = score_skill_groups("any resume text", [], [])

    assert result["required_ratio"] == 1.0
    assert result["preferred_ratio"] == 1.0


def test_score_skill_groups_handles_regex_metacharacters():
    resume = "Skilled in C++ and C#."
    required_groups = [["c++"], ["c#"]]

    result = score_skill_groups(resume, required_groups, [])

    assert result["required_ratio"] == 1.0


def test_calculate_group_final_score_reaches_100_with_no_preferred_section():
    score = calculate_group_final_score(required_ratio=1.0, preferred_ratio=1.0, semantic_score=1.0)

    assert score == 100