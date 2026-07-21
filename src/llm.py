import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

def generate_text(prompt):
    response = client.models.generate_content(
        model="gemini-flash-latest",
        contents=prompt,
    )
    return response.text