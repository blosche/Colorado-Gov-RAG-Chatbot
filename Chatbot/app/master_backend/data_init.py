import decimal
import os

import psycopg2
from langchain_community.document_loaders.text import TextLoader
from langchain.text_splitter import CharacterTextSplitter, RecursiveCharacterTextSplitter
from store import create_retriever, create_retriever_unemployment
from langchain.schema import Document


class DataIngestionManager:
    def __init__(self):
        db_user = os.getenv("DB_USER", "admin")
        db_password = os.getenv("DB_PASSWORD", "admin")
        db_host = os.getenv("DB_HOST", "127.0.0.1")
        db_port = os.getenv("DB_PORT", "5432")
        db_name = os.getenv("DB_NAME", "vectordb")

       
        self.conn_string = f"host={db_host} port={db_port} dbname={db_name} user={db_user} password={db_password}"

        
        self.vector_connection_string = f"postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"

        self.conn = None
        self.cursor = None
        self.retriever = create_retriever(self.vector_connection_string)
        self.retriever_unemployment = create_retriever_unemployment(self.vector_connection_string)

    def connect(self):
        if not self.conn:
            self.conn = psycopg2.connect(self.conn_string)
            self.cursor = self.conn.cursor()

    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()

    def ingest_vector_data(self):
        loader = TextLoader("./data/CO_Services.txt")
        docs = loader.load()

        raw_text = docs[0].page_content
        sections = raw_text.split(";")


        sections = [section.strip() for section in sections if section.strip()]


        chunks = [Document(page_content=section) for section in sections]
        
        # print("Type of docs: ", type(docs))
        # print("DOCS: \n\n", docs, "\n\n")
        # print("Type of Chunks:", type(chunks))
        # print("CHUNKS: \n\n", chunks[0])

        self.retriever.add_documents(chunks)
        
        # Unemployment load
        docs2 = []
        loader = TextLoader("./data/Unemployment.txt")
        docs2.extend(loader.load())
        self.retriever_unemployment.add_documents(docs2)



if __name__ == "__main__":
    data_manager = DataIngestionManager()
    data_manager.ingest_vector_data()

