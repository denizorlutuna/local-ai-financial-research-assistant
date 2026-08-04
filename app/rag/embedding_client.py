import requests


OLLAMA_EMBED_URL = "http://localhost:11434/api/embed"
EMBEDDING_MODEL = "embeddinggemma"


def generate_embeddings(texts):
    if not texts:
        return []

    payload = {
        "model": EMBEDDING_MODEL,
        "input": texts,
    }

    try:
        response = requests.post(
            OLLAMA_EMBED_URL,
            json=payload,
            timeout=180,
        )
        response.raise_for_status()

        data = response.json()
        embeddings = data.get("embeddings")

        if not embeddings:
            raise ValueError(
                "Ollama returned no embeddings."
            )

        return embeddings

    except requests.exceptions.ConnectionError as error:
        raise RuntimeError(
            "Could not connect to Ollama."
        ) from error

    except requests.exceptions.Timeout as error:
        raise RuntimeError(
            "Embedding request timed out."
        ) from error

    except requests.exceptions.RequestException as error:
        raise RuntimeError(
            f"Embedding request failed: {error}"
        ) from error