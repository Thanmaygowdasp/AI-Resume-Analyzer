import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=api_key)

model = genai.GenerativeModel(
    "gemini-2.5-flash"
)


def get_ai_feedback(text):

    prompt = f"""
    You are an expert resume reviewer.

    Analyze the resume.

    Give:   

    1. 3 Strengths
    2. 3 Improvements
    3. 3 Weaknesses 

    Keep response under 200 words.

    Resume:

    {text}
    """

    try:
        response = model.generate_content(prompt)
        return response.text

    except Exception:
        return """
            ⚠️ Gemini API Limit Reached
            Please wait a minute and try again.
            """