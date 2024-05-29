import os.path
import json
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import googleapiclient.errors
import xml.etree.ElementTree as ET

# Define the scope
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
# Update with your credentials file path
CREDENTIALS_FILE = 'F:\\1. Personal\\projects\\email_extractor\\src\\client_secret_78361084380-osbftglnj1k355k7r4eadm6kt6npabbg.apps.googleusercontent.com.json'

def get_gmail_service():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('gmail', 'v1', credentials=creds)
        return service
    except Exception as e:
        print(f"Failed to create Gmail service: {e}")
        return None

def fetch_emails(service):
    try:
        results = service.users().messages().list(userId='me', maxResults=10).execute()
        messages = results.get('messages', [])
        emails = []
        for msg in messages:
            msg = service.users().messages().get(userId='me', id=msg['id']).execute()
            payload = msg['payload']
            headers = payload.get('headers', [])
            snippet = msg['snippet']
            email_data = {
                'id': msg['id'],
                'snippet': snippet,
                'sender': next((header['value'] for header in headers if header['name'] == 'From'), 'Unknown'),
                'date': next((header['value'] for header in headers if header['name'] == 'Date'), 'Unknown'),
                'content': snippet  # Assuming snippet is the content for simplicity
            }
            emails.append(email_data)
        return emails
    except googleapiclient.errors.HttpError as error:
        print('An error occurred:')
        print(json.dumps(json.loads(error.content), indent=4))
        return []
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return []

def convert_to_xml(emails, output_file):
    root = ET.Element('Emails')
    for email in emails:
        email_element = ET.SubElement(root, 'Email')
        sender = ET.SubElement(email_element, 'Sender')
        sender.text = email['sender']
        date = ET.SubElement(email_element, 'Date')
        date.text = email['date']
        content = ET.SubElement(email_element, 'Content')
        content.text = email['content']
    tree = ET.ElementTree(root)
    tree.write(output_file, encoding='utf-8', xml_declaration=True)

if __name__ == "__main__":
    service = get_gmail_service()
    if service:
        emails = fetch_emails(service)
        convert_to_xml(emails, 'emails.xml')
        for email in emails:
            print(email)

