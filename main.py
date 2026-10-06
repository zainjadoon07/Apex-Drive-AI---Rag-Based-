"""
main.py - FastAPI Server with WebSocket Token Streaming, RAG Retrieval Integration,
Interactive Citations, and Concurrency Support.
"""

import json
import re
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

# ---------------------------------------------------------------------------
# Pre-flight out-of-domain guardrail — hard block before LLM is ever called.
# Catches coding tasks, general knowledge, medical, legal, and other off-topic
# queries that the system prompt alone fails to reliably reject.
# ---------------------------------------------------------------------------
_OOD_PATTERNS = re.compile(
    r"\b("
    # Programming / code
    r"python|javascript|java\b|c\+\+|c#|rust|golang|php|ruby|swift|kotlin|typescript"
    r"|write.*code|code.*for|implement.*algorithm|algorithm|dijkstra|binary.*search"
    r"|sorting|recursion|\bscript\b|program(?:me|ming)|function|class definition"
    r"|data structure|linked list|stack|queue|tree|graph.*algorithm|dynamic.*program"
    r"|leetcode|hackerrank|regex.*pattern|sql.*query|api.*endpoint"
    # Science / homework
    r"|\bmath\b|calculus|integral|derivative|equation|theorem|proof"
    r"|biology|chemistry|physics|history.*war|essay|summarize.*article"
    r"|translate.*to|what.*capital.*of|who.*invented|when.*born"
    # Medical / legal
    r"|diagnos|symptom|medication|dosage|legal.*advice|lawsuit|copyright"
    r"|recipe|cook|ingredient"
    r")\b",
    re.IGNORECASE,
)

def is_out_of_domain(message: str) -> bool:
    """Returns True if the message is clearly outside the car rental domain."""
    return bool(_OOD_PATTERNS.search(message))

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

            # Handle stop_stream signal — client aborted generation
            if data.get("type") == "stop_stream":
                await websocket.send_json({"type": "stopped"})
                continue

            session_id = data.get("session_id", "default_user")
            user_message = data.get("message", "").strip()

            if not user_message:
                continue

            # 2. Pre-flight out-of-domain guardrail (hard block — runs before LLM)
            if is_out_of_domain(user_message):
                blocked_msg = (
                    "I'm Apex Drive AI, the official assistant for Apex Car Rental. "
                    "I can only help with vehicle selection, rental rates, insurance coverage, "
                    "pickup and return policies, and roadside emergencies. "
                    "I'm not able to assist with that request. "
                    "How can I help you with your car rental today?"
                )
                await websocket.send_json({"type": "token", "content": blocked_msg})
                await websocket.send_json({
                    "type": "end",
                    "metrics": {"retrieval_ms": 0, "ttft_ms": 0, "tps": 0,
                                "total_time_s": 0, "is_cached": False,
                                "is_relevant": False, "citations_count": 0}
                })
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


@app.get("/favicon.ico", include_in_schema=False)
@app.get("/favicon.jpg", include_in_schema=False)
async def serve_favicon():
    favicon_file = FRONTEND_DIR / "favicon.jpg"
    if favicon_file.exists():
        return FileResponse(str(favicon_file), media_type="image/jpeg")
    return FileResponse(str(FRONTEND_DIR / "index.html"))  # fallback


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
