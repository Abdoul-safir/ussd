from flask import Flask, request
from serverless_wsgi import handle_request

app = Flask(__name__)

@app.route("/event", methods=['POST'])
def event():
    # Read the event data from Africa's Talking
    event_data = request.get_json()

    # Extract event details
    event_type = event_data.get("type")  # e.g., "SessionStart", "SessionEnd"
    session_id = event_data.get("sessionId")
    phone_number = event_data.get("phoneNumber")

    # Log the event (you can customize this logic)
    print(f"Event Type: {event_type}")
    print(f"Session ID: {session_id}")
    print(f"Phone Number: {phone_number}")

    # Respond to Africa's Talking (optional)
    return "Event received", 200

def handler(event, context):
    return handle_request(app, event, context)
