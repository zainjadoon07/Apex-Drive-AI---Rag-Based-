"""
main.py - FastAPI Server with WebSocket Token Streaming, RAG Retrieval Integration,
Interactive Citations, and Concurrency Support.
"""

import json
import time
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel

# Custom Application Modules
from memory import memory_manager
from retrieval import retrieval_engine, RetrievalResult
from prompts import build_rag_prompt_messages
from llm import stream_llm_response

app = FastAPI(title="Apex Car Rental AI Assistant (RAG Enabled)")

FRONTEND_DIR = Path(__file__).resolve().parent / "frontend"


# --- REST API Endpoints ---

@app.get("/api/health")
async def health_check():
    """Returns server and index status."""
    is_index_ready = False
    doc_count = 0
    chunk_count = 0

    try:
        retrieval_engine.load_index()
        is_index_ready = retrieval_engine.is_loaded
        chunk_count = len(retrieval_engine.chunks)
        # Unique doc count
        unique_docs = {c.get("source_file") for c in retrieval_engine.chunks if c.get("source_file")}
        doc_count = len(unique_docs)
    except Exception:
        pass

    return {
        "status": "healthy",
        "service": "Apex Car Rental AI (Assignment 2)",
        "rag_index_ready": is_index_ready,
        "indexed_documents": doc_count,
        "indexed_chunks": chunk_count,
        "active_sessions": len(memory_manager.sessions)
    }


class ResetRequest(BaseModel):
    session_id: str

@app.post("/api/reset")
async def reset_session(payload: ResetRequest):
    """Resets conversation memory for a user session."""
    memory_manager.reset_session(payload.session_id)
    return {"status": "success", "message": f"Session {payload.session_id} reset."}


# --- WebSocket Chat Streaming Endpoint ---

@app.websocket("/ws/chat")
async def websocket_chat_endpoint(websocket: WebSocket):
    """
    WebSocket endpoint handling real-time conversation turns:
    1. Receives: {"session_id": "...", "message": "..."}
    2. Runs hybrid RAG retrieval asynchronously (thread pool).
    3. Emits citations event: {"type": "citations", "citations": [...], "retrieval_ms": ...}
    4. Streams LLM tokens: {"type": "token", "content": "..."}
    5. Emits end event with full latency metrics: {"type": "end", "metrics": {...}}
    """
    await websocket.accept()

    try:
        while True:
            # 1. Receive incoming message from client
            raw_text = await websocket.receive_text()
            try:
                data = json.loads(raw_text)
            except json.JSONDecodeError:
                await websocket.send_json({"type": "error", "message": "Invalid JSON format"})
                continue

            session_id = data.get("session_id", "default_user")
            user_message = data.get("message", "").strip()

            if not user_message:
                continue

            # 2. Retrieve conversation session
            session = memory_manager.get_or_create_session(session_id)
            history = session.get_sliding_window_history(max_turns=8)

            # 3. Execute Hybrid RAG Retrieval asynchronously
            retrieval_res: RetrievalResult = await retrieval_engine.async_retrieve(
                query=user_message,
                mode="hybrid",
                top_k=4
            )

            # Send citations event to UI before or during streaming
            if retrieval_res.citations:
                await websocket.send_json({
                    "type": "citations",
                    "citations": retrieval_res.citations,
                    "retrieval_ms": retrieval_res.latency_ms,
                    "is_cached": retrieval_res.is_cached
                })

            # Format retrieved context according to context budget (max 1200 tokens)
            retrieved_context_str = retrieval_res.format_context_for_prompt(max_tokens=1200)

            # 4. Assemble Grounded Prompt with Context Overflow Protection
            prompt_messages = build_rag_prompt_messages(
                history=history,
                new_user_message=user_message,
                retrieved_context=retrieved_context_str,
                is_relevant=retrieval_res.is_relevant
            )

            # 5. Stream Tokens from Local LLM
            full_response = ""
            final_metrics = {}

            async for token, metrics in stream_llm_response(prompt_messages):
                if token:
                    full_response += token
                    await websocket.send_json({
                        "type": "token",
                        "content": token
                    })

                if metrics.get("is_final", False):
                    final_metrics = metrics

            # 6. Save Turn to Session Memory
            session.add_user_message(user_message)
            session.add_assistant_message(full_response)
            session.last_citations = retrieval_res.citations

            # 7. Notify Client that Streaming has Ended with Complete Latency Metrics
            final_metrics["retrieval_ms"] = retrieval_res.latency_ms
            final_metrics["is_cached"] = retrieval_res.is_cached
            final_metrics["is_relevant"] = retrieval_res.is_relevant
            final_metrics["citations_count"] = len(retrieval_res.citations)

            await websocket.send_json({
                "type": "end",
                "metrics": final_metrics
            })

    except WebSocketDisconnect:
        # User closed browser tab or disconnected
        pass
    except Exception as e:
        try:
            await websocket.send_json({
                "type": "error",
                "message": f"Server processing error: {str(e)}"
            })
        except Exception:
            pass


# --- Static Frontend Serving ---

FRONTEND_DIR.mkdir(parents=True, exist_ok=True)
app.mount("/static", StaticFiles(directory=str(FRONTEND_DIR)), name="static")

@app.get("/")
async def serve_frontend():
    index_file = FRONTEND_DIR / "index.html"
    if index_file.exists():
        return FileResponse(str(index_file))
    return {"message": "Apex Car Rental API is running. Frontend index.html not found."}


@app.on_event("startup")
async def startup_event():
    try:
        retrieval_engine.load_index()
        print(f"[Startup] Pre-loaded {len(retrieval_engine.chunks)} chunks into memory.")
    except Exception as e:
        print(f"[Startup] Note: Index not preloaded ({e}).")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8080, reload=True)
