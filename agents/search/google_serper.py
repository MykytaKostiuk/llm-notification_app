from langchain_community.utilities import GoogleSerperAPIWrapper
from langchain.agents import Tool


class GoogleSerperSerchAgentProvider:

  serper: GoogleSerperAPIWrapper
  DESCRIPTION = 'Useful for when you need more information from an online search'

  def __init__(self):
    self.serper = GoogleSerperAPIWrapper()

  def tool_search(self) -> Tool:
    return Tool(
        name="search",
        func=self.serper.run,
        description=self.DESCRIPTION
    )
