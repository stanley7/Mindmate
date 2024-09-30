from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.llms import ollama
import os
import sys  # Import sys to access command-line arguments
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set Langchain tracing and API key environment variables
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")

## Prompt Template
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful assistant. Please respond to the user queries"),
        ("user", "Question:{question}")
    ]
)

# ollama Llama2 LLM 
llm = ollama.Ollama(model="llama2")
output_parser = StrOutputParser()

# Load the dataset from conversations.txt
def load_conversations(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file if line.strip()]  # Read and strip lines

# Function to check if the question is in the dataset
def is_question_in_dataset(question, dataset):
    return question in dataset

# Function to process the question from the command line
def ask_question_from_cli():
    if len(sys.argv) < 2:
        print("Please provide a question as an argument.")
        sys.exit(1)

    # Get the question from the command-line argument
    question = sys.argv[1]
    
    # Load the dataset
    dataset = load_conversations('C:\\Users\\stanl\\Downloads\\PM - LLM\\conversations.txt')

    # Check if the question is in the dataset
    if is_question_in_dataset(question, dataset):
        response = "Your answer is found in the dataset."  # You can customize this response as needed
    else:
        # Replace the question in the prompt and invoke the LLM
        chain = prompt | llm | output_parser
        response = chain.invoke({"question": question})

    # Display the response
    print(f"Response: {response}")

if __name__ == "__main__":
    ask_question_from_cli()
