import os
from dotenv import load_dotenv
from google import genai

# Load .env
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise Exception("GEMINI_API_KEY not found in .env file")

print("LOADED KEY:", GEMINI_API_KEY[:15])

# Create Client
client = genai.Client(api_key=GEMINI_API_KEY)


# ==========================
# Gemini Helper
# ==========================
def call_gemini(prompt):
    models = [
        "gemini-3.1-flash-lite",
        "gemini-3-flash",
        "gemini-2.5-flash-lite"
    ]

    last_error = None

    for model_name in models:
        try:
            response = client.models.generate_content(
                model=model_name,
                contents=prompt
            )

            print(f"\nSUCCESS USING MODEL: {model_name}\n")
            return response.text

        except Exception as e:
            print(f"\nFAILED MODEL: {model_name}")
            print(str(e))
            last_error = e

    return f"Gemini Error: {str(last_error)}"


# ==========================
# Generate Notes
# ==========================
def generate_notes(topic: str, words: int, language: str = "English"):
    try:
        prompt = f"""
Generate detailed, clean and structured notes on "{topic}"
in approximately {words} words.

STRICT RULES:
- Write the entire response only in {language}
- Return response ONLY in markdown format
- Use proper markdown headings (#, ##)
- Use bullet points where needed
- Keep clean spacing
- Do NOT return plain text

Format EXACTLY like this:

# Detailed Notes: {topic}

## Introduction
Write introduction here.

## Main Points
- Point 1
- Point 2
- Point 3

## Conclusion
Write conclusion here.
"""

        result = call_gemini(prompt)

        print("\n========== GEMINI OUTPUT ==========")
        print(result)
        print("===================================\n")

        return result

    except Exception as e:
        return f"Gemini Error: {str(e)}"


# ==========================
# Summarize Text / PDF
# ==========================
def summarize_text(text: str):
    try:
        prompt = f"""
Summarize the following content clearly:

{text}
"""

        result = call_gemini(prompt)

        print("\n========== SUMMARY OUTPUT ==========")
        print(result)
        print("====================================\n")

        return result

    except Exception as e:
        return f"Gemini Error: {str(e)}"


# ==========================
# Ask Questions From PDF
# ==========================
def ask_pdf_question(pdf_text: str, question: str):
    try:
        prompt = f"""
Based on the following PDF content:

{pdf_text}

Answer this question:

{question}

If answer is not available in PDF,
reply only:

Answer not found in PDF.
"""

        result = call_gemini(prompt)

        print("\n========== PDF QA OUTPUT ==========")
        print(result)
        print("===================================\n")

        return result

    except Exception as e:
        return f"Gemini Error: {str(e)}"


# ==========================
# Ask Questions From Notes
# ==========================
def ask_notes_question(notes_text: str, question: str):
    try:
        prompt = f"""
Notes Content:

{notes_text}

Question:

{question}

Answer only from the notes content.
"""

        result = call_gemini(prompt)

        print("\n========== NOTES QA OUTPUT ==========")
        print(result)
        print("=====================================\n")

        return result

    except Exception as e:
        return f"Gemini Error: {str(e)}"