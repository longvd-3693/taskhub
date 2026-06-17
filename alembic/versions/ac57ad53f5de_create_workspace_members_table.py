from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql


revision: str = "ac57ad53f5de"
down_revision: Union[str, Sequence[str], None] = "19dc1945fab5"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


workspace_member_role_enum = postgresql.ENUM(
    "OWNER",
    "EDITOR",
    "VIEWER",
    name="workspacememberrole",
)


def upgrade() -> None:
    workspace_member_role_enum.create(
        op.get_bind(),
        checkfirst=True,
    )

    op.create_table(
        "workspace_members",
        sa.Column("workspace_id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("role", workspace_member_role_enum, nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.ForeignKeyConstraint(["workspace_id"], ["workspaces.id"]),
        sa.PrimaryKeyConstraint("workspace_id", "user_id"),
    )


def downgrade() -> None:
    op.drop_table("workspace_members")

    workspace_member_role_enum.drop(
        op.get_bind(),
        checkfirst=True,
    )
