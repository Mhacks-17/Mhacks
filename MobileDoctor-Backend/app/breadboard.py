from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

# Your Breadboard API key (replace with actual key)
BREADBOARD_API_KEY = 'your_breadboard_api_key'

# Endpoint to fetch chat data from Breadboard
BREADBOARD_BASE_URL = 'https://api.breadboard.dev/boards'

# Function to get chats related to medical advice
def get_medical_chats(board_id):
    url = f"{BREADBOARD_BASE_URL}/{board_id}/chat"
    headers = {
        'Authorization': f'Bearer {BREADBOARD_API_KEY}',
        'Content-Type': 'application/json'
    }
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return response.json()  # Assuming the API returns JSON data
    else:
        return {"error": "Failed to fetch data from Breadboard API"}

# Flask route to fetch and return chat data
@app.route('/get_medical_chats', methods=['GET'])
def fetch_medical_chats():
    # Get board_id from the request query parameters
    board_id = request.args.get('board_id')
    
    if not board_id:
        return jsonify({"error": "No board_id provided"}), 400
    
    chat_data = get_medical_chats(board_id)
    return jsonify(chat_data)

if __name__ == '__main__':
    app.run(debug=True)
