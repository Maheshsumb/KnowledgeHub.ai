from langchain_core.documents import Document

from app.schemas.parsed_document import ParsedDocument


class DocumentNormalizer:

    @staticmethod
    def normalize(documents: list[Document]) -> ParsedDocument:

        content = "\n\n".join(
            document.page_content
            for document in documents
        )

        metadata = {}

        if documents:
            metadata = documents[0].metadata

        return ParsedDocument(
            content=content,
            page_count=len(documents),
            metadata=metadata,
            title=metadata.get("title"),
        )