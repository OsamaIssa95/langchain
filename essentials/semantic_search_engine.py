from turtle import mode
from PIL import ImageMode
from docling_core.types.doc.base import ImageRefMode
from langchain_core.documents import Document
from langchain_community.document_loaders import FileSystemBlobLoader
from langchain_community.document_loaders.parsers import PyPDFParser, TesseractBlobParser, language
from langchain_community.document_loaders.generic import GenericLoader
from langchain_pymupdf4llm import PyMuPDF4LLMParser

from langchain_text_splitters import Language
from numpy import single
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


""" def pdfloader(path: str, exclude: list [str]) -> list[Document]:
    #"""#This function loads a PDF file from the given path and returns a list of Document objects.
   # Args:
   #    path: The path to the PDF file.
   # Returns:
   #     A list of Document objects.
"""
    loader = GenericLoader(   
        blob_loader=FileSystemBlobLoader(
            path=path,
            glob="*.pdf",
            exclude=exclude,
            ),
     
        blob_parser= PyMuPDF4LLMParser(
                mode="single",
          ),
    )
    docs = loader.load()
    return docs

docs = pdfloader("static/PDF/", exclude=["im.pdf", "Motivation letter.pdf"])
print(docs[0].page_content)
print("______________________________________________________________________________________________") """
""" docs = pdfloader("static/PDF/im.pdf") ()
print(docs[0].page_content)
print("______________________________________________________________________________________________")

md_text = pymupdf4llm.to_markdown("./static/PDF/im.pdf", pages=[0], write_images=True,extract)
#pathlib.Path("output.md").write_bytes(md_text.encode())
print(md_text) """
""" from docling.document_converter import DocumentConverter
converter = DocumentConverter()
doc = converter.convert(docs).document
print(doc.export_to_markdown()) """
""" blob_parser=PyPDFParser(
            mode="single",
            pages_delimiter="--------end--------",
            images_inner_format="markdown-img",
            images_parser= TesseractBlobParser(),
            extraction_mode="layout",
            ), """
            
import json
import logging
import time
from pathlib import Path

from docling.datamodel.accelerator_options import AcceleratorDevice, AcceleratorOptions

from docling.datamodel.base_models import InputFormat
from docling.datamodel.layout_model_specs import LayoutModelConfig

from docling.datamodel.pipeline_options import (
    PdfPipelineOptions,
    TableStructureOptions,
    TesseractCliOcrOptions,
    LayoutOptions,
    
)
from docling.document_converter import DocumentConverter, PdfFormatOption

data_folder = Path("./static/PDF/")
input_doc_path = data_folder / "im.pdf"
tess_ocr = TesseractCliOcrOptions(
    psm=3,
    lang=["eng"],
    force_full_page_ocr=True, 
)



pipeline_options = PdfPipelineOptions()
pipeline_options.do_ocr = True
# pipeline_options.do_table_structure = True
pipeline_options.generate_picture_images=True,
pipeline_options.do_picture_description=False,
# pipeline_options.enable_remote_services = True,
# pipeline_options.force_full_page_ocr=True
pipeline_options.table_structure_options = TableStructureOptions(
        do_cell_matching=True
)
pipeline_options.ocr_options = TesseractCliOcrOptions(force_full_page_ocr=True, lang=["eng"])

#pipeline_options.accelerator_options = AcceleratorOptions(
#        num_threads=4, device=AcceleratorDevice.AUTO
#)

doc_converter = DocumentConverter(
        format_options={
            InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options)
        }
)
start_time = time.time()
conv_result = doc_converter.convert(input_doc_path)
end_time = time.time() - start_time
print(end_time)

## Export results
output_dir = Path("scratch")
output_dir.mkdir(parents=True, exist_ok=True)
doc_filename = conv_result.input.file.stem

# Export Text format (plain text via Markdown export):
with (output_dir / f"{doc_filename}.txt").open("w", encoding="utf-8") as fp:
    fp.write(conv_result.document.export_to_markdown(image_mode= ImageRefMode.EMBEDDED))