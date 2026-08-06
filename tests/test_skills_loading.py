from src import skills


def test_load_known_skills_falls_back_when_file_missing(tmp_path, monkeypatch):
    monkeypatch.setattr(skills, "_KNOWN_SKILLS_PATH", str(tmp_path / "missing.json"))

    result = skills._load_known_skills()

    assert result == skills._FALLBACK_SKILLS


def test_load_known_skills_falls_back_when_file_corrupt(tmp_path, monkeypatch):
    bad_file = tmp_path / "known_skills.json"
    bad_file.write_text("not valid json")
    monkeypatch.setattr(skills, "_KNOWN_SKILLS_PATH", str(bad_file))

    result = skills._load_known_skills()

    assert result == skills._FALLBACK_SKILLS


def test_load_known_skills_reads_generated_file(tmp_path, monkeypatch):
    real_file = tmp_path / "known_skills.json"
    real_file.write_text('["golang", "rust"]')
    monkeypatch.setattr(skills, "_KNOWN_SKILLS_PATH", str(real_file))

    result = skills._load_known_skills()

    assert result == ["golang", "rust"]
