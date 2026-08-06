"""One-off script to regenerate src/data/known_skills.json using Gemini.

Run manually whenever you want to refresh the tech stack list:
    python -m scripts.generate_skills
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.llm import generate_text

OUTPUT_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "src", "data", "known_skills.json",
)

PROMPT = """List as many real-world tech stack skills as you can that appear on resumes and in job descriptions.

Include: programming languages, frameworks, libraries, databases, cloud platforms, DevOps/infra tools, data/ML tools, testing tools, and common professional/soft skills relevant to tech roles (e.g. agile, scrum, communication, project management).

Rules:
- Output ONLY a JSON array of strings, nothing else - no markdown fences, no commentary.
- Each entry must be lowercase.
- No duplicates.
- Prefer the common short form (e.g. "aws" not "amazon web services", "postgresql" not "PostgreSQL").
- Aim for at least 150 entries.
"""


def clean_json_response(text):
    text = text.strip()
    if text.startswith("```"):
        text = text.split("\n", 1)[1]
        if text.endswith("```"):
            text = text.rsplit("```", 1)[0]
    return text.strip()


def main():
    raw = generate_text(PROMPT)
    cleaned = clean_json_response(raw)

    try:
        skills = json.loads(cleaned)
    except json.JSONDecodeError as error:
        print("Failed to parse Gemini response as JSON.")
        print("Raw response:\n", raw)
        raise SystemExit(1) from error

    if not isinstance(skills, list) or not all(isinstance(s, str) for s in skills):
        print("Gemini response was not a JSON array of strings.")
        raise SystemExit(1)

    normalized = sorted({s.strip().lower() for s in skills if s.strip()})

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w") as f:
        json.dump(normalized, f, indent=2)
        f.write("\n")

    print(f"Wrote {len(normalized)} skills to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
