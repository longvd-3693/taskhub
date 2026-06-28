from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql


revision: str = "19dc1945fab5"
down_revision: Union[str, Sequence[str], None] = "4a13304de144"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


user_role_enum = postgresql.ENUM(
    "ADMIN",
    "MEMBER",
    name="userrole",
)


def upgrade() -> None:
    user_role_enum.create(
        op.get_bind(),
        checkfirst=True,
    )

    op.add_column(
        "users",
        sa.Column(
            "role",
            user_role_enum,
            nullable=False,
            server_default="MEMBER",
        ),
    )

    op.alter_column(
        "users",
        "role",
        server_default=None,
    )


def downgrade() -> None:
    op.drop_column("users", "role")

    user_role_enum.drop(
        op.get_bind(),
        checkfirst=True,
    )
