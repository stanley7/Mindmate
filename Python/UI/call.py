from flask import Flask, jsonify, render_template
import smtplib, time

app = Flask(__name__)

# Room names and corresponding moderator emails
rooms = {
    "MindMate Room 1": "quadrasmack@gmail.com",
    "MindMate Room 2": "quadrasmack@gmail.com",
    "MindMate Room 3": "quadrasmack@gmail.com",
    "MindMate Room 4": "quadrasmack@gmail.com",
    "MindMate Room 5": "quadrasmack@gmail.com"
}

# Counter to keep track of the current room
current_room_index = 0

# Function to select the next room and corresponding moderator in round-robin fashion
def get_room_and_moderator():
    global current_room_index
    room_names = list(rooms.keys())
    
    # Select the next room in the sequence
    room_name = room_names[current_room_index]
    moderator_email = rooms[room_name]
    
    # Generate the Jitsi meeting URL
    jitsi_url = f"https://meet.jit.si/{room_name.replace(' ', '')}"
    
    # Update the index for the next call
    current_room_index = (current_room_index + 1) % len(room_names)
    
    return jitsi_url, moderator_email, room_name

# Function to send an email to the moderator with a customized message
def send_email(meeting_url, moderator_email, room_name):
    sender_email = "warp2899@gmail.com"
    password = "peju voio adnu kbhn"  # App password or correct credentials
    
    message = f"Subject: Jitsi Meeting Request\n\nA user requests a conversation in {room_name}.\n\nJoin the meeting: {meeting_url}"
    
    # Connect to the SMTP server and send the email
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, moderator_email, message)

# Route to handle the call button action and generate Jitsi URL
@app.route('/call')
def call():
    meeting_url, moderator_email, room_name = get_room_and_moderator()  # Get the room and moderator in round-robin order
    send_email(meeting_url, moderator_email, room_name)  # Send email to the correct moderator
    
    # Adding a delay to ensure the moderator has time to join
    time.sleep(10)  # 10-second delay to give the moderator time to join first
    
    return jsonify({"meeting_url": meeting_url})

# Route to render the UI
@app.route('/')
def index():
    return render_template('try.html')

if __name__ == '__main__':
    app.run(debug=True)
