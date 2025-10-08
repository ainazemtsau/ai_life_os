"""create milestones table

Revision ID: b1c2d3e4f5a6
Revises: a0a435409c64
Create Date: 2025-10-07 14:00:00.000000

"""

from collections.abc import Sequence

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID

# revision identifiers, used by Alembic.
revision: str = "b1c2d3e4f5a6"
down_revision: str | Sequence[str] | None = "a0a435409c64"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "milestones",
        sa.Column(
            "id", UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")
        ),
        sa.Column("goal_id", UUID(as_uuid=True), nullable=False),
        sa.Column("title", sa.String(255), nullable=False),
        sa.Column("due", sa.DateTime(timezone=True), nullable=True),
        sa.Column("status", sa.String(50), nullable=False, server_default=sa.text("'todo'")),
        sa.Column("demo_criterion", sa.String(255), nullable=False),
        sa.Column("blocking", sa.Boolean(), nullable=False, server_default=sa.text("false")),
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
        sa.CheckConstraint("LENGTH(TRIM(title)) > 0", name="check_milestone_title_not_empty"),
        sa.CheckConstraint(
            "LENGTH(TRIM(demo_criterion)) > 0", name="check_milestone_demo_criterion_not_empty"
        ),
        sa.CheckConstraint(
            "status IN ('todo', 'doing', 'done', 'blocked')", name="check_milestone_status"
        ),
        sa.ForeignKeyConstraint(["goal_id"], ["goals.id"], ondelete="CASCADE"),
    )

    # Indexes for filtering and sorting
    op.create_index("idx_milestones_goal_id", "milestones", ["goal_id"])
    op.create_index("idx_milestones_status", "milestones", ["status"])
    op.create_index("idx_milestones_due", "milestones", ["due"])
    op.create_index("idx_milestones_blocking", "milestones", ["blocking"])
    op.create_index("idx_milestones_date_created", "milestones", [sa.text("date_created DESC")])


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index("idx_milestones_date_created", table_name="milestones")
    op.drop_index("idx_milestones_blocking", table_name="milestones")
    op.drop_index("idx_milestones_due", table_name="milestones")
    op.drop_index("idx_milestones_status", table_name="milestones")
    op.drop_index("idx_milestones_goal_id", table_name="milestones")
    op.drop_table("milestones")
