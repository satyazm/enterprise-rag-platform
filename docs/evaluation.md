# Evaluation

## Metrics

- **Faithfulness**: Answer grounded in retrieved context
- **Answer Relevancy**: Query-answer term overlap
- **Context Precision**: Retrieval quality
- **Groundedness**: Alignment with ground truth (when available)

## Running Evaluations

```bash
make eval
# or via API
curl -X POST http://localhost:8000/api/v1/admin/evaluate \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"dataset_name": "sample"}'
```

## Datasets

Sample datasets live in `evaluation/datasets/`. Add custom JSON files and reference them by name.
