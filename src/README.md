# Email Extractor Tool

This project is an email extractor tool developed in Python. It retrieves emails from Gmail and converts them into an XML format.

## Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/RoyDanger/email_extractor.git
   cd email_extractor/src

2. Create a virtual environment and activate it:

python -m venv venv
# Windows
.\venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

3. Install the required libraries:

pip install -r requirements.txt

4. Place your client_secret.json file in the src directory. This file contains your OAuth 2.0 credentials

## Running the Script

To fetch emails from Gmail and convert them to XML:
python gmail_extractor.py
