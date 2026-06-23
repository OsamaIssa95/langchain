from docling.datamodel.pipeline_options import (PdfPipelineOptions, TableStructureOptions, TesseractCliOcrOptions)
from langchain_community.document_loaders.parsers import PyPDFParser, TesseractBlobParser
from langchain_community.document_loaders.parsers.images import LLMImageBlobParser
from docling.document_converter import DocumentConverter, PdfFormatOption
from langchain_community.document_loaders.generic import GenericLoader
from langchain_community.document_loaders import FileSystemBlobLoader
from docling.document_converter import DocumentConverter
from docling.datamodel.base_models import InputFormat
from docling_core.types.doc.base import ImageRefMode
from langchain_pymupdf4llm import PyMuPDF4LLMParser
from langchain_core.documents import Document
from langchain_ollama.llms import OllamaLLM
from langchain_ollama import ChatOllama
from pathlib import Path
from ollama import embed
import pymupdf4llm
import base64
import time
import re



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


def pdfloader(path: str, exclude: list [str]) -> list[Document]:
    # This function loads a PDF file from the given path and returns a list of Document objects.
    # Args:
    #    path: The path to the PDF file.
    # Returns:
    #     A list of Document objects.
    #define the LLM model:
    vlm_model = ChatOllama(model="gemma3", temperature=0)
    #initialize image parser:
    vlm_image_parser = LLMImageBlobParser(model=vlm_model, prompt="Describe the content of this image:")

    loader = GenericLoader(   
                            blob_loader=FileSystemBlobLoader(
                                                                path=path,
                                                                glob="*.pdf",
                                                                exclude=exclude,
                                                            ),
                            blob_parser= PyMuPDF4LLMParser(
                                                            mode="single",                                                            
                                                            images_parser=vlm_image_parser,
                                                            extract_images=True
                                                          ),
                        )
    docs = loader.load()
    return docs



            
"""
#docling
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
#with (output_dir / f"{doc_filename}.txt").open("w", encoding="utf-8") as fp:
#    fp.write(conv_result.document.export_to_markdown(image_mode= ImageRefMode.EMBEDDED))
result_to_MD = conv_result.document.export_to_markdown(image_mode= ImageRefMode.EMBEDDED)

"""

def ocr_base64_from_md(result_to_MD, llm):
    
    base64_pattern = r'data:image/.+;base64,([A-Za-z0-9+/=]+)'
    matches = re.findall(base64_pattern, result_to_MD)

    #llm = OllamaLLM(model="gemma3")

    results = []
    for b64_string in matches:
        img_data = base64.b64decode(b64_string)
        llm_with_image_context = llm.bind(images=[img_data])
        # image = Image.open(io.BytesIO(img_data))
        # text = pytesseract.image_to_string(image)
        text = llm_with_image_context.invoke(input="Describe in detail the content of this image:")
        results.append(text)
    return results




def main():
    # laoding pdf using langchain func
    docs = pdfloader("static/PDF/", exclude=["im.pdf", "CV.pdf", "scan.pdf", "Motivation letter.pdf"])
    with open( encoding= "utf-8", file="out3.txt", mode= "w") as f:
        f.write(docs[0].page_content) 
    #try text
    """  
    llm = OllamaLLM(model="gemma3")
    start_time = time.time()
    md_text = pymupdf4llm.to_markdown("./static/PDF/2.pdf", embed_images=True)
    end_time = time.time() - start_time
    with open( encoding= "utf-8", file="out.txt", mode= "w") as f:
        f.write( ocr_base64_from_md(md_text, llm)[1])
        f.write("------------------------------------------")
        f.write( md_text)
    # Overwrites existing file or creates a new one
    #pathlib.Path("output.md").write_bytes(md_text.encode())
    print(end_time)
    """
    """
    converter = DocumentConverter()
    doc = converter.convert(docs).document
    print(doc.export_to_markdown()) 
    blob_parser=PyPDFParser(
            mode="single",
            pages_delimiter="--------end--------",
            images_inner_format="markdown-img",
            images_parser= TesseractBlobParser(),
            extraction_mode="layout",
            ), 
    """
if __name__ == "__main__":
    main()