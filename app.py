import gradio as gr, requests

URL = "http://localhost:7860/summarize"

def summarize(text):
    if not text.strip():
        return "Please enter text to summarize"
    
    try:
        full_text: str = ""
        stream = requests.post(URL, json={"text": text}, stream=True)
        for chunk in stream.iter_lines():
            full_text += chunk.decode().removeprefix("data: ")
            yield full_text
        
    except Exception as e:
        yield "Error: " + str(e)
        

iface = gr.Interface(
    fn = summarize,
    inputs = gr.Textbox(lines=8, placeholder="Paste your article/text here...", label="Input Text"),
    outputs=gr.Textbox(label="Summary"),
    title="AI Text Summarizer",
    description = "Powered by Groq/LLaMA"
)

#if __name__ == "__main__": iface.launch(server_name="0.0.0.0")
