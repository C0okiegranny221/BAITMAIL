from message import service

def get_email_sender(service, user_id='me'):
    results = service.users().messages().list(userId='me',q="is:unread",  maxResults=1).execute()
    messages = results.get('messages', [])

    if not messages:
        print("No messages found.")
        return

    message_id = messages[0]['id']
    # Get the message metadata with 'metadata' format to reduce payload
    message = service.users().messages().get(userId=user_id, id=message_id, format='metadata', metadataHeaders=['From']).execute()
    
    headers = message.get('payload', {}).get('headers', [])
    sender = None

    for header in headers:
        if header['name'] == 'From':
            sender = header['value']
            break
    import re

    text = sender
    #email = re.search(r'<(.+?)>', text).group(1)
    print(text)  
    return text
def get_authenticated_user_email(service):
    
    profile = service.users().getProfile(userId='me').execute()
    return profile.get('emailAddress')

print(get_email_sender(service))
