from pathlib import Path

from langchain_community.document_loaders import (
    BSHTMLLoader,
    CSVLoader,
    Docx2txtLoader,
    JSONLoader,
    PyMuPDFLoader,
    TextLoader,
    UnstructuredExcelLoader,
    UnstructuredPowerPointLoader,
)

from app.services.ingestion.exceptions import UnsupportedDocumentTypeError


class LoaderFactory:
    """
    Returns the appropriate LangChain loader based on file extension.
    """

    @staticmethod
    def get_loader(file_path: str):
        extension = Path(file_path).suffix.lower()

        loaders = {
            ".pdf": lambda: PyMuPDFLoader(file_path),
            ".txt": lambda: TextLoader(file_path, encoding="utf-8"),
            ".md": lambda: TextLoader(file_path, encoding="utf-8"),
            ".docx": lambda: Docx2txtLoader(file_path),
            ".csv": lambda: CSVLoader(file_path),
            ".html": lambda: BSHTMLLoader(file_path),
            ".htm": lambda: BSHTMLLoader(file_path),
            ".json": lambda: JSONLoader(
                file_path=file_path,
                jq_schema=".",
                text_content=False,
            ),
            ".pptx": lambda: UnstructuredPowerPointLoader(file_path),
            ".xlsx": lambda: UnstructuredExcelLoader(file_path),
        }

        try:
            return loaders[extension]()
        except KeyError:
            raise UnsupportedDocumentTypeError(
                f"Unsupported file type: {extension}"
            )