import requests
import json

def ask_ollama(prompt: str) -> str:
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": "deepseek-r1:1.5b", "prompt": prompt},
            timeout=30,
            stream=True  # IMPORTANT: enables line-by-line streaming
        )

        output = ""
        for line in response.iter_lines():
            if line:
                try:
                    data = json.loads(line.decode("utf-8"))
                    if "response" in data:
                        output += data["response"]
                except json.JSONDecodeError:
                    continue  # Skip bad chunks

        return output.strip() or "⚠️ No content received from Ollama"

    except Exception as e:
        return f"❌ Error from Ollama: {e}"
