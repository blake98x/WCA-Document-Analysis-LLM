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
from langchain.llms import OpenAI
from langchain.callbacks import get_openai_callback
from langchain.chat_models import ChatOpenAI

import json
#%%

def import_documents(url, downloaded_documents):
    # Create the directory to store the documents found
    if not os.path.exists('Documents'):
        os.makedirs('Documents')

    # Send a GET request to the URL
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    pdf_links = soup.find_all('a', href=lambda href: (href and href.endswith('.pdf')))

    # Download each PDF file
    for link in pdf_links:
        pdf_url = link['href']
        pdf_filename = pdf_url.split('/')[-1]
        if pdf_filename not in downloaded_documents:
            pdf_path = os.path.join('Documents', pdf_filename)
            pdf_url = urllib.parse.urljoin(url, pdf_url.replace(' ', '%20'))
            print("Downloading:", pdf_filename)
            with open(pdf_path, 'wb') as f:
                f.write(requests.get(pdf_url).content)

def create_page():
    st.set_page_config(page_title = "Ask a Question about a WCA Document!")
    st.header("What do you want to know about the WCA?")

def read_pdfs(downloaded_documents):

    for doc in downloaded_documents:
        pdf_reader = PdfReader('Documents/' + doc)
        text = ''
        for page in pdf_reader.pages:
            text += page.extract_text()
         
        # Split into chunks
        text_splitter = CharacterTextSplitter(
            separator = "\n",
            chunk_size = 1000,
            chunk_overlap = 200,
            length_function = len
        )

        chunks = text_splitter.split_text(text)

        embeddings = OpenAIEmbeddings()

        knowledge_base = FAISS.from_texts(chunks, embeddings)

        user_question = st.text_input("Ask a question about the WCA!")

        if user_question:
            docs = knowledge_base.similarity_search(user_question)

            llm = ChatOpenAI(model="gpt-4-turbo-preview")

            # Load the QA chain
            chain = load_qa_chain(llm, chain_type='stuff')

            # Perform question answering
            response = chain.run(input_documents=docs, question=user_question)

            st.write(response)
        



def main():

    load_dotenv()

    # Set URLs of WCA's documents page and Regulations/Guidelines
    urls = [
        'https://www.worldcubeassociation.org/documents',
        'https://www.worldcubeassociation.org/regulations/',
        'https://www.worldcubeassociation.org/regulations/guidelines.html'
    ]

    downloaded_documents = os.listdir('Documents')

    for url in urls:
        import_documents(url, downloaded_documents)

    print('\n 🎉 All Documents have been downloaded! 🎉')

    create_page()

    read_pdfs(downloaded_documents[0:1])




if __name__ == '__main__':
    main()



# %%

'''
TODO:

- Work out loading speed
- Test on wider span of documents


'''