from pydantic import BaseModel
from typing import Annotated
from langgraph.graph.message import add_messages

class AgentState(BaseModel):
  messages: Annotated[list, add_messages]