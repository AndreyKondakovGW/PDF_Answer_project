from langchain_ollama.llms import OllamaLLM
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain.chains import LLMChain
from langchain_core.prompts import PromptTemplate

class LangchainModel:
    def __init__(self, retriver=None):
        #options: mistral:latest llama3.1:8b
        self.llm = OllamaLLM(model="mistral:latest")
        self.memory = ConversationBufferMemory(
            memory_key='chat_history', return_messages=True)
        if retriver is None:
            template = """You are a nice chatbot having a conversation with a human.

            Previous conversation:
            {chat_history}

            New human question: {question}
            Response:"""
            prompt = PromptTemplate.from_template(template)
            self.conversation_chain = LLMChain(
                llm=self.llm,
                verbose=False,
                memory=self.memory,
                prompt=prompt
            )
        else:
            self.conversation_chain = ConversationalRetrievalChain.from_llm(
                llm=self.llm,
                retriever=retriver,
                memory=self.memory,
                verbose=False
            )

    def change_retriver(self, retriver):
        self.conversation_chain = ConversationalRetrievalChain.from_llm(
            llm=self.llm,
            retriever=retriver,
            memory=self.memory,
            verbose=False
        )
    def ask(self, question):
        return self.conversation_chain.invoke({'question': question})