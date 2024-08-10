from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OllamaEmbeddings
from langchain.vectorstores.faiss import FAISS
from src.pdf_parser import PDFParser
import os

DATABASE_PATH = './databases'

class Retriver:
    def __init__(self):
        self.text_spliter = CharacterTextSplitter(separator='\n',
                                        chunk_size=1024, chunk_overlap=256,
                                        length_function=len)
        self.embedder = OllamaEmbeddings(model="mxbai-embed-large")

    def create_new_vectorstore(self, vectorstore_name, text_chunks):
        db = FAISS.from_texts(text_chunks, self.embedder)
        db.save_local(os.path.join(DATABASE_PATH, vectorstore_name))
        return db.as_retriever()

    def load_vectorstore(self, vectorstore_name):
        return FAISS.load_local(os.path.join(DATABASE_PATH, vectorstore_name), self.embedder).as_retriever()

    def split_text(self, text):
        chunks = self.text_spliter.split_text(text)
        return chunks
    
    def create_from_file(self, file_path, filename):
        _, file_extension = os.path.splitext(file_path)
        if file_extension == ".pdf":
            parser = PDFParser()
            file_text = parser.parse_file(file_path)
        file_chunks = self.split_text(file_text)
        return self.create_new_vectorstore(filename, file_chunks)
    
    def get_existed_retrivers(self):
        return os.listdir(DATABASE_PATH)


