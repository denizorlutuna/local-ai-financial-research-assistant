from app.ai.ollama_client import generate_response
from app.rag.retriever import search_similar_chunks


def answer_question(
    query,
    top_k=5,
    document_name=None,
):
    results = search_similar_chunks(
        query,
        top_k=top_k,
        document_name=document_name,
    )

    if not results:
        return {
            "answer": "No relevant information was found.",
            "sources": [],
        }

    context_parts = []

    for result in results:
        context_parts.append(
            f"Page {result['page_number']}:\n{result['text']}"
        )

    context = "\n\n".join(context_parts)

    prompt = f"""
You are a financial document research assistant.

Answer the user's question using only the document context below.

Instructions:

- Give a direct and concise answer.
- Answer using only information supported by the document context.
- Summarize the main points instead of copying the context.
- Do not invent information.
- Ignore irrelevant context.
- Mention uncertainty if the context is insufficient.
- When listing multiple points, use Markdown bullet points.
- Put every bullet point on a separate line.
- Start each bullet point with "- ".
- Do not place multiple bullet points on the same line.
- Keep each bullet point concise and readable.
- Cite the relevant source page at the end of each important point,
  for example: [Page 14].
- Do not create a separate Sources section.
- Do not give personal investment advice.

Question:
{query}

Document Context:
{context}
"""

    answer = generate_response(prompt)

    sources = []

    for result in results:
        sources.append(
            {
                "document_name": result["document_name"],
                "page_number": result["page_number"],
                "distance": result["distance"],
            }
        )

    return {
        "answer": answer,
        "sources": sources,
    }


def main():
    query = "What are Apple's main business risks?"

    result = answer_question(
        query=query,
        top_k=5,
    )

    print(f"Question: {query}")
    print("\nAnswer:")
    print(result["answer"])

    print("\nSources:")

    for source in result["sources"]:
        print(
            f"- {source['document_name']} | "
            f"Page {source['page_number']} | "
            f"distance: {source['distance']:.4f}"
        )


if __name__ == "__main__":
    main()