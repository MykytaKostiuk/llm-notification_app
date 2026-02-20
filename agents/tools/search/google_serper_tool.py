from langchain_community.utilities import GoogleSerperAPIWrapper
from langchain_core.tools import Tool, tool
from pydantic import BaseModel, Field

class SearchInput(BaseModel):
  query: str = Field(description="The search request query")

@tool(name_or_callable='send_push_notification',
      description='Useful for when you need more information from an online search',
      args_schema=SearchInput)
def tool_search(query: str) -> str:
  serper = GoogleSerperAPIWrapper()
  return serper.run(query)
