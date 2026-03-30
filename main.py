import os, groq
from dotenv import load_dotenv
from groq import Groq
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import StreamingResponse
import gradio as gr
from app import iface

load_dotenv()
key = os.environ.get("GROQ_API_KEY")
client = Groq(api_key=key)


class SummarizeRequest(BaseModel):
    text: str

app = FastAPI()

@app.post("/summarize")
def summarize(request: SummarizeRequest):
    if not request.text.strip():
        return "Please enter text to summarize"
    
    try:
        messages = [
            {"role": "system", "content":"You need to summarize the input, make sure the length is not greater than 150 and you need to give bullet points"},
            {"role": "user", "content": request.text}
        ]

        stream = client.chat.completions.create(
            model = "llama-3.1-8b-instant",
            messages = messages,
            stream=True
        )


        return StreamingResponse(generator(stream), media_type="text/event-stream")


    
    except groq.AuthenticationError:
        return  "Invalid API Key"
    except groq.RateLimitError:
        return "Too many requests, try again"
    except Exception as e:
        return "Error: " + str(e)
    
@app.post("/summarize-sync")
def summarize_sync(request: SummarizeRequest):
    if not request.text.strip():
        return {"error": "Please enter text to summarize"}
    
    try:
        messages = [
            {"role": "system", "content": "You need to summarize the input, make sure the length is not greater than 150 and you need to give bullet points"},
            {"role": "user", "content": request.text}
        ]
        response = client.chat.completions.create(
            model = "llama-3.1-8b-instant",
            messages = messages,
            stream= False
        )

        return {"summary": response.choices[0].message.content}
    
    except groq.AuthenticationError:
        return  "Invalid API Key"
    except groq.RateLimitError:
        return "Too many requests, try again"
    except Exception as e:
        return "Error: " + str(e)


app = gr.mount_gradio_app(app, iface, path="/")

def generator(stream):
    for chunk in stream:
        content = chunk.choices[0].delta.content
        if content is not None:
            yield f"data: {content}\n\n"
    return    


        

    





