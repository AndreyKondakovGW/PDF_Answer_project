from pdf_to_text import pdf_to_text
from text_splitter import split_text
from vectorstore import create_vectorstore, get_vectorstore
from converstion_chain import get_conversation_chain
import os
from io import StringIO

def get_model_fromfiles(files = []):
    if files != []:
        vectorstore = load_files(files)
        if vectorstore is None:
            vectorstore = get_vectorstore('vectorstore')
    else:
        vectorstore = get_vectorstore('vectorstore')
    
    conversation = get_conversation_chain(vectorstore)
    return conversation

def load_files(files = []):
    files_text = ""
    for file in files:
        files_text += get_file_text(file)
    if files_text == "":
        return None
    print('Splitting text...')
    text_chunks = split_text(files_text)
    print('Creating vectorstore...')
    vectorstore = create_vectorstore(text_chunks, 'vectorstore')
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
        