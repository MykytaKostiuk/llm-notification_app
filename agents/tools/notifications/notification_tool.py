from langchain_core.tools import tool
from pydantic import BaseModel, Field
import requests
import os

URL = 'https://dpocco02b9.execute-api.eu-north-1.amazonaws.com/prod/notify'

class PushNotificationInput(BaseModel):
  subject: str = Field(description="The subject of the push notification")
  message: str = Field(description="The message body of the push notification")

@tool(name_or_callable='send_push_notification',
      description='Useful for when you want to send a push notification',
      args_schema=PushNotificationInput)
def tool_push_ann(subject: str, message: str) -> None:
  push(subject=subject, message=message)

def push(subject: str, message: str):
  token: str = os.getenv('SNS_API_TOKEN') or ''
  print(f'subject: {subject}')
  resp = requests.post(URL,
                       headers={
                           'x-api-key': token
                       },
                       json={
                           "subject": subject,
                           "message": message
                       })
  # breakpoint()
  print(f'response: {resp.text}')
