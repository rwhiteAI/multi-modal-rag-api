# gradio_app.py

import gradio as gr
import requests

class ApiClient:
    def __init__(self, base_url: str = "http://127.0.0.1:5000"):
        self.base_url = base_url

    def ingest_file(self, file_path: str) -> dict:
        with open(file_path, "rb") as f:
            response = requests.post(f"{self.base_url}/ingest", files={"file": f})
        return response.json()

    def query(self, question: str, media_type: str) -> dict:
        payload = {"question": question}
        if media_type != "all":
            payload["media_type"] = media_type
        response = requests.post(f"{self.base_url}/query", json=payload)
        return response.json()


client = ApiClient()


def handle_ingest(file_path):
    if file_path is None:
        return "No file uploaded."
    result = client.ingest_file(file_path)
    if "error" in result:
        return f"Error: {result['error']}"
    return f"Ingested '{result['filename']}' as media_type: {result['media_type']}"


def handle_query(question, media_type):
    if not question.strip():
        return "Please enter a question."
    result = client.query(question, media_type)
    if "error" in result:
        return f"Error: {result['error']}"
    return result["answer"]


with gr.Blocks(title="Multimodal RAG API Demo") as demo:
    gr.Markdown("# Multimodal RAG API Demo")

    with gr.Tab("Ingest"):
        file_input = gr.File(label="Upload audio, image, video, or PDF", type="filepath")
        ingest_button = gr.Button("Ingest")
        ingest_output = gr.Textbox(label="Result", interactive=False)
        ingest_button.click(fn=handle_ingest, inputs=file_input, outputs=ingest_output)

    with gr.Tab("Query"):
        question_input = gr.Textbox(label="Question")
        media_type_input = gr.Dropdown(
            choices=["all", "audio", "image", "video", "document"],
            value="all",
            label="Media Type"
        )
        query_button = gr.Button("Ask")
        query_output = gr.Textbox(label="Answer", interactive=False)
        query_button.click(fn=handle_query, inputs=[question_input, media_type_input], outputs=query_output)

if __name__ == "__main__":
    demo.launch()