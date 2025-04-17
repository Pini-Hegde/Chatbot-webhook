from flask import Flask, jsonify, request

app = Flask(__name__)

# Sample in-memory database
leave_balances = {
    "john@example.com": {"casual": 5, "sick": 2, "earned": 10},
    "pini@example.com": {"casual": 8, "sick": 1, "earned": 7}
}

@app.route("/")
def home():
    return "Leave Balance API is running!"


# ✅ Webhook validation endpoint for ChatBot.com
@app.route("/leave_balance", methods=["GET"])
def validate_webhook():
    challenge = request.args.get("challenge")
    if challenge:
        return challenge, 200
    return "Missing challenge parameter", 400


# ✅ Actual API handler for leave balance using email
@app.route("/leave_balance/<email>", methods=["GET", "POST"])
def handle_leave_balance(email):
    email = email.lower()

    # GET request to fetch leave balance
    if request.method == "GET":
        if email in leave_balances:
            return jsonify({
                "email": email,
                "leave_balance": leave_balances[email]
            }), 200
        else:
            return jsonify({
                "error": "User not found"
            }), 404

    # POST request to update leave balance
    if request.method == "POST":
        data = request.get_json()

        if email not in leave_balances:
            leave_balances[email] = {"casual": 0, "sick": 0, "earned": 0}

        for leave_type in data:
            if leave_type in leave_balances[email]:
                leave_balances[email][leave_type] += data[leave_type]
            else:
                leave_balances[email][leave_type] = data[leave_type]

        return jsonify({
            "message": "Leave balance updated",
            "leave_balance": leave_balances[email]
        }), 200


if __name__ == "__main__":
    app.run(debug=True)
