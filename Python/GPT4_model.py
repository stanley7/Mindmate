import sys
import os
from datasets import load_dataset
from dotenv import load_dotenv
import openai
from langchain.document_loaders import TextLoader
from langchain.indexes import VectorstoreIndexCreator
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.schema import Document

# Load environment variables
load_dotenv()

# Set the API key for OpenAI
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError("Please set the OPENAI_API_KEY environment variable.")
openai.api_key = api_key

# Load the dataset and prepare the file path
ds = load_dataset("Amod/mental_health_counseling_conversations")

file_path = '/content/conversations.txt'

# Ensure the conversations file exists and contains data
if not os.path.exists(file_path):
    with open(file_path, 'w', encoding='utf-8') as f:
        for record in ds['train']:
            input_text = record.get('Context', 'No context')
            response_text = record.get('Response', 'No response')
            text_content = f"User: {input_text}\nAssistant: {response_text}\n\n"
            f.write(text_content)
    print(f"Saved all conversations to {file_path}")
else:
    print(f"Using existing file at {file_path}")

# Load documents with error handling for encoding issues
documents = []
try:
    with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
        for line in f:
            documents.append(Document(page_content=line.strip()))
except Exception as e:
    raise RuntimeError(f"Error loading {file_path}: {e}")

# Instantiate the OpenAI embeddings model
embeddings = OpenAIEmbeddings()

# Create the index with the embeddings model
index = VectorstoreIndexCreator(embedding=embeddings).from_documents(documents)

# Get a query from the user
query = input("Please provide a query: ")

# Instantiate the OpenAI language model using ChatOpenAI
openai_llm = ChatOpenAI(temperature=0.7, model_name="gpt-4")

# Query the index with the provided query
print(index.query(query, llm=openai_llm))
