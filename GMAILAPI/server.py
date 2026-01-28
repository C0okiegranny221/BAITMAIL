from flask import Flask, jsonify
from flask_cors import CORS
from message import service
from read_message import read_latest_email
from send_message import send_message
from bedrock import analyze_email_with_bedrock
from sender_details import get_email_sender
from sender_details import get_authenticated_user_email
from bedrock import analyze_email_with_bedrock_scam_back
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/ping', methods=['GET'])

def ping():

    message = read_latest_email(service)
    email = get_email_sender(service)
    email_user = get_authenticated_user_email(service)
    if (message == "No new emails") | (email==email_user):
        return jsonify({'message': 'NO SCAM EMAILS DETECTED'})
    summary = analyze_email_with_bedrock(message)
    #print("Email scam or not scam:", summary)
    if "qwerty" in summary:
        scam_back = analyze_email_with_bedrock_scam_back(message)
        send_message(service,email,"This in regards to your offer.",scam_back)
        send_message(service,email_user,"SCAM EMAIL DETECTED",f"SCAM EMAIL DETECTED FROM {email} WITH THE CONTENT {message} AND THE ANALYSIS IS {summary[10:]}")
        return jsonify({'message': 'THE EMAIL HAS BEEN SENT SUCCESSFULLY'})
    else:
        return jsonify({'message': 'NO SCAM EMAILS DETECTED'})

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=3000)
