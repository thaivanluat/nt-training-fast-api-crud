"""generate user table

Revision ID: 553782a89622
Revises: 4d92716d5aca
Create Date: 2023-04-30 08:30:51.443927

"""
from alembic import op
import sqlalchemy as sa
from uuid import uuid4
from datetime import datetime
from schemas.user import get_password_hash
from settings import ADMIN_DEFAULT_PASSWORD
from schemas.company import Company
from sqlalchemy.orm import Session

# revision identifiers, used by Alembic.
revision = '553782a89622'
down_revision = '4d92716d5aca'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # User Table
    user_table = op.create_table(
        "users",
        sa.Column('id', sa.UUID, nullable=False, primary_key=True),
        sa.Column("email", sa.String, unique=True, nullable=True, index=True),
        sa.Column("username", sa.String, unique=True, index=True),
        sa.Column("first_name", sa.String),
        sa.Column("last_name", sa.String),
        sa.Column("hashed_password", sa.String),
        sa.Column("is_active", sa.Boolean, default=True),
        sa.Column("is_admin", sa.Boolean, default=False),
        sa.Column("created_at", sa.DateTime),
        sa.Column("updated_at", sa.DateTime),
        sa.Column('company_id', sa.UUID, nullable=False),
    )

    op.create_foreign_key('fk_user_company', 'users', 'companies', ['company_id'], ['id'])

    # data seed
    bind = op.get_bind()
    session = Session(bind=bind)
    company = session.query(Company).filter(Company.name == "Nashtech").first()

    op.bulk_insert(user_table, [
        {
            "id": uuid4(),
            "email": "thaivanluat@gmail.com",
            "username": "admin",
            "hashed_password": get_password_hash(ADMIN_DEFAULT_PASSWORD),
            "first_name": "Thai Van",
            "last_name": "Luat",
            "is_active": True,
            "is_admin": True,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
            "company_id": company.id
        },
        {
            "id": uuid4(),
            "email": "thaivanluat2@gmail.com",
            "username": "user",
            "hashed_password": get_password_hash(ADMIN_DEFAULT_PASSWORD),
            "first_name": "Normal user",
            "last_name": "",
            "is_active": True,
            "is_admin": False,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
            "company_id": company.id
        }
    ])
    pass


def downgrade() -> None:
    op.drop_table("users")
    pass
