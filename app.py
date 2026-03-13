import gradio as gr, requests

URL = "http://localhost:8000/summarize"

def summarize(text):
    if not text.strip():
        return "Please enter text to summarize"
    
    try:
       
        response = requests.post(URL, json={"text": text})
        return response.json()["summary"]

    except Exception as e:
        return "Error: " + str(e)
        

iface = gr.Interface(
    fn = summarize,
    inputs = gr.Textbox(lines=8, placeholder="Paste your article/text here...", label="Input Text"),
    outputs=gr.Textbox(label="Summary"),
    title="AI Text Summarizer",
    description = "Powered by Groq/LLaMA"
)

if __name__ == "__main__": iface.launch()