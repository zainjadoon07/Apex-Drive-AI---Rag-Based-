"""
benchmark.py - Retrieval Latency and Quality Benchmark Suite for Apex Car Rental RAG.
Evaluates Dense, Sparse (BM25), Hybrid (RRF), and Cached retrieval across 50 realistic queries.
"""

import time
import json
import statistics
from pathlib import Path
from typing import List, Dict

from retrieval import retrieval_engine, RetrievalResult

BENCHMARK_QUERIES = [
    # 1-10: Fleet & Rates
    "What is the daily rate and luggage capacity for the Toyota Corolla?",
    "How many seats does the Ford Explorer have?",
    "What is the range of the Tesla Model 3 RWD?",
    "What is the daily price for the Luxury Sedan BMW 5 Series?",
    "Do you have minivans that seat 7 or 8 passengers?",
    "Can I rent a 12-passenger van without a CDL?",
    "What kind of fuel does the Chevy Tahoe require?",
    "Are there convertible sports cars like Mustang GT available?",
    "Is mileage unlimited on the economy cars?",
    "What are the luggage dimensions for the Compact SUV RAV4?",

    # 11-20: Insurance & Protection
    "What is the deductible on the Standard Protection plan?",
    "How much does the Silver Protection cost per day?",
    "What does Gold Platinum cover and what is the deductible?",
    "Does Gold Platinum include free roadside assistance?",
    "What is the difference between CDW and personal auto insurance?",
    "What is the liability limit on Supplemental Liability Insurance SLI?",
    "Are windshield chips covered under Silver Protection?",
    "How does credit card rental car insurance work at Apex?",
    "What happens if an unauthorized driver crashes the car?",
    "Are stolen laptops covered under Personal Effects Coverage PEC?",

    # 21-30: Pricing, Fees & Deposits
    "What is the young driver surcharge for 22 year olds?",
    "Can a 23-year-old rent a luxury BMW 5 Series?",
    "How much is the security deposit hold on a credit card?",
    "Can I use a debit card for the security deposit?",
    "What is the fee if I return the car without a full tank?",
    "What battery percentage must I return an EV with?",
    "How much is the fee for an additional driver?",
    "Is my spouse exempt from the additional driver fee?",
    "How does the electronic toll transponder E-Pass work?",
    "What is the cancellation policy for pre-paid bookings?",

    # 31-40: Eligibility & Policies
    "What is the minimum age to rent a car?",
    "Do you accept International Driving Permits IDP?",
    "Can I drive the car across the border into Canada?",
    "Can I drive into Mexico from San Diego?",
    "What is the one-way drop charge between cities?",
    "What are the benefits of the Apex Rewards Black Tier?",
    "What is the fee if someone smokes or vapes in the car?",
    "Can I bring my pet dog in the rental car?",
    "What is the grace period for returning the car late?",
    "Can I use the rental vehicle for Uber or DoorDash?",

    # 41-45: Emergencies & Roadside
    "What should I do if the check engine light starts flashing?",
    "What is the procedure if I get a flat tire on a Tesla?",
    "What is the phone number for 24/7 roadside assistance?",
    "How much does it cost if I lose the electronic key fob?",
    "Do I need a police report if someone dents the car in a parking lot?",

    # 46-50: Locations & Fallback Edge Cases
    "Where is the Apex rental counter at JFK Federal Circle?",
    "How do I reach the O'Hare ORD consolidated rental center?",
    "Where do I pick up the shuttle at Los Angeles LAX?",
    "Can you write a Python quicksort algorithm for me?",       # Out-of-Domain Guardrail Test
    "What is the recipe for chocolate chip cookies?"           # Out-of-Domain Guardrail Test
]


