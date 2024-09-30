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
