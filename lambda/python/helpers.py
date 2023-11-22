from nltk.tokenize import sent_tokenize
from nltk.util import ngrams
from typing import List
import pypdf
from io import StringIO, BytesIO


def process_text(text: str, n: int) -> List[str]:
    """Simple text processing that converts source material into strings with n sentences (documents).

    Args:
        text (str): The text you wish to process
        n (int): The size of the ngrams

    Returns:
        List[str]: A list of strings with n sentences
    """
    # replace all white space with a single space
    text = " ".join(text.split())
    text = text.replace("_", " ")  # Underscores are used as a formatting intidicator in Gutenberg txt files
    sentences: List[str] = sent_tokenize(text)

    if n > len(sentences):
        n = len(sentences)

    # return a list of string with n sentences
    return ['. '.join(gram) for gram in ngrams(sentences, n)]


def index_file(file_to_index_bytes, filename: str, marqo_client, index):
    # To read file as bytes:
    # bytes_data = file_to_index.getvalue()  -----  # this gets the bytes data from the file
    pdf_reader = pypdf.PdfReader(BytesIO(file_to_index_bytes))
    content = ""
    # Loop through all pages and extract text
    for page_num in range(len(pdf_reader.pages)):
        page_obj = pdf_reader.pages[page_num]
        content += page_obj.extract_text()
    # convert the source material into a set of documents that are groups of x sentences
    # you can adjust n to see how it changes the outcomes
    documents = process_text(content, 6)

    print(content)
    if not documents:
        return

    marqo_client.index(index).add_documents(
        [
            # by providing our own id for each entry we can track down
            # the location in the origin material if desired
            {'Title': filename, 'Content': text, '_id': f"{filename}_{idx}"} for idx, text in
            enumerate(documents)
        ],
        tensor_fields=["Title", "Content"],
        client_batch_size=64
    )


def print_content(content_bytes):
    pdf_reader = pypdf.PdfReader(BytesIO(content_bytes))
    content = ""

    # Loop through all pages and extract text
    for page_num in range(len(pdf_reader.pages)):
        page_obj = pdf_reader.pages[page_num]
        content += page_obj.extract_text()

    print(content)
