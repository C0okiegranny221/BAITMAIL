from google_mod import Create_Service
import base64
import email
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from message import service

def extract_plain_text(msg):
    if msg.is_multipart():
        for part in msg.walk():
            if part.get_content_type() == "text/plain" and "attachment" not in str(part.get("Content-Disposition")):
                return part.get_payload(decode=True).decode(part.get_content_charset("utf-8"))
    else:
        if msg.get_content_type() == "text/plain":
            return msg.get_payload(decode=True).decode(msg.get_content_charset("utf-8"))
    return None
'''
messages = []

def read_latest_email(service):
    results = service.users().messages().list(userId='me',q="is:unread",  maxResults=1).execute()
    messages = results.get('messages', [])

    if not messages:
        print("No messages found.")
        return

    message_id = messages[0]['id']
    message = service.users().messages().get(userId='me', id=message_id, format='raw').execute()
    raw_message = base64.urlsafe_b64decode(message['raw'].encode("ASCII"))
    #print("Latest Email MIME:", raw_message.decode("utf-8"))
    message_plain = email.message_from_bytes(raw_message)
    message_plain = extract_plain_text(message_plain)
    
    if message_plain not in messages:
        messages.append(message_plain)
        return message_plain
    #print("Latest Email Body:", message_plain)
    return "No new emails"
'''
##read_latest_email(service)
processed_messages = set()  # to track already processed messages

def read_latest_email(service):
    results = service.users().messages().list(
        userId='me',
        q="is:unread",
        maxResults=1
    ).execute()

    msgs = results.get('messages', [])

    if not msgs:
        print("No messages found.")
        return "No new emails"

    message_id = msgs[0]['id']
    message = service.users().messages().get(
        userId='me', id=message_id, format='raw'
    ).execute()

    raw_message = base64.urlsafe_b64decode(message['raw'].encode("ASCII"))
    message_plain = email.message_from_bytes(raw_message)
    message_plain = extract_plain_text(message_plain)

    # Check if we already processed this email
    if message_id not in processed_messages:
        processed_messages.add(message_id)
        return message_plain

    return "No new emails"

