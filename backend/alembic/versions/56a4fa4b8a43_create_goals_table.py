"""create goals table

Revision ID: 56a4fa4b8a43
Revises:
Create Date: 2025-10-05 06:00:48.497114

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID


# revision identifiers, used by Alembic.
revision: str = '56a4fa4b8a43'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'goals',
        sa.Column('id', UUID(as_uuid=True), primary_key=True, server_default=sa.text('gen_random_uuid()')),
        sa.Column('title', sa.String(255), nullable=False),
        sa.Column('is_done', sa.Boolean(), nullable=False, server_default=sa.text('false')),
        sa.Column('date_created', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column('date_updated', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now(), onupdate=sa.func.now()),
        sa.CheckConstraint("LENGTH(TRIM(title)) > 0", name='check_title_not_empty')
    )

    # Indexes for filtering and sorting
    op.create_index('idx_goals_is_done', 'goals', ['is_done'])
    op.create_index('idx_goals_date_updated', 'goals', [sa.text('date_updated DESC')])


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index('idx_goals_date_updated', table_name='goals')
    op.drop_index('idx_goals_is_done', table_name='goals')
    op.drop_table('goals')
