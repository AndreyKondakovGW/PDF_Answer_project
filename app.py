import streamlit as st
from htmlTemplates import css, bot_template, user_template
from src.model import LangchainModel
from src.retriver import Retriver
import os

def main():
    st.set_page_config(page_title="Chat with multiple files",
                       page_icon=":books:")
    st.write(css, unsafe_allow_html=True)

    if "conversation" not in st.session_state:
        st.session_state.conversation = LangchainModel()
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = None
    if "retriver" not in st.session_state:
        st.session_state.retriver = Retriver()

    st.header("Chat with multiple Files :books:")
    user_question = st.text_input("Ask a question about your documents:")
    if user_question:
        handle_userinput(user_question)

    with st.sidebar:
        st.subheader("Select your models")
        st.subheader("Your documents")
        pdf_docs = st.file_uploader(
            "Upload your Files here and click on 'Process'", accept_multiple_files=False)
        #input for site url
        url = st.text_input("Enter the site url here:")
        if st.button("Process"):
            with st.spinner("Processing"):
                os.makedirs("./tmp")
                temp_file = "./tmp/temp.pdf"
                with open(temp_file, "wb") as file:
                    file.write(pdf_docs.getvalue())
                    file_name = pdf_docs.name
                db = st.session_state.retriver.create_from_file(temp_file, file_name)
                st.session_state.conversation.change_retriver(db)

def handle_userinput(user_question):
    response = st.session_state.conversation.ask(user_question)
    st.session_state.chat_history = response['chat_history']

    for i, message in enumerate(st.session_state.chat_history):
        if i % 2 == 0:
            st.write(user_template.replace(
                "{{MSG}}", message.content), unsafe_allow_html=True)
        else:
            st.write(bot_template.replace(
                "{{MSG}}", message.content), unsafe_allow_html=True)

if __name__ == '__main__':
    main()
