import streamlit as st
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings, HuggingFaceInstructEmbeddings
from langchain.vectorstores import FAISS
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI
from htmlTemplates import bot_template, user_template, css
from langchain.llms import HuggingFaceHub
from InstructorEmbedding import INSTRUCTOR

API_KEY = open("NO_SYNC/apikey.txt", 'r').read().strip("\n")
API_KEY_HF = open("NO_SYNC/apikeyHF.txt", 'r').read().strip("\n")


def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text


def get_text_chunks(text):
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    chunks = text_splitter.split_text(text)
    return chunks


def get_vectorstore(text_chunks):
    embeddings = OpenAIEmbeddings(openai_api_key=API_KEY)
    #embeddings = HuggingFaceInstructEmbeddings(model_name="hkunlp/instructor-base")
    vectorstore = FAISS.from_texts(texts=text_chunks, embedding=embeddings)
    return vectorstore


def get_conversation_chain(vectorstore):
    llm = ChatOpenAI(openai_api_key=API_KEY, model="gpt-3.5-turbo")
    #llm = HuggingFaceHub(huggingfacehub_api_token=API_KEY_HF, repo_id="google/flan-t5-xxl",
    #                    model_kwargs={"temprature": 0.5, "max_length": 500})
    memory = ConversationBufferMemory(
        memory_key='chat_history', return_messages=True)
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(),
        memory=memory
    )
    return conversation_chain


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
    st.set_page_config(page_title="Chat with multiple pdfs",
                       page_icon=":books:")
    st.write(css, unsafe_allow_html=True)

    if 'conversation' not in st.session_state:
        st.session_state.conversation = None

    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = None

    st.header("Chat with multiple pdfs :books:")
    user_question = st.text_input("Ask questions avout the pdfs")
    if user_question:
        handle_userinput(user_question)

    with st.sidebar:
        st.subheader("Your PDFs")
        pdf_docs = st.file_uploader(
            "Upload your PDFs", accept_multiple_files=True)
        if st.button("Process"):
            with st.spinner("Processing ..."):
                # get the text from the pdfs
                raw_text = get_pdf_text(pdf_docs)
                # st.write(raw_text)

                # get the text chunks
                text_chunks = get_text_chunks(raw_text)
                # st.write(text_chunks)

                # create vectore store
                vectorstore = get_vectorstore(text_chunks)

                # Create conversation chain
                st.session_state.conversation = get_conversation_chain(
                    vectorstore)


if __name__ == '__main__':
    main()
