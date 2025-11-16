from langchain_core.documents import Document
from langchain_community.document_loaders import FileSystemBlobLoader, PyPDFLoader
from langchain_community.document_loaders.parsers import PyPDFParser, TesseractBlobParser
from langchain_community.document_loaders.generic import GenericLoader
import pymupdf4llm
import pathlib

#document structure
""" documents = [
    Document(
        page_content="Dogs are great companions, known for their loyalty and friendliness.",
        metadata={"source": "mammal-pets-doc"},
    ),
    Document(
        page_content="Cats are independent pets that often enjoy their own space.",
        metadata={"source": "mammal-pets-doc"},
    ),
] """


def pdfloader(path: str) -> list[Document]:
    """ This function loads a PDF file from the given path and returns a list of Document objects.
    Args:
        path: The path to the PDF file.
    Returns:
        A list of Document objects.
    """
    loader = GenericLoader(   
        blob_loader=FileSystemBlobLoader(
            path=path,
            glob="*.pdf",
            ),
        blob_parser=PyPDFParser(
            mode="single",
            pages_delimiter="--------end--------",
            images_inner_format="markdown-img",
            images_parser=TesseractBlobParser,
            extraction_mode="layout",
            ),
    )
    docs = loader.load()
    return docs


docs = pdfloader("static/PDF") 
print(docs[0].page_content)


""" md_text = pymupdf4llm.to_markdown("./static/PDF/CV.pdf")
pathlib.Path("output.md").write_bytes(md_text.encode())
print(md_text) """