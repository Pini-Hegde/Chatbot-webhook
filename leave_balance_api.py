from flask import Flask, request, jsonify
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

@app.route('/webhook', methods=['GET', 'POST'])
def chatbot_webhook():
    if request.method == 'GET':
        # Handle challenge verification
        challenge = request.args.get('challenge')
        if challenge:
            logging.info(f"Challenge received: {challenge}")
            return challenge, 200  # Respond with raw challenge string
        else:
            return "No challenge found", 400

    if request.method == 'POST':
        try:
            if not request.is_json:
                return jsonify({"error": "Invalid content type. Expected application/json."}), 400

            data = request.get_json(force=True)
            logging.info(f"Received data: {data}")

            # Check required fields
            required_keys = ['event_name', 'user_id', 'message']
            for key in required_keys:
                if key not in data:
                    return jsonify({"error": f"Missing key: {key}"}), 400

            # Do your processing here
            response_message = f"Received event '{data['event_name']}' from user {data['user_id']}."

            return jsonify({
                "success": True,
                "message": response_message
            }), 200

        except Exception as e:
            logging.exception("Unexpected error:")
            return jsonify({"error": "Internal Server Error", "details": str(e)}), 500

@app.route('/', methods=['GET'])
def index():
    return "ChatBot Webhook API is live!", 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)
