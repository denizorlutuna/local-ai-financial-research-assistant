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
        text = " ".join(
            page["text"].split()
        )

        start = 0
        chunk_index = 0

        while start < len(text):
            end = min(
                start + chunk_size,
                len(text),
            )

            # Chunk bitişini kelimenin ortasından kesmemek için
            if end < len(text):
                last_space = text.rfind(
                    " ",
                    start,
                    end,
                )

                if last_space > start:
                    end = last_space

            chunk_text = text[start:end].strip()

            if chunk_text:
                chunks.append(
                    {
                        "text": chunk_text,
                        "page_number": page["page_number"],
                        "chunk_index": chunk_index,
                    }
                )

            if end >= len(text):
                break

            # Overlap uygula
            next_start = end - overlap

            # Başlangıç kelimenin ortasındaysa
            # bir sonraki boşluğa ilerle
            if (
                next_start > 0
                and text[next_start - 1] != " "
            ):
                next_space = text.find(
                    " ",
                    next_start,
                )

                if next_space != -1:
                    next_start = next_space + 1

            # Sonsuz veya çok yavaş ilerleyen döngüyü engelle
            if next_start <= start:
                next_start = end

            start = next_start
            chunk_index += 1

    return chunks