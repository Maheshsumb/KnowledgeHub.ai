from app.schemas.retrieval import RetrievedChunk


class ContextBuilder:
    """
    Builds a formatted context from retrieved chunks.
    """

    @staticmethod
    def build(
        chunks: list[RetrievedChunk],
    ) -> str:

        if not chunks:
            return ""

        sections = []

        for index, chunk in enumerate(chunks, start=1):

            source = chunk.metadata.get(
                "source",
                "Unknown",
            )

            sections.append(
                f"""
Document {index}
Source: {source}

Content:
{chunk.content}
""".strip()
            )

        return "\n\n-------------------------\n\n".join(
            sections
        )