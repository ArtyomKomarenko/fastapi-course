"""Update users table to make email unique

Revision ID: 52810959ed1e
Revises: d0e959f5843c
Create Date: 2025-08-18 20:22:46.284670

"""

from collections.abc import Sequence

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "52810959ed1e"
down_revision: str | Sequence[str] | None = "d0e959f5843c"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_unique_constraint(None, "users", ["email"])


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint(None, "users", type_="unique")
