import os
import sys
import smtplib
import time
from flask import Flask, request, jsonify, render_template
from langchain_community.document_loaders import TextLoader
from langchain_openai import OpenAIEmbeddings, OpenAI
from langchain.indexes import VectorstoreIndexCreator
from dotenv import load_dotenv
from langchain_community.chat_models import ChatOpenAI

# Load environment variables
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("Please set the OPENAI_API_KEY environment variable.")

# Initialize the loader, embeddings, and index
loader = TextLoader('conversations.txt')
loader2 = TextLoader('dataset_prompts_chosen.txt')
embedding = OpenAIEmbeddings(openai_api_key=api_key)
index = VectorstoreIndexCreator(embedding=embedding).from_loaders([loader, loader2])

app = Flask(__name__)

# Room names and corresponding moderator emails
rooms = {
    "MindMate Room 1": "quadrasmack@gmail.com",
    "MindMate Room 2": "quadrasmack@gmail.com",
    "MindMate Room 3": "quadrasmack@gmail.com",
    "MindMate Room 4": "quadrasmack@gmail.com",
    "MindMate Room 5": "quadrasmack@gmail.com"
}

current_room_index = 0

def get_room_and_moderator():
    global current_room_index
    room_names = list(rooms.keys())
    room_name = room_names[current_room_index]
    moderator_email = rooms[room_name]
    jitsi_url = f"https://meet.jit.si/{room_name.replace(' ', '')}"
    current_room_index = (current_room_index + 1) % len(room_names)
    return jitsi_url, moderator_email, room_name

def send_email(meeting_url, moderator_email, room_name):
    sender_email = "warp2899@gmail.com"
    password = "peju voio adnu kbhn"  # Replace with your app password or correct credentials
    message = f"Subject: Jitsi Meeting Request\n\nA user requests a conversation in {room_name}.\n\nJoin the meeting: {meeting_url}"
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, moderator_email, message)

@app.route("/")
def home():
    return render_template("opening.html")

@app.route("/chat")
def chat():
    return render_template("chat.html")

@app.route("/query", methods=["POST"])
def query():
    query_text = request.form["query"]
    response = query_index(query_text)
    return jsonify({"response": response})

@app.route('/call')
def call():
    meeting_url, moderator_email, room_name = get_room_and_moderator()
    send_email(meeting_url, moderator_email, room_name) 
    return jsonify({"meeting_url": meeting_url})

if __name__ == "__main__":
    app.run(debug=True)
