from flask import Flask, request, jsonify

app = Flask(__name__)


VERIFICATION_TOKEN = 'A9f$Lx7!eQ2@Zm#4'


leave_balances = {
    "john.doe@example.com": {"casual": 5, "sick": 2},
    "pini@example.com": {"casual": 3, "sick": 1},
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

    data = request.json
    print("Incoming request:", data)


    user_email = data.get("user", {}).get("email", "john.doe@example.com")

    leave_data = leave_balances.get(user_email, leave_balances["default"])
    casual = leave_data["casual"]
    sick = leave_data["sick"]

    response_text = f"Annual leave : {sick}"

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
    app.run(port=5000, debug=True)
