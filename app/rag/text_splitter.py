def split_pages_into_chunks(
    pages,
    chunk_size=1200,
    overlap=200,
):
    if chunk_size <= overlap:
        raise ValueError(
            "Chunk size must be greater than overlap."
        )

    chunks = []

    for page in pages:
        text = " ".join(page["text"].split())
        start = 0
        chunk_index = 0

        while start < len(text):
            end = start + chunk_size
            chunk_text = text[start:end].strip()

            if chunk_text:
                chunks.append(
                    {
                        "text": chunk_text,
                        "page_number": page["page_number"],
                        "chunk_index": chunk_index,
                    }
                )

            start += chunk_size - overlap
            chunk_index += 1

    return chunks