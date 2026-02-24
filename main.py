from dotenv import load_dotenv
load_dotenv(override=True)

import uuid
import boto3
import gradio as gr
from langchain_core.runnables import RunnableConfig
from agents.graph.graph_definition import GraphDefinition
from agents.graph.graph_definition import AgentState

TABLE_NAME = "lg-checkpoint-table"


def list_thread_ids() -> list[str]:
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(TABLE_NAME)  # type: ignore[attr-defined]
    items = table.scan(ProjectionExpression="PK").get("Items", [])
    return sorted({item["PK"] for item in items})


def main():
    graph = GraphDefinition().build_graph()

    with gr.Blocks() as demo:
        thread_id = gr.State(value=str(uuid.uuid4()))

        with gr.Row():
            thread_dropdown = gr.Dropdown(choices=list_thread_ids(), label="Conversation", scale=4)
            new_chat_btn = gr.Button("+ New Chat", scale=1)

        chatbot = gr.Chatbot()
        msg_input = gr.Textbox(placeholder="Type a message...", show_label=False)

        def new_chat():
            new_id = str(uuid.uuid4())
            return new_id, [], gr.update(choices=list_thread_ids(), value=None)

        def select_thread(selected_id):
            return selected_id, []

        def send(user_input, history, tid):
            config = RunnableConfig(configurable={"thread_id": tid})
            result = graph.invoke(
                AgentState(messages=[{"role": "user", "content": user_input}]),
                config=config,
            )
            ai_response = result["messages"][-1].content
            history = history + [
                {"role": "user", "content": user_input},
                {"role": "assistant", "content": ai_response},
            ]
            return history, "", gr.update(choices=list_thread_ids(), value=tid)

        new_chat_btn.click(new_chat, outputs=[thread_id, chatbot, thread_dropdown])
        thread_dropdown.change(select_thread, inputs=[thread_dropdown], outputs=[thread_id, chatbot])
        msg_input.submit(send, inputs=[msg_input, chatbot, thread_id], outputs=[chatbot, msg_input, thread_dropdown])

    demo.launch()


if __name__ == "__main__":
    main()
