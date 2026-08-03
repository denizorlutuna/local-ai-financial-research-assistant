import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3.2:3b"


def generate_response(prompt):
    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False,
    }

    try:
        response = requests.post(
            OLLAMA_URL,
            json=payload,
            timeout=120,
        )

        response.raise_for_status()
        data = response.json()

        generated_text = data.get("response")

        if not generated_text:
            return (
                "AI analysis is currently unavailable. "
                "The financial report was generated successfully."
            )

        return generated_text.strip()

    except requests.exceptions.ConnectionError:
        return (
            "AI analysis is currently unavailable because Ollama "
            "could not be reached. The financial report was generated "
            "successfully."
        )

    except requests.exceptions.Timeout:
        return (
            "AI analysis timed out. The financial report was generated "
            "successfully."
        )

    except requests.exceptions.RequestException as error:
        return (
            "AI analysis could not be generated. "
            f"Ollama request error: {error}"
        )