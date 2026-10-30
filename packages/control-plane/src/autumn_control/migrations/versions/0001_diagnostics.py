"""Initial immutable diagnostic schema, SQLite and PostgreSQL."""

import sqlalchemy as sa
from alembic import op

revision = "0001"
down_revision = None


def upgrade():
    op.create_table(
        "tasks",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("workspace", sa.String(64), nullable=False),
        sa.Column("request_key", sa.String(128), nullable=False),
        sa.Column("status", sa.String(32), nullable=False),
        sa.Column("result", sa.Text),
        sa.UniqueConstraint("workspace", "request_key"),
    )
    op.create_table(
        "task_events",
        sa.Column("sequence", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("task_id", sa.String(36), sa.ForeignKey("tasks.id"), nullable=False),
        sa.Column("kind", sa.String(64), nullable=False),
    )
    op.create_table(
        "edge_commands",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("task_id", sa.String(36), sa.ForeignKey("tasks.id"), nullable=False, unique=True),
        sa.Column("edge_id", sa.String(64)),
        sa.Column("lease_token", sa.String(36)),
        sa.Column("lease_until", sa.Float, nullable=False),
        sa.Column("done", sa.Integer, nullable=False),
    )
    op.create_table(
        "edge_agents",
        sa.Column("workspace", sa.String(64), primary_key=True),
        sa.Column("id", sa.String(64), primary_key=True),
    )


def downgrade():
    for name in ("edge_agents", "edge_commands", "task_events", "tasks"):
        op.drop_table(name)
