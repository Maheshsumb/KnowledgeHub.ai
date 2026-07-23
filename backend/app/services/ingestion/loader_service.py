from app.schemas.parsed_document import ParsedDocument
from app.services.ingestion.loader_factory import LoaderFactory
from app.services.ingestion.normalizer import DocumentNormalizer


class DocumentLoaderService:

    async def load(self, file_path: str) -> ParsedDocument:

        loader = LoaderFactory.get_loader(file_path)

        documents = loader.load()

        return DocumentNormalizer.normalize(documents)