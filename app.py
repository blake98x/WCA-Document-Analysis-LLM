#%%

import requests
from bs4 import BeautifulSoup
import urllib
import os
from dotenv import load_dotenv
from PyPDF2 import PdfReader
import streamlit as st
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain.chat_models import ChatOpenAI

#%%

def import_documents(url, downloaded_documents, folder_name):
    # Create the directory to store the documents
    folder_path = os.path.join('Documents', folder_name)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    # Send a GET request to the URL
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    pdf_links = soup.find_all('a', href=lambda href: (href and href.endswith('.pdf')))

    # Download each unique PDF file
    for link in pdf_links:
        pdf_url = link['href']
        pdf_filename = pdf_url.split('/')[-1]
        if pdf_filename not in downloaded_documents:
            pdf_path = os.path.join(folder_path, pdf_filename)
            pdf_url = urllib.parse.urljoin(url, pdf_url.replace(' ', '%20'))
            print("Downloading:", pdf_filename)
            with open(pdf_path, 'wb') as f:
                f.write(requests.get(pdf_url).content)

def create_page():
    st.set_page_config(page_title="Ask a Question about a WCA Document!")
    st.header("What do you want to know about the WCA?")

def get_pdf_text(folder_name):
    text = ''
    folder_path = os.path.join('Documents', folder_name)
    for doc in os.listdir(folder_path):
        pdf_reader = PdfReader(os.path.join(folder_path, doc))
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text

def get_text_chunks(text):
    # Split into chunks
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    chunks = text_splitter.split_text(text)
    return chunks

def get_vectorstore(chunks):
    embeddings = OpenAIEmbeddings()
    return FAISS.from_texts(chunks, embeddings)

def ask_question(knowledge_base, context_name):
    user_question = st.text_input(f"Ask a question about {context_name}!")
    if user_question:
        docs = knowledge_base.similarity_search(user_question)

        llm = ChatOpenAI()
        chain = load_qa_chain(llm, chain_type='stuff')

        # Perform question answering
        response = chain.run(input_documents=docs, question=user_question)
        st.write(response)

def main():
    load_dotenv()

    # Set URLs of WCA's documents page and Regulations/Guidelines
    urls = {
        "Documents": 'https://www.worldcubeassociation.org/documents',
        "Regulations and Guidelines": 'https://www.worldcubeassociation.org/regulations/full/'
    }

    # Create necessary folders
    downloaded_documents = {
        context: os.listdir(os.path.join('Documents', context)) if os.path.exists(os.path.join('Documents', context)) else []
        for context in urls.keys()
    }

    # Import all relevant documents
    for context, url in urls.items():
        import_documents(url, downloaded_documents[context], context)

    print('\n 🎉 All Documents have been downloaded! 🎉')

    create_page()

    # Add toggle for selecting the context
    context_name = st.selectbox(
        "Choose a context for your question:",
        list(urls.keys())
    )

    # Load the text and create a vectorstore
    raw_text = get_pdf_text(context_name)
    text_chunks = get_text_chunks(raw_text)
    knowledge_base = get_vectorstore(text_chunks)

    ask_question(knowledge_base, context_name)

if __name__ == '__main__':
    main()

# %%
