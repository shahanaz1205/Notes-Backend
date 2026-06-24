from services.gemini import summarize_text

try:
    text = """
    Python is a high-level programming language.
    It is widely used for web development,
    artificial intelligence, data science,
    automation, and software development.
    """

    result = summarize_text(text)

    print("SUCCESS")
    print(result)

except Exception as e:
    print("ERROR")
    print(str(e))