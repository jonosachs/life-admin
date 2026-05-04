from models.event import Event, Events
from services.llm_base import LlmBase
from services.prompt import prompt
from config import load_secrets
from google.genai import errors
from google import genai
from typing import List
import logging

logger = logging.getLogger(__name__)


class Gemini(LlmBase):
    def __init__(self):
        self.secrets = load_secrets()

    def extract_events(self, exist_events, declined_events, emails) -> Events:
        logger.info("Contacting Gemini API..")

        prompt_contents = f"{prompt}\nExisting Events:\n{exist_events}\nRecently Declined Events:\n{declined_events}\nEmails:\n{emails}"

        try:
            logger.info("Attempting to extract events..")
            response = self.client.models.generate_content(
                model="gemini-3-flash-preview",
                contents=prompt_contents,
                config={
                    "response_mime_type": "application/json",
                    "response_json_schema": Events.model_json_schema(),
                },
            )
            events_obj = Events.model_validate_json(response.text)
            events = (
                events_obj.events
            )  # Pydantic 'Events' object has field events: List[Event]

            if events:
                logger.info(
                    f"Extracted {len(events)} events from {len(emails)} emails."
                )
            else:
                logger.info(f"No events found in {len(emails)} emails.")
                logger.info(f"Gemini notes: {events_obj.notes}")

            return events_obj

        except errors.APIError as e:
            logger.error(f"An error occured while trying to extract events: {e}")
            raise
