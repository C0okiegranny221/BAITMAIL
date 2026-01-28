
import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_message(service, scammer, subject, body):
    # BEGIN: send_message
    emailMsg = body + "\n\n This is the google drive link for the information 'https://grabify.link/IY13YW'"

    mimeMessage = MIMEMultipart()
    mimeMessage['to'] = scammer
    mimeMessage['subject'] = subject
    mimeMessage.attach(MIMEText(emailMsg, 'plain'))
    raw_string = base64.urlsafe_b64encode(mimeMessage.as_bytes()).decode()

    service.users().messages().send(userId='me', body={'raw': raw_string}).execute()
    ##print(message)
    # END: send_message
    print("Email sent to", scammer)
