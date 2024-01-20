from pdf_to_text import pdf_to_text
from text_splitter import split_text, split_for_site
from vectorstore import create_vectorstore, get_vectorstore
from converstion_chain import get_conversation_chain
from langchain_community.document_loaders import AsyncChromiumLoader
from langchain_community.document_transformers import BeautifulSoupTransformer
from io import StringIO

def get_model_fromfiles(files = [], url = "", vectormodel_name = "openai", conversation_model_name = 'openai'):
    print(f"Vectorstore model: {vectormodel_name}")
    print(f"Conversation model: {conversation_model_name}")
    vectorstore = None
    if files != []:
        vectorstore = load_files(files, vectormodel_name)
        if vectorstore is None:
            vectorstore = get_vectorstore('vectorstore', vectormodel_name)
    if url != "":
        vectorstore = get_url_text(url, vectormodel_name)    
    conversation = get_conversation_chain(vectorstore, conversation_model_name)
    return conversation

def load_files(files = [], vectormodel_name = "openai"):
    files_text = ""
    for file in files:
        files_text += get_file_text(file)
    if files_text == "":
        return None
    print('Splitting text...')
    text_chunks = split_text(files_text)
    print('Creating vectorstore...')
    vectorstore = create_vectorstore(text_chunks, 'vectorstore', vectormodel_name)
    return vectorstore

def get_url_text(url, vectormodel_name = "openai"):
    loader = AsyncChromiumLoader(url)
    docs = loader.load()
    bs_transformer = BeautifulSoupTransformer()
    docs_transformed = bs_transformer.transform_documents(
        docs, tags_to_extract=["p", "th", "td","li"]
    )
    print("Splitting text...")
    text_chunks = split_for_site(docs_transformed)
    vectorstore = create_vectorstore(text_chunks, 'vectorstore', vectormodel_name)
    return vectorstore

def get_file_text(full_filename):
    filename = full_filename.name.split('.')[0]
    filetype = full_filename.name.split('.')[1]
    raw_text = ""
    if filetype == 'pdf':
        print('Parsing pdf...')
        raw_text += f"File: {filename}\n"
        raw_text += pdf_to_text(full_filename)
    if filetype == 'txt':
        print('Parsing txt...')
        raw_text += f"File: {filename}\n"
        
        stringio=StringIO(full_filename.getvalue().decode('utf-8'))
        raw_text+=stringio.read()
    return raw_text
        