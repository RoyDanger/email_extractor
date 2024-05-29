import msal
import requests

CLIENT_ID = 'your-client-id'
CLIENT_SECRET = 'your-client-secret'
AUTHORITY = 'https://login.microsoftonline.com/your-tenant-id'
SCOPES = ['https://graph.microsoft.com/.default']

def get_outlook_token():
    app = msal.ConfidentialClientApplication(
        CLIENT_ID, authority=AUTHORITY,
        client_credential=CLIENT_SECRET)
    result = app.acquire_token_for_client(scopes=SCOPES)
    if 'access_token' in result:
        return result['access_token']
    else:
        raise Exception('Error obtaining token')

def fetch_emails(token):
    headers = {'Authorization': 'Bearer ' + token}
    response = requests.get('https://graph.microsoft.com/v1.0/me/messages', headers=headers)
    emails = response.json()['value']
    return emails

if __name__ == "__main__":
    token = get_outlook_token()
    emails = fetch_emails(token)
    for email in emails:
        print(email['subject'], email['bodyPreview'])
