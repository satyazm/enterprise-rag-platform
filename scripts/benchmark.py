#!/usr/bin/env python3
"""Retrieval benchmark script."""

import asyncio
import time

QUERIES = [
    "What is the data retention policy?",
    "How do I request dashboard access?",
    "What are on-call escalation procedures?",
]


async def benchmark():
    print("Enterprise RAG Retrieval Benchmark")
    print("=" * 40)
    for q in QUERIES:
        start = time.perf_counter()
        # Simulated latency for demo
        await asyncio.sleep(0.1)
        elapsed = (time.perf_counter() - start) * 1000
        print(f"Query: {q[:50]:<50} {elapsed:.1f}ms")


if __name__ == "__main__":
    asyncio.run(benchmark())
