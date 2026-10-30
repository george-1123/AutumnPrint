import os
from dataclasses import dataclass, field
from pathlib import Path

from platformdirs import user_data_path


@dataclass(frozen=True)
class Settings:
    mode: str
    workspace: str
    database_url: str = field(repr=False)
    desktop_token: str = field(repr=False)
    edge_token: str = field(repr=False)
    broker_url: str = field(default="", repr=False)

    def __post_init__(self):
        if self.mode not in {"personal", "enterprise"}:
            raise ValueError("AUTUMN_MODE must be personal or enterprise")
        if not self.workspace or len(self.workspace) > 64:
            raise ValueError("workspace must contain 1 to 64 characters")
        if min(len(self.desktop_token), len(self.edge_token)) < 32:
            raise ValueError("independent desktop and edge tokens must be at least 32 characters")
        if self.desktop_token == self.edge_token:
            raise ValueError("desktop and edge credentials must differ")
        if self.mode == "personal" and not self.database_url.startswith("sqlite:///"):
            raise ValueError("personal mode requires SQLite")
        if self.mode == "enterprise" and (
            not self.database_url.startswith("postgresql+psycopg://")
            or not self.broker_url.startswith(("redis://", "rediss://"))
        ):
            raise ValueError("enterprise requires PostgreSQL/psycopg and Redis")

    @classmethod
    def from_env(cls):
        data = user_data_path("AutumnPrint", appauthor=False)
        if not os.getenv("AUTUMN_DATABASE_URL"):
            data.mkdir(parents=True, exist_ok=True)
        return cls(
            mode=os.getenv("AUTUMN_MODE", "personal"),
            workspace=os.getenv("AUTUMN_WORKSPACE", "personal"),
            database_url=os.getenv(
                "AUTUMN_DATABASE_URL", f"sqlite:///{Path(data) / 'autumn.sqlite'}"
            ),
            desktop_token=os.getenv("AUTUMN_DESKTOP_TOKEN", ""),
            edge_token=os.getenv("AUTUMN_EDGE_TOKEN", ""),
            broker_url=os.getenv("AUTUMN_BROKER_URL", ""),
        )
