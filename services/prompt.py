from datetime import datetime
from pydantic import BaseModel, Field
from typing import List, Optional

today = datetime.now().strftime('%Y-%m-%d')

prompt = f"""
  Today is {today}.

  Your job is to filter the provided emails and find any important events, or actions items, and return calendar entries for each.

  Only include events that are important or actually require a response.
  Return a JSON array per the schema provided. 
  Only include events with confidence > 0.7.
  Return empty array [] if no events found.
  Return JSON only, no other text.
"""

class Event(BaseModel):
  title: str = Field(description="Brief event title")
  from_: str = Field(description="Sender of the email from which the event is generated (use names over addresses)")
  date: str = Field(description="YYYY-MM-DD format")
  time: str = Field(description="HH:MM 24hr format")
  duration_minutes: int = Field(default=60, description="Default 60 if not specified")
  location: Optional[str] = Field(default=None, description="Physical or virtual location")
  description: Optional[str] = Field(default=None, description="Additional context")
  confidence: float = Field(description="0-1 confidence score")

class Events(BaseModel):
  events: List[Event]
