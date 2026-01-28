from flask import Flask, jsonify
from flask_cors import CORS
from message import service
from read_message import read_latest_email
from send_message import send_message
from bedrock import analyze_email_with_bedrock
from sender_details import get_email_sender
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/ping', methods=['GET'])
def ping():

    message = read_latest_email(service)
    summary = analyze_email_with_bedrock(message)
    #print("Email scam or not scam:", summary)
    email = get_email_sender(service)
    send_message(service,email,"SCAM KAREGA GANDU",summary)
    return jsonify({'message': 'THE EMAIL HAS BEEN SENT SUCCESSFULLY'})

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=3000)
