import requests


OLLAMA_EMBED_URL = "http://localhost:11434/api/embed"
EMBEDDING_MODEL = "embeddinggemma"
BATCH_SIZE = 32


def generate_embeddings(texts):
    if not texts:
        return []

    all_embeddings = []

    for start in range(0, len(texts), BATCH_SIZE):
        batch = texts[start:start + BATCH_SIZE]

        payload = {
            "model": EMBEDDING_MODEL,
            "input": batch,
        }

        try:
            response = requests.post(
                OLLAMA_EMBED_URL,
                json=payload,
                timeout=180,
            )

            if not response.ok:
                raise RuntimeError(
                    f"Ollama returned {response.status_code}: "
                    f"{response.text}"
                )

            data = response.json()
            embeddings = data.get("embeddings")

            if not embeddings:
                raise ValueError(
                    "Ollama returned no embeddings."
                )

            all_embeddings.extend(embeddings)

            completed = min(
                start + BATCH_SIZE,
                len(texts),
            )

            print(
                f"Embeddings created: "
                f"{completed}/{len(texts)}"
            )

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

    return all_embeddings