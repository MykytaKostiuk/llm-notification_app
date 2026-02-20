from langchain_core.tools import BaseTool

from agents.tools.search import google_serper_tool
from agents.tools.notifications import notification_tool

def build_tools() -> list[BaseTool]:
  search = google_serper_tool.tool_search
  notification= notification_tool.tool_push_ann
  return [search, notification]
