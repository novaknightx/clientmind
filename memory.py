import requests
import os

HINDSIGHT_BASE = "https://api.hindsight.vectorize.io"

HEADERS = {
    "Authorization": f"Bearer {os.getenv('HINDSIGHT_API_KEY')}",
    "Content-Type": "application/json"
}


def retain(client_id: str, content: str):
    """Save a memory about a client."""

    payload = {
        "items": [
            {
                "content": content
            }
        ]
    }

    response = requests.post(
        f"{HINDSIGHT_BASE}/v1/default/banks/{client_id}/memories",
        json=payload,
        headers=HEADERS
    )

    response.raise_for_status()
    return response.json()


def recall(client_id: str, query: str):
    """Retrieve relevant memories about a client."""

    payload = {
        "query": query
    }

    response = requests.post(
        f"{HINDSIGHT_BASE}/v1/default/banks/{client_id}/memories/recall",
        json=payload,
        headers=HEADERS
    )

    response.raise_for_status()
    return response.json()