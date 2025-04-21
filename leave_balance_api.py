from flask import Flask, request, jsonify

app = Flask(__name__)

VERIFICATION_TOKEN = 'A9f$Lx7!eQ2@Zm4'

leave_balances = {
    "john.doe@example.com": {"casual": 5, "sick": 2},
    "pini@example.com": {"casual": 3, "sick": 1},
    "rajesh@example.com": {"annual": 10, "sick": 1},
    "default": {"casual": 0, "sick": 0}
}

@app.route('/leave_balance/', methods=['GET'])
def verify_token():
    token = request.args.get('token')
    challenge = request.args.get('challenge')

    if token != VERIFICATION_TOKEN:
        return 'Unauthorized', 401

    return challenge, 200

@app.route('/leave_balance/', methods=['POST'])
def webhook():
    token = request.args.get('token')
    if token != VERIFICATION_TOKEN:
        return 'Unauthorized', 401

    # Get email from request header
    user_email = request.headers.get('X-User-Email')
    if not user_email:
        return jsonify({"error": "Email is required in the headers"}), 400

    # Process the leave balance
    leave_data = leave_balances.get(user_email, leave_balances["default"])
    # casual = leave_data["casual"]
    # sick = leave_data["sick"]
    annual = leave_data["annual"]

    response_text = f"Annual leave : {annual}"

    response = {
        "responses": [
            {
                "type": "text",
                "message": response_text
            }
        ]
    }

    return jsonify(response)

if __name__ == '__main__':
    app.run(port=3000, debug=True)
