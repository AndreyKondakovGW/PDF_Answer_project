from langchain.text_splitter import CharacterTextSplitter
from langchain.text_splitter import RecursiveCharacterTextSplitter

def split_text(text):
    text_spliteer = CharacterTextSplitter(separator='\n',
                                          chunk_size=512, chunk_overlap=100,
                                          length_function=len)
    chunks = text_spliteer.split_text(text)
    return chunks

def split_for_site(docs):
    splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        chunk_size=512, chunk_overlap=100
    )
    chunks = splitter.split_documents(docs)
    return chunks