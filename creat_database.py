import os.path
import re
import shutil

from langchain_community.document_loaders import DirectoryLoader
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

from Key import API_KEY

DATA_PATH = "Data"
CHROMA_PATH = 'chroma'

def load_documents():
    loader = DirectoryLoader(DATA_PATH, glob = "*.txt")
    documents = loader.load()
    for doc in documents:
        doc.page_content = re.sub(r'\[\d+\]', '', doc.page_content)
    return documents

def split_text(documents):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=500,
        length_function=len,
        add_start_index=True,
    )

    chunks = text_splitter.split_documents(documents)
    document = chunks[10]
    print(document.page_content)
    print(document.metadata)
    return chunks


def save_to_chroma(chunks):
    if os.path.exists(CHROMA_PATH):
        shutil.rmtree(CHROMA_PATH)

    db = Chroma.from_documents(
        chunks,
        OpenAIEmbeddings(api_key = API_KEY),
        persist_directory=CHROMA_PATH
    )
    print(f"Saved {len(chunks)} documents to {CHROMA_PATH}")

if __name__ == "__main__":
    documents = load_documents()
    chunks = split_text(documents)
    save_to_chroma(chunks)