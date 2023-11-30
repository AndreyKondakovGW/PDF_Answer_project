from pdf_to_text import pdf_to_text
from text_splitter import split_text
from vectorstore import create_vectorstore, get_vectorstore
from converstion_chain import get_conversation_chain
import os

def init():
    pdf_file = "./txt_examples/SS13exampleEN.txt"
    filename = os.path.basename(pdf_file).split('.')[0]
    filetype = os.path.basename(pdf_file).split('.')[1]
    vectorstore = get_vectorstore(filename)
    if vectorstore is None:
        if filetype == 'pdf':
            print('Parsing pdf...')
            raw_text = pdf_to_text(pdf_file)
        if filetype == 'txt':
            print('Parsing txt...')
            with open(pdf_file, 'r', encoding="utf-8") as file:
                raw_text = file.read()
        print('Splitting text...')
        text_chunks = split_text(raw_text)
        print('Creating vectorstore...')
        vectorstore = create_vectorstore(text_chunks, filename)
    
    conversation = get_conversation_chain(vectorstore)
    return conversation


if __name__ == "__main__":
    user_question = "How can I not be shocken during hacking."
    conversation = init()
    print(conversation({'question': user_question}))