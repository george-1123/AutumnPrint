"""Durable diagnostic handoff; leases apply only to the explicitly Fake tool."""

import json
import time
from uuid import uuid4

from autumn_contracts import Command, Receipt, Task, TaskEvent
from sqlalchemy import (
    Column,
    Float,
    ForeignKey,
    Integer,
    MetaData,
    String,
    Table,
    Text,
    UniqueConstraint,
    create_engine,
    event,
    insert,
    select,
    update,
)
from sqlalchemy.exc import IntegrityError

metadata = MetaData()
tasks = Table(
    "tasks",
    metadata,
    Column("id", String(36), primary_key=True),
    Column("workspace", String(64), nullable=False),
    Column("request_key", String(128), nullable=False),
    Column("status", String(32), nullable=False),
    Column("result", Text),
    UniqueConstraint("workspace", "request_key"),
)
events = Table(
    "task_events",
    metadata,
    Column("sequence", Integer, primary_key=True, autoincrement=True),
    Column("task_id", ForeignKey("tasks.id"), nullable=False),
    Column("kind", String(64), nullable=False),
)
commands = Table(
    "edge_commands",
    metadata,
    Column("id", String(36), primary_key=True),
    Column("task_id", ForeignKey("tasks.id"), nullable=False, unique=True),
    Column("edge_id", String(64)),
    Column("lease_token", String(36)),
    Column("lease_until", Float, nullable=False, default=0),
    Column("done", Integer, nullable=False, default=0),
)
edges = Table(
    "edge_agents",
    metadata,
    Column("workspace", String(64), primary_key=True),
    Column("id", String(64), primary_key=True),
)


class Store:
    def __init__(self, database_url):
        self.engine = create_engine(database_url, pool_pre_ping=True)
        if self.engine.dialect.name == "sqlite":

            @event.listens_for(self.engine, "connect")
            def configure(connection, _):
                connection.execute("PRAGMA foreign_keys=ON")
                connection.execute("PRAGMA journal_mode=WAL")
                connection.execute("PRAGMA busy_timeout=5000")

    def submit(self, workspace, key):
        try:
            with self.engine.begin() as db:
                task_id = str(uuid4())
                db.execute(
                    insert(tasks).values(
                        id=task_id, workspace=workspace, request_key=key, status="queued"
                    )
                )
                db.execute(insert(events).values(task_id=task_id, kind="queued"))
        except IntegrityError:
            with self.engine.connect() as db:
                task_id = db.execute(
                    select(tasks.c.id).where(
                        tasks.c.workspace == workspace, tasks.c.request_key == key
                    )
                ).scalar_one()
        return self.get(workspace, task_id)

    def get(self, workspace, task_id):
        with self.engine.connect() as db:
            row = (
                db.execute(
                    select(tasks).where(tasks.c.id == task_id, tasks.c.workspace == workspace)
                )
                .mappings()
                .one_or_none()
            )
        if row is None:
            raise KeyError(task_id)
        return Task(
            id=row["id"],
            workspace=row["workspace"],
            status=row["status"],
            result=Receipt.model_validate_json(row["result"]) if row["result"] else None,
        )

    def list_tasks(self, workspace):
        with self.engine.connect() as db:
            ids = (
                db.execute(select(tasks.c.id).where(tasks.c.workspace == workspace)).scalars().all()
            )
        return [self.get(workspace, task_id) for task_id in ids]

    def task_events(self, workspace, task_id, after=0):
        self.get(workspace, task_id)
        with self.engine.connect() as db:
            rows = (
                db.execute(
                    select(events)
                    .where(
                        events.c.task_id == task_id,
                        events.c.sequence > after,
                    )
                    .order_by(events.c.sequence)
                )
                .mappings()
                .all()
            )
        return [TaskEvent(**row) for row in rows]

    def dispatch(self, workspace):
        # Atomic state transition is the queue claim; handoff and event commit together.
        with self.engine.begin() as db:
            ids = (
                db.execute(
                    select(tasks.c.id).where(
                        tasks.c.workspace == workspace, tasks.c.status == "queued"
                    )
                )
                .scalars()
                .all()
            )
            for task_id in ids:
                changed = db.execute(
                    update(tasks)
                    .where(tasks.c.id == task_id, tasks.c.status == "queued")
                    .values(status="waiting_edge")
                )
                if changed.rowcount:
                    db.execute(insert(commands).values(id=str(uuid4()), task_id=task_id))
                    db.execute(insert(events).values(task_id=task_id, kind="fake_model_completed"))
        return len(ids)

    def register(self, workspace, edge_id):
        try:
            with self.engine.begin() as db:
                db.execute(insert(edges).values(workspace=workspace, id=edge_id))
        except IntegrityError:
            pass

    def claim(self, workspace, edge_id):
        now = time.time()
        with self.engine.begin() as db:
            registered = db.execute(
                select(edges).where(edges.c.workspace == workspace, edges.c.id == edge_id)
            ).first()
            if registered is None:
                raise PermissionError("edge must register first")
            candidate = db.execute(
                select(commands.c.id, commands.c.task_id)
                .join(tasks)
                .where(
                    tasks.c.workspace == workspace,
                    commands.c.done == 0,
                    commands.c.lease_until < now,
                )
                .order_by(commands.c.id)
                .limit(1)
            ).first()
            if candidate is None:
                return None
            token = str(uuid4())
            changed = db.execute(
                update(commands)
                .where(
                    commands.c.id == candidate.id,
                    commands.c.done == 0,
                    commands.c.lease_until < now,
                )
                .values(edge_id=edge_id, lease_token=token, lease_until=now + 30)
            )
            if not changed.rowcount:
                return None
            return Command(id=candidate.id, task_id=candidate.task_id, lease_token=token)

    def complete(self, workspace, edge_id, command_id, token, receipt):
        with self.engine.begin() as db:
            row = (
                db.execute(
                    select(commands)
                    .join(tasks)
                    .where(
                        commands.c.id == command_id,
                        tasks.c.workspace == workspace,
                        commands.c.edge_id == edge_id,
                        commands.c.lease_token == token,
                    )
                )
                .mappings()
                .one_or_none()
            )
            if row is None:
                raise PermissionError("unknown command or lease")
            if row["done"]:
                return
            if row["lease_until"] < time.time():
                raise PermissionError("expired lease")
            changed = db.execute(
                update(commands)
                .where(commands.c.id == command_id, commands.c.done == 0)
                .values(done=1)
            )
            if changed.rowcount:
                db.execute(
                    update(tasks)
                    .where(tasks.c.id == row["task_id"])
                    .values(status="succeeded", result=json.dumps(receipt.model_dump()))
                )
                db.execute(
                    insert(events).values(task_id=row["task_id"], kind="fake_tool_completed")
                )
