"""generate company table

Revision ID: 4d92716d5aca
Revises: 
Create Date: 2023-04-30 08:18:16.667494

"""
from alembic import op
import sqlalchemy as sa
from schemas.base_entity import Mode, Rating
from datetime import datetime
from uuid import uuid4

# revision identifiers, used by Alembic.
revision = '4d92716d5aca'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    company_table = op.create_table(
        'companies',
        sa.Column('id', sa.UUID, nullable=False, primary_key=True),
        sa.Column('name', sa.String, nullable=False),
        sa.Column('description', sa.String, nullable=True),
        sa.Column('mode', sa.Enum(Mode), nullable=False, default=Mode.ACTIVE), 
        sa.Column('rating', sa.Enum(Rating), nullable=False, default=Rating.FIVE_STAR),
        sa.Column('created_at', sa.DateTime),
        sa.Column('updated_at', sa.DateTime)
    )

    # data seed
    op.bulk_insert(company_table, [
        {
            "id": uuid4(),
            "name": "Nashtech",
            "description": "Company description",
            "mode": Mode.ACTIVE,
            "rating": Rating.FIVE_STAR,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
    ])
    pass


def downgrade() -> None:
    op.drop_table("companies")
    op.execute("DROP TYPE mode;")
    op.execute("DROP TYPE rating;")
