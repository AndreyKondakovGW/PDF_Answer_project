from langchain.embeddings import OpenAIEmbeddings, HuggingFaceInstructEmbeddings
from langchain.vectorstores.faiss import FAISS
import os
OPEN_AI_API_KEY = os.environ['OPENAI_SECRET']

DATABASE_PATH = './data'
def get_vectorstore(database_name, vectormodel_name = "openai"):
    path = os.path.join(DATABASE_PATH, database_name)
    if os.path.exists(path):
        if vectormodel_name == 'openai':
            embeddings = OpenAIEmbeddings(openai_api_key=OPEN_AI_API_KEY)
        elif vectormodel_name == 'instructor-base':
            embeddings = HuggingFaceInstructEmbeddings(model_name="hkunlp/instructor-base", model_kwargs={'device': 'cpu'})
        else:
            print(f'Model with name {vectormodel_name} not found')
            return None
        return FAISS.load_local(path, embeddings)
    else:
        return None
    
def create_vectorstore(chunks, database_name, vectormodel_name = "openai"):
    if vectormodel_name == 'openai':
        embeddings = OpenAIEmbeddings(openai_api_key=OPEN_AI_API_KEY)
    elif vectormodel_name == 'instructor-base':
        embeddings = HuggingFaceInstructEmbeddings(model_name="hkunlp/instructor-base", model_kwargs={'device': 'cpu'})
    else:
        print(f'Model with name {vectormodel_name} not found')
        return None
    db = FAISS.from_texts(chunks, embeddings)
    print('DB created')
    db.save_local(os.path.join(DATABASE_PATH, database_name))
    return db