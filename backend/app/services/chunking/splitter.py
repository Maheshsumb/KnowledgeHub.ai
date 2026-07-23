from langchain_text_splitters import RecursiveCharacterTextSplitter


class TextSplitter:
    """
    Wrapper around LangChain's RecursiveCharacterTextSplitter.
    """

    def __init__(
        self,
        chunk_size: int = 1000,
        chunk_overlap: int = 200,
    ) -> None:
        self._splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
            separators=[
                "\n\n",
                "\n",
                ". ",
                "? ",
                "! ",
                " ",
                "",
            ],
        )

    def split(
        self,
        text: str,
    ) -> list[str]:
        """
        Split text into chunks.
        """

        return self._splitter.split_text(text)