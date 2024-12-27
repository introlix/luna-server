from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from llama_cpp import Llama
from pydantic import BaseModel
from fastapi.responses import StreamingResponse
from typing import Optional, Dict
from luna_server.llm import LLM

class ChatRequest(BaseModel):
    model_path: str
    chat_format: str
    prompt: str
    system_prompt: Optional[str] = None
    task: str
    scan_documents: bool = False
    document_path: Optional[str] = None
    links: Optional[list] = None

app = FastAPI()

# Allow CORS for all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

@app.post("/")
def chat(request: ChatRequest):
    llm = LLM(request.model_path, request.prompt, request.chat_format, request.system_prompt, request.task, request.scan_documents, request.document_path, request.links)
    output = llm.create_chat_completion()
    
    def token_stream():
        try:
            for chunk in output:
                delta = chunk.get('choices', [{}])[0].get('delta', {})
                if 'content' in delta:
                    yield delta['content']
        except Exception as e:
            yield f"An error occurred: {e}"

    return StreamingResponse(token_stream(), media_type="text/plain")


# running the application
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=11343)
