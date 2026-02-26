import os
from langchain_ollama import ChatOllama
from langchain_openai import ChatOpenAI
from langchain_core.runnables import Runnable
from langchain_core.language_models import LanguageModelInput
from langchain_core.messages import AIMessage
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_core.tools import BaseTool
from pydantic import (
    SecretStr)

from langgraph.graph import StateGraph, START
from agents.state.agent_state import AgentState
from agents.tools import tools_provider
from agents.state.chekpointing.sql_lite_cp import sql_memory
from agents.state.chekpointing.dynamo_cp import dynamo_saver

class GraphDefinition:

  def __init__(self):
    pass

  def build_graph(self):
    graph_builder = StateGraph(AgentState)
    tools = tools_provider.build_tools()
    llm_with_tools = self.define_llm(tools)

    graph_builder.add_node("chatbot", self.chatbot(llm_with_tools))
    graph_builder.add_node("tools", ToolNode(tools=tools))

    graph_builder.add_conditional_edges(
        "chatbot", tools_condition)

    # Any time a tool is called, we return to the chatbot to decide the next step
    graph_builder.add_edge("tools", "chatbot")
    graph_builder.add_edge(START, "chatbot")

    graph = graph_builder.compile(checkpointer=dynamo_saver)
    graph.get_graph().draw_mermaid_png(output_file_path="graph.png")
    
    return graph

  def chatbot(self, llm: Runnable[LanguageModelInput, AIMessage]):
    return lambda state: {
        "messages": [llm.invoke(state.messages)]
    }

  def define_llm(self, tools: list[BaseTool]) -> Runnable[LanguageModelInput, AIMessage]:
    llm = ChatOllama(
        model='gpt-oss:20b',
        base_url='http://localhost:11434'
    )
    llm_qroq = ChatOpenAI(
        model="openai/gpt-oss-20b",
        api_key=SecretStr(os.environ.get("GROQ_API_KEY") or ""),
        base_url="https://api.groq.com/openai/v1"
    )
    llm_with_tools = llm_qroq.bind_tools(tools)
    return llm_with_tools
