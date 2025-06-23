import os
import openai
from dotenv import load_dotenv

load_dotenv()

def ask_groq(query: str, context: str = "") -> str:
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        return "❌ GROQ_API_KEY not found in environment variables."

    openai.api_key = api_key
    openai.api_base = "https://api.groq.com/openai/v1"

    try:
        messages = [
            {"role": "system", "content": "Answer based on context."}
        ]

        if context:
            messages.append({"role": "user", "content": context + "\n\n" + query})
        else:
            messages.append({"role": "user", "content": query})

        response = openai.ChatCompletion.create(
            model="llama3-8b-8192",
            messages=messages,
            timeout=30
        )
        return response.choices[0].message.content

    except openai.error.OpenAIError as e:
        return f"❌ Error from Groq API: {e}"

    except Exception as e:
        return f"❌ Unexpected error: {e}"
