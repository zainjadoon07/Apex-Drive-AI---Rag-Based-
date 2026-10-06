"""
test_e2e.py - Verification script testing RAG retrieval, prompt assembly, and fallback handling.
"""

from retrieval import retrieval_engine
from prompts import build_rag_prompt_messages

def test_system():
    print("Loading RAG retrieval engine...")
    retrieval_engine.load_index()
    print(f"Loaded {len(retrieval_engine.chunks)} chunks from 75 documents.")

    # Test 1: Grounded Fleet Query
    q1 = "What is the daily rate and luggage capacity for the Toyota Corolla?"
    res1 = retrieval_engine.retrieve(q1, mode="hybrid", top_k=3)
    print("\n--- Test 1: Grounded Fleet Query ---")
    print(f"Query: {q1}")
    print(f"Latency: {res1.latency_ms} ms | Relevant: {res1.is_relevant}")
    print(f"Top Source: {res1.citations[0]['source_file']} - {res1.citations[0]['title']}")
    context_str = res1.format_context_for_prompt()
    prompt1 = build_rag_prompt_messages([], q1, context_str, res1.is_relevant)
    assert res1.is_relevant is True, "Test 1 failed: Should be relevant"
    assert "Corolla" in context_str, "Test 1 failed: Context should mention Corolla"
    print("PASS: Grounded context retrieved and injected into prompt.")

    # Test 2: Insurance & Zero Deductible Query
    q2 = "What does Gold Platinum cover and what is the deductible?"
    res2 = retrieval_engine.retrieve(q2, mode="hybrid", top_k=3)
    print("\n--- Test 2: Insurance Query ---")
    print(f"Query: {q2}")
    print(f"Latency: {res2.latency_ms} ms | Relevant: {res2.is_relevant}")
    print(f"Top Source: {res2.citations[0]['source_file']} - {res2.citations[0]['title']}")
    assert "insurance_03_gold_platinum_zero_deductible.md" in [c["source_file"] for c in res2.citations], "Test 2 failed"
    print("PASS: Correct Gold Platinum document retrieved.")

    # Test 3: Out-of-Domain Guardrail Fallback
    q3 = "Can you help me solve this calculus differential equation?"
    res3 = retrieval_engine.retrieve(q3, mode="hybrid", top_k=3)
    print("\n--- Test 3: Out-of-Domain Query ---")
    print(f"Query: {q3}")
    print(f"Latency: {res3.latency_ms} ms | Relevant: {res3.is_relevant}")
    assert res3.is_relevant is False, "Test 3 failed: Out of domain should NOT be marked relevant"
    prompt3 = build_rag_prompt_messages([], q3, "", res3.is_relevant)
    assert "=== RETRIEVED DOMAIN CONTEXT ===\nUse the following verified internal documents" not in prompt3[0]["content"], "Test 3 failed: Should not inject context"
    print("PASS: Out-of-domain properly identified as irrelevant and fallback preserved.")

    # Test 4: Cache Hit Speed
    q4 = q1
    res4 = retrieval_engine.retrieve(q4, mode="hybrid", top_k=3)
    print("\n--- Test 4: Cache Hit ---")
    print(f"Latency: {res4.latency_ms} ms | Cached: {res4.is_cached}")
    assert res4.is_cached is True, "Test 4 failed: Query should be cached"
    assert res4.latency_ms < 1.0, "Test 4 failed: Cache hit should be sub-millisecond"
    print("PASS: LRU Cache hit verified (< 1ms).")

    print("\n" + "=" * 50)
    print("ALL 4 INTEGRATION TESTS PASSED SUCCESSFULLY!")
    print("=" * 50)

if __name__ == "__main__":
    test_system()
