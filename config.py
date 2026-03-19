from dotenv import load_dotenv
import os

load_dotenv(override=True)

def load_secrets():
  '''Get secrets from AWS Secret Manager'''
  secrets = {
    'GOOGLE_CLIENT_ID':     os.getenv('GOOGLE_CLIENT_ID'),
    'GOOGLE_CLIENT_SECRET': os.getenv('GOOGLE_CLIENT_SECRET'),
    'GOOGLE_API_KEY':       os.getenv('GOOGLE_API_KEY'),
    'GOOGLE_REFRESH_TOKEN': os.getenv('GOOGLE_REFRESH_TOKEN'),
    'MAILBOXES':            os.getenv('MAILBOXES')
  }
  
  for key, value in secrets.items():
        print(f"{key}: {'SET' if value else 'MISSING'}")
  
  return secrets