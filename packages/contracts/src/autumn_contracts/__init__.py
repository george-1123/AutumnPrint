"""Versioned process boundary. No persistence or hardware imports."""

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

PROTOCOL_VERSION = "1"


class Contract(BaseModel):
    model_config = ConfigDict(extra="forbid")


class DiagnosticRequest(Contract):
    idempotency_key: str = Field(min_length=1, max_length=128, pattern=r"^[\w-]+$")


class Receipt(Contract):
    protocol_version: Literal["1"] = "1"
    simulated: Literal[True] = True
    tool: Literal["fake-diagnostic"] = "fake-diagnostic"
    message: str = Field(max_length=256)


class Task(Contract):
    id: str
    workspace: str
    status: Literal["queued", "waiting_edge", "succeeded"]
    result: Receipt | None = None


class TaskEvent(Contract):
    sequence: int
    task_id: str
    kind: str


class EdgeRegistration(Contract):
    protocol_version: Literal["1"] = "1"
    edge_id: str = Field(min_length=1, max_length=64, pattern=r"^[\w-]+$")


class Command(Contract):
    id: str
    task_id: str
    lease_token: str
    protocol_version: Literal["1"] = "1"
    tool: Literal["fake-diagnostic"] = "fake-diagnostic"


class CompleteCommand(Contract):
    lease_token: str
    receipt: Receipt
