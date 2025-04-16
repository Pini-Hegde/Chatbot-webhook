from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/chatbot-webhook', methods=['POST'])
def chatbot_webhook():
    data = request.get_json()

    # Extract the user message from the request
    user_message = data.get('message', '')

    # Do your logic here (AI/ML/DB/API etc.)
    # For now, let's echo the message with a custom twist
    if 'hello' in user_message.lower():
        bot_reply = "Hi there! How can I help you today? 😊"
    else:
        bot_reply = f"You said: {user_message}. That's interesting!"

    # IMPORTANT: Return this structure for ChatBot.com
    return jsonify({
        "reply": bot_reply
    })

if __name__ == '__main__':
    app.run(debug=True)
