"""generate task table

Revision ID: 8b0ef6ea7cd0
Revises: 1c8a9b800565
Create Date: 2023-05-02 20:56:05.142581

"""
from alembic import op
import sqlalchemy as sa
from schemas.base_entity import Priority, Status
from sqlalchemy.orm import Session
from schemas.user import User
from uuid import uuid4
from datetime import datetime
from schemas.base_entity import Status, Priority

# revision identifiers, used by Alembic.
revision = '8b0ef6ea7cd0'
down_revision = '553782a89622'
branch_labels = None
depends_on = None


def upgrade() -> None:
    task_table = op.create_table(
        'tasks',
        sa.Column('id', sa.UUID, nullable=False, primary_key=True),
        sa.Column('summary', sa.String, nullable=False),
        sa.Column('description', sa.String, nullable=True),
        sa.Column('status', sa.Enum(Status), nullable=False, default=Status.OPEN), 
        sa.Column('priority', sa.Enum(Priority), nullable=False, default=Priority.LOW), 
        sa.Column('created_at', sa.DateTime),
        sa.Column('updated_at', sa.DateTime),
        sa.Column('owner_id', sa.UUID, nullable=False),
    )

    # data seed
    bind = op.get_bind()
    session = Session(bind=bind)
    admin = session.query(User).filter(User.username == "admin").first()
    normal_user = session.query(User).filter(User.username == "user").first()

    op.bulk_insert(task_table, [
        {
            "id": uuid4(),
            "summary": "admin task",
            "description": "admin task description",
            "status": Status.OPEN,
            "priority": Priority.MEDIUM,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
            "owner_id": admin.id
        },
        {
            "id": uuid4(),
            "summary": "user task",
            "description": "user task description",
            "status": Status.OPEN,
            "priority": Priority.MEDIUM,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
            "owner_id": normal_user.id
        }
    ])
    pass


def downgrade() -> None:
    op.drop_table("tasks")
    op.execute("DROP TYPE status;")
    op.execute("DROP TYPE priority;")
    pass
