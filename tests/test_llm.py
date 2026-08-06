from src import llm


class FakeResponse:
    def __init__(self, text):
        self.text = text


def test_generate_text_returns_response_text(monkeypatch):
    monkeypatch.setattr(
        llm.client.models,
        "generate_content",
        lambda model, contents: FakeResponse("some suggestions"),
    )

    result = llm.generate_text("any prompt")

    assert result == "some suggestions"


def test_generate_text_handles_api_failure(monkeypatch):
    def raise_error(model, contents):
        raise RuntimeError("quota exceeded")

    monkeypatch.setattr(llm.client.models, "generate_content", raise_error)

    result = llm.generate_text("any prompt")

    assert "currently unavailable" in result
    assert "quota exceeded" in result


def test_parse_job_description_returns_structured_data(monkeypatch):
    valid_json = """{
        "core_requirements_text": "Build things with Python.",
        "required_skill_groups": [["python"], ["docker", "kubernetes"]],
        "preferred_skill_groups": [["aws"]],
        "eligibility_requirements": ["Must hold a valid work visa"]
    }"""
    monkeypatch.setattr(
        llm.client.models,
        "generate_content",
        lambda **kwargs: FakeResponse(valid_json),
    )

    result = llm.parse_job_description("some job description")

    assert result["core_requirements_text"] == "Build things with Python."
    assert result["required_skill_groups"] == [["python"], ["docker", "kubernetes"]]
    assert result["preferred_skill_groups"] == [["aws"]]
    assert result["eligibility_requirements"] == ["Must hold a valid work visa"]


def test_parse_job_description_returns_none_on_api_failure(monkeypatch):
    def raise_error(**kwargs):
        raise RuntimeError("quota exceeded")

    monkeypatch.setattr(llm.client.models, "generate_content", raise_error)

    result = llm.parse_job_description("some job description")

    assert result is None


def test_parse_job_description_returns_none_on_invalid_schema(monkeypatch):
    monkeypatch.setattr(
        llm.client.models,
        "generate_content",
        lambda **kwargs: FakeResponse('{"unexpected": "shape"}'),
    )

    result = llm.parse_job_description("some job description")

    assert result is None


def test_parse_job_description_returns_none_on_blank_core_text(monkeypatch):
    blank_json = """{
        "core_requirements_text": "   ",
        "required_skill_groups": [],
        "preferred_skill_groups": [],
        "eligibility_requirements": []
    }"""
    monkeypatch.setattr(
        llm.client.models,
        "generate_content",
        lambda **kwargs: FakeResponse(blank_json),
    )

    result = llm.parse_job_description("some job description")

    assert result is None


def test_parse_job_description_filters_overly_long_group_terms(monkeypatch):
    long_term_json = """{
        "core_requirements_text": "Build things.",
        "required_skill_groups": [["python"], ["five or more years of relevant hands-on experience"]],
        "preferred_skill_groups": [],
        "eligibility_requirements": []
    }"""
    monkeypatch.setattr(
        llm.client.models,
        "generate_content",
        lambda **kwargs: FakeResponse(long_term_json),
    )

    result = llm.parse_job_description("some job description")

    assert result["required_skill_groups"] == [["python"]]
