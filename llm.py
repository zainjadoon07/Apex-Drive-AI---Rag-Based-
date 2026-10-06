"""
llm.py - Local CPU LLM Streaming Engine & Real-Time Latency Metrics
"""

import os
import json
import time
import httpx
from typing import AsyncGenerator, Dict, Tuple, List

# Default local Ollama endpoint and CPU-friendly model
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://127.0.0.1:11434/api/chat")
MODEL_NAME = os.getenv("LLM_MODEL", "qwen2.5:1.5b")


async def stream_llm_response(
    messages: List[Dict[str, str]],
    model_name: str = MODEL_NAME
) -> AsyncGenerator[Tuple[str, Dict], None]:
    """
    Sends ChatML messages to local Ollama LLM and yields:
      (token_chunk, running_metrics)
    Final yield provides completed latency statistics:
      - ttft_ms: Time to First Token in milliseconds
      - tps: Tokens per second throughput
      - total_time_s: Total inference elapsed time
      - token_count: Total tokens generated
    """
    payload = {
        "model": model_name,
        "messages": messages,
        "stream": True,
        "options": {
            "temperature": 0.2,       # Low temperature for precise factual adherence
            "top_p": 0.9,
            "num_predict": 512,       # Bounded output to keep latency low
        }
    }

    start_time = time.perf_counter()
    first_token_time = None
    token_count = 0

    try:
        async with httpx.AsyncClient(timeout=120.0) as client:
            async with client.stream("POST", OLLAMA_URL, json=payload) as response:
                if response.status_code != 200:
                    err_msg = f"[LLM Error: HTTP {response.status_code} from local Ollama service]"
                    yield err_msg, {"is_final": True, "ttft_ms": 0, "tps": 0, "total_time_s": 0}
                    return

                async for line in response.aiter_lines():
                    if not line:
                        continue

                    try:
                        data = json.loads(line)
                    except json.JSONDecodeError:
                        continue

                    token = data.get("message", {}).get("content", "")

                    if token:
                        now = time.perf_counter()
                        if first_token_time is None:
                            first_token_time = now
                        token_count += 1

                        elapsed = now - start_time
                        ttft_ms = (first_token_time - start_time) * 1000.0

                        metrics = {
                            "is_final": False,
                            "ttft_ms": round(ttft_ms, 2),
                            "tps": round(token_count / max(elapsed, 0.001), 2),
                            "token_count": token_count
                        }
                        yield token, metrics

                    if data.get("done", False):
                        break

        total_time = time.perf_counter() - start_time
        ttft_ms = (first_token_time - start_time) * 1000.0 if first_token_time else 0.0
        final_metrics = {
            "is_final": True,
            "ttft_ms": round(ttft_ms, 2),
            "total_time_s": round(total_time, 2),
            "token_count": token_count,
            "tps": round(token_count / max(total_time, 0.001), 2)
        }
        yield "", final_metrics

    except (httpx.ConnectError, httpx.ConnectTimeout):
        # Graceful simulated response if Ollama is not yet started by the user
        fallback_msg = (
            "*(Local Ollama offline — run `ollama serve` and `ollama pull qwen2.5:1.5b` to connect the real CPU model)*\n\n"
            "Welcome to Apex Car Rental! Based on our verified records, we offer Economy ($45/day), "
            "Compact SUV ($72/day), Electric EV ($75/day), and Luxury ($125/day) with standard unlimited mileage. "
            "How may I assist with your booking today?"
        )
        yield fallback_msg, {
            "is_final": True,
            "ttft_ms": 0,
            "total_time_s": 0.01,
            "token_count": len(fallback_msg.split()),
            "tps": 0
        }
