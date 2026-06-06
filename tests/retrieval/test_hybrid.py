from app.rag.retrieval.hybrid import _fuse_results


def test_fuse_results_combines_scores():
    vector = [{"document_id": "1", "chunk_index": 0, "content": "a", "score": 1.0}]
    bm25 = [{"document_id": "1", "chunk_index": 0, "content": "a", "score": 0.5}]
    fused = _fuse_results(vector, bm25, alpha=0.5)
    assert len(fused) == 1
    assert "hybrid_score" in fused[0]
