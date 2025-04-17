from flask import Flask, request, Response, jsonify
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

@app.route('/webhook', methods=['GET', 'POST'])
def chatbot_webhook():
    if request.method == 'GET':
        # Grab the challenge token
        challenge = request.args.get('challenge')
        if challenge:
            logging.info(f"Responding to challenge: {challenge}")
            return Response(challenge, status=200, mimetype='text/plain')
        else:
            return Response("Missing challenge parameter", status=400)

    if request.method == 'POST':
        try:
            if not request.is_json:
                return jsonify({"error": "Expected application/json"}), 400

            data = request.get_json()
            logging.info(f"Received webhook data: {data}")

            # Optional: Check required fields (e.g., event_name, user_id, etc.)
            return jsonify({"success": True}), 200

        except Exception as e:
            logging.exception("Webhook handling error:")
            return jsonify({"error": "Internal Server Error", "details": str(e)}), 500

@app.route('/', methods=['GET'])
def index():
    return "Webhook API is running!", 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)
