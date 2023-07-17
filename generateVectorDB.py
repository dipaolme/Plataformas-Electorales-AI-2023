from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from pathlib import Path
import os

# COLOCAR AQUI LA API KEY DE OPENAI
os.environ['OPENAI_API_KEY'] = ""


def generate_vectorDBs(dir_pdfs):
    """Funcion que genera base de datos de vectores a partir de un pdf
       Colocar el pdf en la carpeta pdfs, si ya existe la bd no la hace nuevamente"""

    for f in os.listdir(dir_pdfs):

        fname = Path(f).stem

        dirName = 'vectorstores'

        if os.path.exists(dirName+'/'+fname):
            continue
        
        loader = PyPDFLoader(dir_pdfs+'/'+f)
        pages = loader.load()

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=2000,
            chunk_overlap=200
        )

        docs = text_splitter.split_documents(pages)

        persist_directory = f'vectorstores/{fname}'

        vectordb = Chroma.from_documents(
            documents=docs,
            embedding=OpenAIEmbeddings(),
            persist_directory = persist_directory
        )

        vectordb.persist()

generate_vectorDBs('pdfs')

