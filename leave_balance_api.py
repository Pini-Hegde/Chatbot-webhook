from flask import Flask, jsonify, request

app = Flask(__name__)

# Sample in-memory database
leave_balances = {
    "john@example.com": {"casual": 5, "sick": 2, "earned": 10},
    "pini@example.com": {"casual": 8, "sick": 1, "earned": 7}
}

# Define your secure token here
VALID_TOKEN = "securetoken123"

# ✅ Webhook validation endpoint for ChatBot.com
@app.route("/leave_balance", methods=["GET"])
def validate_webhook():
    challenge = request.args.get("challenge")
    
    # Token validation for the Webhook verification (GET request)
    token = request.headers.get("Authorization")
    if not token or not token.startswith("Bearer "):
        return jsonify({"error": "Unauthorized - Missing or invalid token"}), 401
    
    # Extract the token part and compare with valid token
    token = token.split(" ")[1]  # Get token part after "Bearer"
    if token != VALID_TOKEN:
        return jsonify({"error": "Unauthorized - Invalid token"}), 401
    
    if challenge:
        return challenge, 200
    return "Missing challenge parameter", 400


# ✅ Actual API handler for leave balance using email
@app.route("/leave_balance/<email>", methods=["GET", "POST"])
def handle_leave_balance(email):
    email = email.lower()

    # Token validation for actual leave balance API (GET/POST request)
    token = request.headers.get("Authorization")
    if not token or not token.startswith("Bearer "):
        return jsonify({"error": "Unauthorized - Missing or invalid token"}), 401
    
    token = token.split(" ")[1]  # Get token part after "Bearer"
    if token != VALID_TOKEN:
        return jsonify({"error": "Unauthorized - Invalid token"}), 401

    # Handle GET request to fetch leave balance
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

    # Handle POST request to update leave balance
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
