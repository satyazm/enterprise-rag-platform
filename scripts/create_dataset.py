#!/usr/bin/env python3
"""Create evaluation dataset files."""

import json
import os

DATASET = [
    {
        "question": "What is our data retention policy?",
        "ground_truth": "Customer data is retained for 7 years per compliance requirements.",
    },
    {
        "question": "How do I request access to the analytics dashboard?",
        "ground_truth": "Submit a ticket to IT with your manager's approval.",
    },
]

out_dir = os.path.join(os.path.dirname(__file__), "..", "evaluation", "datasets")
os.makedirs(out_dir, exist_ok=True)

with open(os.path.join(out_dir, "sample.json"), "w") as f:
    json.dump(DATASET, f, indent=2)

print(f"Created dataset at {out_dir}/sample.json")
