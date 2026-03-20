from services.gmail import Gmail
from services.gemini import Gemini

gmail = Gmail()
gemini = Gemini()
emails = gmail.get_mail()
events = gemini.extract_events(emails)

print(events)
