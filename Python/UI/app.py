import os
from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv

# Importing model functions
from models.model_a import model_a_response
from models.model_b import model_b_response
from models.model_c import model_c_response

# Load environment variables
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("Please set the OPENAI_API_KEY environment variable.")

app = Flask(_name_)

@app.route("/")
def home():
    return render_template("opening.html")

@app.route("/chat")
def chat():
    return render_template("chat.html")

@app.route("/query", methods=["POST"])
def query():
    query_text = request.form["query"]  # Get the query text from the form
    selected_model = request.form.get("model")  # Get the selected model from the form
    
    try:
        if selected_model == "model_a":
            response_text = model_a_response(query_text)
        elif selected_model == "model_b":
            response_text = model_b_response(query_text)
        elif selected_model == "model_c":
            response_text = model_c_response(query_text)
        else:
            response_text = "Invalid model selected."
        
        return jsonify({"response": response_text})
    except Exception as e:
        return jsonify({"response": f"An error occurred: {e}"})

if _name_ == "_main_":
    app.run(debug=True, port=5001)
[11:24 PM, 9/30/2024] Swathi Uni-Potsdam: meeting.py
import smtplib
from config import SENDER_EMAIL, SENDER_PASSWORD, ROOMS  # Import shared configurations

current_room_index = 0

def get_room_and_moderator():
    global current_room_index
    room_names = list(ROOMS.keys())
    room_name = room_names[current_room_index]
    moderator_email = ROOMS[room_name]
    jitsi_url = f"https://meet.jit.si/{room_name.replace(' ', '')}"
    current_room_index = (current_room_index + 1) % len(room_names)
    return jitsi_url, moderator_email, room_name

def send_email(meeting_url, moderator_email, room_name):
    message = f"Subject: Jitsi Meeting Request\n\nA user requests a conversation in {room_name}.\n\nJoin the meeting: {meeting_url}"
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.sendmail(SENDER_EMAIL, moderator_email, message)
