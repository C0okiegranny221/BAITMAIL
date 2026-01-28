from message import service
from read_message import read_latest_email
from send_message import send_message
from bedrock import analyze_email_with_bedrock
message = read_latest_email(service)
summary = analyze_email_with_bedrock("message")

#print("Email scam or not scam:", summary)
send_message(service,"namanagrawal568@gmail.com","scam karta hai gandu",summary)