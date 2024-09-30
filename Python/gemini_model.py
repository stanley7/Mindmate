import os
from dotenv import load_dotenv
from langchain.document_loaders import TextLoader
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings 
from langchain.chains import RetrievalQA
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import Document 

# Load environment variables
load_dotenv()

# Set your Google API Key 
GOOGLE_API_KEY = ""

# Initialize the Gemini API model
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=GOOGLE_API_KEY)

# Load your dataset using TextLoader with encoding handling
def load_custom_dataset(file_path):
    try:
        # TextLoader uses default 'utf-8', we will override with error handling for non-UTF-8 characters
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
            data = file.read()
        # Return a list of Document objects, with content in 'page_content'
        return [Document(page_content=data)]
    except Exception as e:
        print(f"Error reading the file: {e}")
        return []

# Embed the dataset using HuggingFace sentence transformers
def create_embeddings(documents):
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")  
    vectorstore = FAISS.from_documents(documents, embeddings)
    return vectorstore

# Set up the QA Chain with Retriever
def setup_qa_chain(vectorstore):
    retriever = vectorstore.as_retriever() 
    qa_chain = RetrievalQA.from_llm(llm, retriever=retriever)  
    return qa_chain

if __name__ == "__main__":
    # Load your dataset
    dataset_path = "/content/conversations.txt"  # Path to your dataset
    documents = load_custom_dataset(dataset_path)

    if not documents:
        print("No documents loaded. Exiting.")
    else:
        # Create embeddings and vectorstore
        vectorstore = create_embeddings(documents)
        qa_chain = setup_qa_chain(vectorstore)
        query = input(" ")  # Replace with your actual query
        try:
            response = qa_chain.run(query)
            print(f"Answer: {response}")
        except Exception as e:
            print(f"An error occurred while querying the dataset: {e}")
