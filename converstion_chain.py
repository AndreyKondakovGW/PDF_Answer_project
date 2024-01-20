from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI
from langchain import HuggingFaceHub

import os
OPEN_AI_API_KEY = os.environ['OPENAI_SECRET']
OPEN_AI_API_KEY = os.environ['OPENAI_SECRET']


def get_conversation_chain(vectorstore, model_name = 'openai'):
    if vectorstore is None:
        print('No vectorstore found')
        return None
    if model_name == 'openai':
        llm = ChatOpenAI(openai_api_key=OPEN_AI_API_KEY, temperature=0)
    elif model_name == 'flan':
        llm = HuggingFaceHub(repo_id="google/flan-t5-xxl", model_kwargs= {"temperature":0.1, "max_length":512})
    else:
        print(f'Model with name {model_name} not found')
        return None
    memory = ConversationBufferMemory(
        memory_key='chat_history', return_messages=True)
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(),
        memory=memory,
        verbose=True
    )
    return conversation_chain