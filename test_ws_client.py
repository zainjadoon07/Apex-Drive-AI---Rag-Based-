"""
test_ws_client.py - Live WebSocket client test verifying RAG retrieval, citations, and streaming tokens.
"""

import asyncio
import json
import websockets

async def test_live_chat():
    uri = "ws://127.0.0.1:8080/ws/chat"
    print(f"Connecting to {uri}...")

    async with websockets.connect(uri) as ws:
        print("Connected!")
        query = "What is the deductible for Gold Platinum and does it include free towing?"
        payload = {
            "session_id": "test_sess_live",
            "message": query
        }

        print(f"\nSending Query: '{query}'")
        await ws.send(json.dumps(payload))

        citations_received = []
        tokens_received = []
        final_metrics = {}

        while True:
            raw_msg = await ws.recv()
            data = json.loads(raw_msg)
            msg_type = data.get("type")

            if msg_type == "citations":
                citations_received = data.get("citations", [])
                retrieval_ms = data.get("retrieval_ms", 0)
                print(f"\n[EVENT: CITATIONS] Found {len(citations_received)} sources in {retrieval_ms:.2f} ms:")
                for idx, cit in enumerate(citations_received, start=1):
                    print(f"  {idx}. [{cit.get('category')}] {cit.get('title')} ({cit.get('source_file')})")

            elif msg_type == "token":
                token = data.get("content", "")
                tokens_received.append(token)
                print(token, end="", flush=True)

            elif msg_type == "end":
                final_metrics = data.get("metrics", {})
                print("\n\n[EVENT: END OF STREAM]")
                print(f"Metrics: RAG Retrieval={final_metrics.get('retrieval_ms')}ms | TTFT={final_metrics.get('ttft_ms')}ms | TPS={final_metrics.get('tps')} tok/s | Total Time={final_metrics.get('total_time_s')}s")
                break

            elif msg_type == "error":
                print(f"\n[EVENT: ERROR] {data.get('message')}")
                break

        assert len(citations_received) > 0, "Failed: No citations received"
        assert len(tokens_received) > 0, "Failed: No tokens received"
        print("\nLIVE WEBSOCKET STREAMING TEST PASSED PERFECTLY!")

if __name__ == "__main__":
    asyncio.run(test_live_chat())
