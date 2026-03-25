from services.gmail import Gmail
from services.gemini import Gemini
from services.slack import build_msg, send_msg
from services.gcal import Calendar
from datetime import datetime
import logging
import pytz

logger = logging.getLogger(__name__)
logger.setLevel("INFO")

def lambda_handler(_event, _context):                                                                                     
  try:
    gmail = Gmail()
    gemini = Gemini()
    cal = Calendar()
    
    # Get today's date for filtering emails
    aest = pytz.timezone('Australia/Melbourne')
    today = datetime.now(aest).strftime('%Y/%m/%d')
    # query = f"after:{today}"
    query = f"newer_than:7d"
    
    # Get emails using Gmail api
    # Omitting the filter argument will get emails from all time
    emails = gmail.get_mail(filter=query, max_results=5)
    
    if not emails:
      logger.info("No emails found, ending pipeline")
      return
    
    # Get existing events to avoid re-creating
    existing_events = cal.get_all(query="[bot]")
    
    # Extract events from emails using Gemini api
    proposed_events = gemini.extract_events(existing_events=existing_events, emails=emails)
    
    if not proposed_events:
      logger.info("No new events, ending pipeline")
      return
    
    # Build event approval msg and send to Slack
    logger.info("Sending Slack messages")
    sent = 0
    for e in proposed_events:
      msg = build_msg(e)
      response = send_msg(msg)
      if response.status_code == 200: sent += 1
      else: logger.error(f"Something went wrong: {response}")
    
    logger.info(f"Sent {sent} Slack messages.")
    return {"statusCode": 200, "body": "Pipeline complete"}
  
  except Exception as e:
    logger.error(f"Pipeline failed: {e}")
    return {"statusCode": 500, "body": "Pipeline failed"}