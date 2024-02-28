from langchain.vectorstores import FAISS
from langchain.llms import GooglePalm

from langchain.document_loaders.csv_loader import CSVLoader
from langchain.embeddings import GooglePalmEmbeddings
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
import os


# Get api google api key from the .env
from dotenv import load_dotenv
load_dotenv() 

# Create Google Palm LLM model instance
llm = GooglePalm()

# # Initialize embeddings using the GooglePalmEmbeddings
embeddings = GooglePalmEmbeddings()

# vector database file path
vectordb_file_path = "faiss_index"

# create vector database based on our csv file
def create_vector_db():
    loader = CSVLoader(file_path='epassport-faq-updated.csv', source_column="question")
    data = loader.load()

    # Create a FAISS instance for vector database from 'data'
    vectordb = FAISS.from_documents(documents=data,
                                    embedding=embeddings)

    # Save vector database locally
    vectordb.save_local(vectordb_file_path)


def get_qa_chain():
    # Load the vector database from the local folder
    vectordb = FAISS.load_local(vectordb_file_path, embeddings)

    # Create a retriever for querying the vector database
    retriever = vectordb.as_retriever(score_threshold=0.7)

    prompt_template = """Given the following context and a question, generate an answer based on this context only.
    In the answer try to provide as much text as possible from "response" section in the source document context only.
    If the answer is not found in the context, kindly state "This is not in my knowledgebase" Don't try to make up an answer.

    CONTEXT: {context}

    QUESTION: {question}"""

    PROMPT = PromptTemplate(
        template=prompt_template, input_variables=["context", "question"]
    )

    chain = RetrievalQA.from_chain_type(llm=llm,
                                        chain_type="stuff",
                                        retriever=retriever,
                                        input_key="query",
                                        return_source_documents=True,
                                        chain_type_kwargs={"prompt": PROMPT})

    return chain