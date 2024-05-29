import xml.etree.ElementTree as ET

def convert_to_xml(emails, output_file):
    root = ET.Element('Emails')
    for email in emails:
        email_element = ET.SubElement(root, 'Email')
        sender = ET.SubElement(email_element, 'Sender')
        sender.text = email.get('sender')
        date = ET.SubElement(email_element, 'Date')
        date.text = email.get('date')
        content = ET.SubElement(email_element, 'Content')
        content.text = email.get('content')
    tree = ET.ElementTree(root)
    tree.write(output_file)

if __name__ == "__main__":
    # Example emails
    emails = [
        {'sender': 'example1@gmail.com', 'date': '2024-05-01', 'content': 'Hello, this is a test email.'},
        {'sender': 'example2@outlook.com', 'date': '2024-05-02', 'content': 'Another test email.'}
    ]
    convert_to_xml(emails, 'emails.xml')
