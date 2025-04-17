from flask import Flask, request, jsonify
import logging

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)

@app.route('/webhook', methods=['POST'])
def chatbot_webhook():
    try:
        # Ensure request is JSON
        if not request.is_json:
            logging.error("Request is not JSON")
            return jsonify({"error": "Invalid content type. Expected application/json."}), 400
        
        data = request.get_json(force=True)
        logging.info(f"Received data: {data}")
        
        # Check for required keys
        required_keys = ['event_name', 'user_id', 'message']
        for key in required_keys:
            if key not in data:
                logging.error(f"Missing key: {key}")
                return jsonify({"error": f"Missing key: {key}"}), 400

        # Optional: Process the webhook data here
        response_message = f"Webhook received from user {data['user_id']} with event {data['event_name']}."

        return jsonify({
            "success": True,
            "message": response_message
        }), 200

    except Exception as e:
        logging.exception("An unexpected error occurred")
        return jsonify({"error": "Internal Server Error", "details": str(e)}), 500

@app.route('/', methods=['GET'])
def index():
    return "ChatBot Webhook API is up and running!", 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)
