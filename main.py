from dotenv import load_dotenv
load_dotenv(override=True)

import gradio as gr
from agents.graph.graph_definition import GraphDefinition
from agents.graph.graph_definition import AgentState

def main():
    print("Hello from notifications-app!")
    graph = GraphDefinition().build_graph()
    # graph.invoke(AgentState(messages=["Send notification with the pie recipe"]))
    
    def chat(user_input: str, history):
        state = AgentState(messages=[{"role": "user", "content": user_input}])
        result = graph.invoke(state)
        return result["messages"][-1].content
    
    gr.ChatInterface(chat).launch()
    

if __name__ == "__main__":
    main()
