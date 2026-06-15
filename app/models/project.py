from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class Project(Base):
    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(primary_key=True)

    workspace_id: Mapped[int] = mapped_column(
        ForeignKey("workspaces.id"),
        nullable=False
    )

    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    status: Mapped[str] = mapped_column(
        String(50),
        default="ACTIVE"
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )

    workspace = relationship(
        "Workspace",
        back_populates="projects"
    )

    tasks = relationship(
        "Task",
        back_populates="project",
        cascade="all, delete-orphan"
    )

    labels = relationship(
        "Label",
        back_populates="project",
        cascade="all, delete-orphan"
    )