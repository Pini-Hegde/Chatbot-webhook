from flask import Flask, jsonify, request

app = Flask(__name__)

# Sample in-memory database of leave balances
leave_balances = {
    "john@example.com": {"casual": 5, "sick": 2, "earned": 10},
    "pini@example.com": {"casual": 8, "sick": 1, "earned": 7}
}

@app.route("/")
def home():
    return "✅ Leave Balance API is running!", 200

@app.route("/leave_balance/<email>", methods=["GET"])
def get_leave_balance(email):
    email = email.lower()

    # ✅ Handle ChatBot.com webhook URL validation challenge
    challenge = request.args.get("challenge")
    if challenge:
        return jsonify({"challenge": challenge})

    # ✅ Handle valid leave balance requests
    if email in leave_balances:
        return jsonify({
            "email": email,
            "leave_balance": leave_balances[email]
        }), 200
    else:
        return jsonify({
            "error": "User not found",
            "email_provided": email
        }), 404

# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)
