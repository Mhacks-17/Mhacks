from flask import Flask, request, jsonify
from twilio.rest import Client
import os

app = Flask(__name__)

# Twilio setup (for SMS notifications)
account_sid = 'your_twilio_account_sid'
auth_token = 'your_twilio_auth_token'
twilio_phone_number = 'your_twilio_phone_number'
client = Client(account_sid, auth_token)

# Trigger for sending notifications via Magic Loops
@app.route('/send_notification', methods=['POST'])
def send_notification():
    try:
        # Get data from the request (from Magic Loops or another trigger)
        data = request.json
        user_phone_number = data.get('phone_number')
        message_body = data.get('message', 'This is a test notification from Magic Loops.')

        # Sending SMS notification via Twilio
        message = client.messages.create(
            body=message_body,
            from_=twilio_phone_number,
            to=user_phone_number
        )

        return jsonify({"status": "success", "message_sid": message.sid})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Health check endpoint
@app.route('/', methods=['GET'])
def health_check():
    return "Server is running!"

if __name__ == '__main__':
    app.run(debug=True)
