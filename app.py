import streamlit as st
from load_files import get_model_fromfiles
from htmlTemplates import css, bot_template, user_template

def handle_userinput(user_question):
    response = st.session_state.conversation({'question': user_question})
    st.session_state.chat_history = response['chat_history']

    for i, message in enumerate(st.session_state.chat_history):
        if i % 2 == 0:
            st.write(user_template.replace(
                "{{MSG}}", message.content), unsafe_allow_html=True)
        else:
            st.write(bot_template.replace(
                "{{MSG}}", message.content), unsafe_allow_html=True)
def main():
    st.set_page_config(page_title="Chat with multiple files",
                       page_icon=":books:")
    st.write(css, unsafe_allow_html=True)
    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = None

    st.header("Chat with multiple Files :books:")
    user_question = st.text_input("Ask a question about your documents:")
    if user_question:
        handle_userinput(user_question)

    with st.sidebar:
        st.subheader("Select your models")
        st.write("Select the model you want to use for the vectorstore and the conversation chain")
        vectormodel_name = st.selectbox("Vectorstore model", ["openai", "instructor-base"])
        conversation_model_name = st.selectbox("Conversation model", ["openai", "flan"])
        st.subheader("Your documents")
        pdf_docs = st.file_uploader(
            "Upload your Files here and click on 'Process'", accept_multiple_files=True)
        #input for site url
        url = st.text_input("Enter the site url here:")
        if st.button("Process"):
            with st.spinner("Processing"):
                st.session_state.conversation = get_model_fromfiles(pdf_docs, vectormodel_name, conversation_model_name)


if __name__ == '__main__':
    main()
