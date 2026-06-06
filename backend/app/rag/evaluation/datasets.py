SAMPLE_DATASET = [
    {
        "question": "What is our data retention policy?",
        "ground_truth": "Customer data is retained for 7 years per compliance requirements.",
        "contexts": ["All customer records must be retained for a minimum of 7 years to meet SOC2 and GDPR compliance."],
    },
    {
        "question": "How do I request access to the analytics dashboard?",
        "ground_truth": "Submit a ticket to IT with your manager's approval.",
        "contexts": ["Analytics dashboard access requires manager approval and an IT service desk ticket under category 'Data Access'."],
    },
    {
        "question": "What are the on-call escalation procedures?",
        "ground_truth": "Page L1, escalate to L2 after 15 minutes, L3 after 30 minutes.",
        "contexts": ["On-call L1 responds within 5 min. Escalate to L2 after 15 min unacknowledged. L3 after 30 min for P1 incidents."],
    },
]


def get_dataset(name: str) -> list[dict]:
    datasets = {"sample": SAMPLE_DATASET}
    return datasets.get(name, SAMPLE_DATASET)
