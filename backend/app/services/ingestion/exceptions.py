class UnsupportedDocumentTypeError(Exception):
    """Raised when a document type is not supported."""


class DocumentLoadingError(Exception):
    """Raised when a document cannot be parsed."""