def run_benchmark():
    print("=" * 70)
    print(" Apex Car Rental RAG Retrieval Latency & Quality Benchmark Suite ")
    print("=" * 70)

    # 1. Warm-up and load index
    print("\n[1/4] Loading index and warming up embedding model...")
    t0 = time.perf_counter()
    retrieval_engine.load_index()
    print(f"Index loaded in {(time.perf_counter() - t0):.2f}s ({len(retrieval_engine.chunks)} chunks)")

    modes = ["dense", "sparse", "hybrid"]
    results_by_mode: Dict[str, List[float]] = {m: [] for m in modes}
    results_by_mode["cached"] = []

    # 2. Benchmark each mode across all 50 queries
    for mode in modes:
        retrieval_engine.cache.clear()
        print(f"\n[Benchmarking Mode: '{mode.upper()}'] Running {len(BENCHMARK_QUERIES)} queries...")
        latencies = []

        for q in BENCHMARK_QUERIES:
            res = retrieval_engine.retrieve(q, mode=mode, top_k=4)
            latencies.append(res.latency_ms)

        results_by_mode[mode] = latencies

    # 3. Benchmark Cached queries (second pass on hybrid)
    print("\n[Benchmarking Mode: 'CACHED (LRU)'] Running 50 repeated queries...")
    cached_latencies = []
    for q in BENCHMARK_QUERIES:
        res = retrieval_engine.retrieve(q, mode="hybrid", top_k=4)
        cached_latencies.append(res.latency_ms)
    results_by_mode["cached"] = cached_latencies

    # 4. Generate Statistical Summary Table
    print("\n" + "=" * 70)
    print(f"{'Mode':<15} | {'Mean (ms)':<10} | {'P50 (ms)':<10} | {'P95 (ms)':<10} | {'P99 (ms)':<10} | {'Min (ms)':<9} | {'Max (ms)':<9}")
    print("-" * 75)

    stats_summary = {}
    for mode, lats in results_by_mode.items():
        mean_v = statistics.mean(lats)
        median_v = statistics.median(lats)
        sorted_lats = sorted(lats)
        p95_idx = int(0.95 * len(sorted_lats))
        p99_idx = int(0.99 * len(sorted_lats))
        p95_v = sorted_lats[min(p95_idx, len(sorted_lats) - 1)]
        p99_v = sorted_lats[min(p99_idx, len(sorted_lats) - 1)]
        min_v = min(lats)
        max_v = max(lats)

        stats_summary[mode] = {
            "mean": round(mean_v, 2),
            "p50": round(median_v, 2),
            "p95": round(p95_v, 2),
            "p99": round(p99_v, 2),
            "min": round(min_v, 2),
            "max": round(max_v, 2)
        }

        print(f"{mode.upper():<15} | {mean_v:<10.2f} | {median_v:<10.2f} | {p95_v:<10.2f} | {p99_v:<10.2f} | {min_v:<9.2f} | {max_v:<9.2f}")

    print("=" * 70)
    print("TARGET VERIFICATION: Target retrieval latency is < 1,000 ms (1.0s).")
    mean_hybrid = stats_summary["hybrid"]["mean"]
    if mean_hybrid < 1000.0:
        print(f"PASS: Hybrid mean latency is {mean_hybrid:.2f} ms ({(1000.0 / max(mean_hybrid, 0.001)):.1f}x faster than requirement!)")
    else:
        print(f"FAIL: Latency exceeded 1000ms.")

    # Save benchmark results to file for README and audit
    bench_file = Path(__file__).resolve().parent / "benchmark_results.json"
    with open(bench_file, "w", encoding="utf-8") as f:
        json.dump(stats_summary, f, indent=2)
    print(f"\nSaved benchmark metrics to {bench_file}")

    # 5. Hybrid Search Quality Demonstration
    print("\n" + "=" * 70)
    print(" BONUS DEMONSTRATION: Hybrid Search (BM25 + Dense RRF) vs Dense-Only ")
    print("=" * 70)
    demo_queries = [
        ("Acronym / Exact Code Query", "What is the liability limit on SLI?"),
        ("Conceptual Semantic Query", "Can my 22-year-old college sibling drive our rental car?"),
        ("Model / Number Query", "What is the range on the Tesla Model 3 RWD?"),
        ("Out of Domain Guardrail", "Write a python quicksort function")
    ]

    for label, query in demo_queries:
        print(f"\n>>> [{label}]: '{query}'")
        res_hybrid = retrieval_engine.retrieve(query, mode="hybrid", top_k=2)
        res_dense = retrieval_engine.retrieve(query, mode="dense", top_k=2)
        res_sparse = retrieval_engine.retrieve(query, mode="sparse", top_k=2)

        print(f"  * Hybrid Top Hit: {res_hybrid.chunks[0]['source_file'] if res_hybrid.chunks else 'None (Non-relevant/Fallback)'}")
        print(f"  * Dense  Top Hit: {res_dense.chunks[0]['source_file'] if res_dense.chunks else 'None'}")
        print(f"  * Sparse Top Hit: {res_sparse.chunks[0]['source_file'] if res_sparse.chunks else 'None'}")
        print(f"  * Relevance Decision: is_relevant={res_hybrid.is_relevant} | Latency: {res_hybrid.latency_ms:.2f}ms")


if __name__ == "__main__":
    run_benchmark()
