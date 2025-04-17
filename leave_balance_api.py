from flask import Flask, request, jsonify

app = Flask(__name__)

# Sample in-memory leave balance database
leave_balances = {
    "john@example.com": {"casual": 5, "sick": 2, "earned": 10},
    "pini@example.com": {"casual": 8, "sick": 1, "earned": 7}
}

@app.route("/")
def home():
    return "✅ Leave Balance API is running!", 200

@app.route("/leave_balance/<email>", methods=["GET"])
def get_leave_balance(email):
    # ✅ Handle ChatBot.com URL validation
    challenge = request.args.get("challenge")
    if challenge:
        return jsonify({"challenge": challenge})


    email = email.lower()
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

if __name__ == "__main__":
    app.run(debug=True)
