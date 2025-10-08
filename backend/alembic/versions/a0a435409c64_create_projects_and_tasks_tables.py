"""create projects and tasks tables

Revision ID: a0a435409c64
Revises: 56a4fa4b8a43
Create Date: 2025-10-07 12:00:00.000000

"""

from collections.abc import Sequence

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID, ARRAY

# revision identifiers, used by Alembic.
revision: str = "a0a435409c64"
down_revision: str | Sequence[str] | None = "56a4fa4b8a43"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    # Create projects table
    op.create_table(
        "projects",
        sa.Column(
            "id", UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")
        ),
        sa.Column("goal_id", UUID(as_uuid=True), nullable=True),
        sa.Column("title", sa.String(255), nullable=False),
        sa.Column("status", sa.String(50), nullable=False, server_default=sa.text("'todo'")),
        sa.Column("priority", sa.String(10), nullable=False),
        sa.Column("scope", sa.Text(), nullable=False),
        sa.Column("risk", sa.String(10), nullable=False),
        sa.Column("tags", ARRAY(sa.String()), nullable=False, server_default=sa.text("'{}'")),
        sa.Column("dependencies", ARRAY(UUID()), nullable=False, server_default=sa.text("'{}'")),
        sa.Column(
            "date_created", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()
        ),
        sa.Column(
            "date_updated",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.func.now(),
            onupdate=sa.func.now(),
        ),
        sa.CheckConstraint("LENGTH(TRIM(title)) > 0", name="check_project_title_not_empty"),
        sa.CheckConstraint(
            "status IN ('todo', 'doing', 'done', 'blocked')", name="check_project_status"
        ),
        sa.CheckConstraint("priority IN ('P0', 'P1', 'P2', 'P3')", name="check_project_priority"),
        sa.CheckConstraint("risk IN ('green', 'yellow', 'red')", name="check_project_risk"),
        sa.ForeignKeyConstraint(["goal_id"], ["goals.id"], ondelete="SET NULL"),
    )

    # Create indexes for projects
    op.create_index("idx_projects_goal_id", "projects", ["goal_id"])
    op.create_index("idx_projects_status", "projects", ["status"])
    op.create_index("idx_projects_date_created", "projects", [sa.text("date_created DESC")])

    # Create tasks table
    op.create_table(
        "tasks",
        sa.Column(
            "id", UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")
        ),
        sa.Column("project_id", UUID(as_uuid=True), nullable=False),
        sa.Column("title", sa.String(255), nullable=False),
        sa.Column("status", sa.String(50), nullable=False, server_default=sa.text("'todo'")),
        sa.Column("dependencies", ARRAY(UUID()), nullable=False, server_default=sa.text("'{}'")),
        sa.Column("size", sa.String(10), nullable=False),
        sa.Column("energy", sa.String(20), nullable=False),
        sa.Column("continuity", sa.String(20), nullable=False),
        sa.Column("clarity", sa.String(20), nullable=False),
        sa.Column("risk", sa.String(10), nullable=False),
        sa.Column("context", sa.Text(), nullable=False, server_default=sa.text("''")),
        sa.Column(
            "date_created", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()
        ),
        sa.Column(
            "date_updated",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.func.now(),
            onupdate=sa.func.now(),
        ),
        sa.CheckConstraint("LENGTH(TRIM(title)) > 0", name="check_task_title_not_empty"),
        sa.CheckConstraint(
            "status IN ('todo', 'doing', 'done', 'blocked')", name="check_task_status"
        ),
        sa.CheckConstraint("size IN ('XS', 'S', 'M', 'L', 'XL')", name="check_task_size"),
        sa.CheckConstraint(
            "energy IN ('Deep', 'Focus', 'Light')", name="check_task_energy"
        ),
        sa.CheckConstraint(
            "continuity IN ('chain', 'linked', 'puzzle')", name="check_task_continuity"
        ),
        sa.CheckConstraint(
            "clarity IN ('clear', 'cloudy', 'unknown')", name="check_task_clarity"
        ),
        sa.CheckConstraint("risk IN ('green', 'yellow', 'red')", name="check_task_risk"),
        sa.ForeignKeyConstraint(["project_id"], ["projects.id"], ondelete="CASCADE"),
    )

    # Create indexes for tasks
    op.create_index("idx_tasks_project_id", "tasks", ["project_id"])
    op.create_index("idx_tasks_status", "tasks", ["status"])
    op.create_index("idx_tasks_date_created", "tasks", [sa.text("date_created DESC")])


def downgrade() -> None:
    """Downgrade schema."""
    # Drop tasks table and indexes
    op.drop_index("idx_tasks_date_created", table_name="tasks")
    op.drop_index("idx_tasks_status", table_name="tasks")
    op.drop_index("idx_tasks_project_id", table_name="tasks")
    op.drop_table("tasks")

    # Drop projects table and indexes
    op.drop_index("idx_projects_date_created", table_name="projects")
    op.drop_index("idx_projects_status", table_name="projects")
    op.drop_index("idx_projects_goal_id", table_name="projects")
    op.drop_table("projects")
