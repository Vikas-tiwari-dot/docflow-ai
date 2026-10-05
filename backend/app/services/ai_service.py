import logging

from groq import Groq

from app.core.config import get_settings

logger = logging.getLogger("docflow.ai")


def answer_question(question: str, chunks: list[str]):
    settings = get_settings()

    context = "\n\n---\n\n".join(chunks[:8])

    if not settings.groq_api_key:
        return (
            "Groq is not configured. Add GROQ_API_KEY to the backend "
            "environment to enable AI answers.\n\n"
            "Document context available:\n"
            + context[:1200]
        )

    prompt = f"""
You are DocFlow AI, an AI document assistant.

Answer the user's question ONLY using the supplied document context.
If the answer is not present in the context, clearly say that the
information is not available in the document.

Be concise, accurate, and directly answer the question.

Document Context:
{context}

Question:
{question}
"""

    try:
        client = Groq(api_key=settings.groq_api_key)

        response = client.chat.completions.create(
            model=settings.groq_model,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You answer questions based only on provided "
                        "document context."
                    ),
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
            temperature=0.2,
        )

        return response.choices[0].message.content.strip()

    except Exception:
        logger.exception("Groq API failure")
        raise RuntimeError("AI provider request failed")