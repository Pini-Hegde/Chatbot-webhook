from flask import Flask, request, jsonify
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)

VERIFICATION_TOKEN = 'A9f$Lx7!eQ2@Zm4'

@app.route('/leave_request/', methods=['GET'])
def verify_token():
    token = request.args.get('token')
    challenge = request.args.get('challenge')

    if token != VERIFICATION_TOKEN:
        return 'Unauthorized', 401

    return challenge, 200

@app.route('/leave_request/', methods=['POST'])
def webhook():
    token = request.args.get('token')
    if token != VERIFICATION_TOKEN:
        return 'Unauthorized', 401

    # Get data from request headers
    fname = request.headers.get('Fname')
    lname = request.headers.get('Lname')
    leave_date = request.headers.get('Date')
    leave_type = request.headers.get('Leave-Type')
    sender_email = request.headers.get('Sender-Email')
    print(fname, lname, leave_date, leave_type, sender_email)

    if not fname or not lname or not leave_date or not leave_type or not sender_email:
        return jsonify({"error": "All fields (Fname, Lname, Date, Leave-Type, Sender-Email) are required in the headers"}), 400
    else:
        print("All fields are present")
    # Compose the email message
    subject = f"Leave Request from {fname} {lname}"
    body = f"Leave Request Details:\n\nName: {fname} {lname}\nLeave Date: {leave_date}\nLeave Type: {leave_type}\nSender Email: {sender_email}"
    print("Email body is ready")
    
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = "praveen.hegde@synergysolutions.asia"
    msg['Subject'] = subject
    
    print(msg)

    msg.attach(MIMEText(body, 'plain'))

    # Send email using SMTP (you may need to replace the SMTP server and authentication info with your details)
    try:
        print("Sending email...")
        server = smtplib.SMTP('smtp.gmail.com', 587)  # Use appropriate SMTP server and port
        print("Server is ready")
        server.starttls()
        print("TLS started")
        server.login('praveenhegde0987@gmail.com', 'dyfg elqx lagy btyt')  # Use your email and app password
        print("Logged in successfully")
        text = msg.as_string()
        print("All set to triggerc email")
        server.sendmail(sender_email, "praveen.hegde@synergysolutions.asia", text)
        print("Email sent successfully")
        server.quit()

        response = {
            "responses": [
                {
                    "type": "text",
                    "message": f"Leave request from {fname} {lname} has been sent successfully."
                }
            ]
        }
        return jsonify(response)

    except Exception as e:
        return jsonify({"error": f"Failed to send email: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(port=3000, debug=True)
