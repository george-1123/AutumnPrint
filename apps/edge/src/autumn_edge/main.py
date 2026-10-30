import os
import sqlite3
import time

import httpx
from autumn_contracts import Command, CompleteCommand, Receipt


def run_once(client, edge_id, journal):
    client.post(
        "/edge/register", json={"edge_id": edge_id, "protocol_version": "1"}
    ).raise_for_status()
    response = client.post(f"/edge/{edge_id}/claim")
    response.raise_for_status()
    if response.json() is None:
        return False
    command = Command.model_validate(response.json())
    journal.execute("CREATE TABLE IF NOT EXISTS receipts (id TEXT PRIMARY KEY, body TEXT NOT NULL)")
    cached = journal.execute("SELECT body FROM receipts WHERE id=?", (command.id,)).fetchone()
    receipt = (
        Receipt.model_validate_json(cached[0])
        if cached
        else Receipt(message="Fake tool completed; no printer or model service was contacted.")
    )
    if not cached:
        journal.execute(
            "INSERT INTO receipts VALUES (?, ?)", (command.id, receipt.model_dump_json())
        )
        journal.commit()
    body = CompleteCommand(lease_token=command.lease_token, receipt=receipt)
    client.post(
        f"/edge/{edge_id}/commands/{command.id}/complete", json=body.model_dump()
    ).raise_for_status()
    return True


def main():
    token = os.environ["AUTUMN_EDGE_TOKEN"]
    if len(token) < 32:
        raise SystemExit("edge token must be at least 32 characters")
    with httpx.Client(
        base_url=os.environ["AUTUMN_API_URL"],
        headers={"Authorization": f"Bearer {token}"},
        timeout=10,
    ) as client:
        with sqlite3.connect(os.environ["AUTUMN_EDGE_JOURNAL"]) as journal:
            try:
                while True:
                    try:
                        run_once(client, "local-fake", journal)
                    except httpx.TransportError:
                        time.sleep(1)
                    time.sleep(0.25)
            except KeyboardInterrupt:
                pass


if __name__ == "__main__":
    main()
