from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from app.core.engine import GitAnalyzerEngine
import pydantic

app = FastAPI(title="Multi-Agent Git Analyzer API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class IngestRequest(pydantic.BaseModel):
    repo_url: str

@app.post("/api/v1/ingest")
async def ingest_repository(payload: IngestRequest):
    engine = GitAnalyzerEngine(repo_url=payload.repo_url)
    success = engine.ingest_and_index()
    if success:
        return {"status": "success", "message": f"Successfully indexed {engine.repo_name}"}
    return {"status": "error", "message": "Failed to process repository context."}

@app.websocket("/api/v1/chat")
async def websocket_chat_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_json()
            user_question = data.get("question")
            repo_url = data.get("repo_url")
            
            if not user_question or not repo_url:
                await websocket.send_json({"error": "Missing parameters"})
                continue
                
            engine = GitAnalyzerEngine(repo_url=repo_url)
            
            # Stream tokens back to client in real-time
            async for token in engine.stream_query(user_question):
                await websocket.send_json({"token": token})
                
            await websocket.send_json({"status": "done"})
    except WebSocketDisconnect:
        print("Client disconnected from streaming channel.")