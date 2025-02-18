from flask import Flask, request, jsonify
import awsgi  # Correct import

app = Flask(__name__)

@app.route("/event", methods=['POST'])
def event():
    try:
        # Read the event data from Africa's Talking
        event_data = request.get_json()

        # Validate JSON data
        if not event_data:
            return jsonify({"error": "Invalid or empty JSON data"}), 400

        # Extract event details
        event_type = event_data.get("type")  # e.g., "SessionStart", "SessionEnd"
        session_id = event_data.get("sessionId")
        phone_number = event_data.get("phoneNumber")

        # Validate required fields
        if not event_type or not session_id or not phone_number:
            return jsonify({"error": "Missing required fields"}), 400

        # Log the event (you can customize this logic)
        print(f"Event Type: {event_type}")
        print(f"Session ID: {session_id}")
        print(f"Phone Number: {phone_number}")

        # Respond to Africa's Talking
        return jsonify({"message": "Event received"}), 200
    except Exception as e:
        # Handle unexpected errors
        print(f"Error: {e}")
        return jsonify({"error": "An error occurred. Please try again later."}), 500

def handler(event, context):
    return awsgi.response(app, event, context)  # Use the correct handler
