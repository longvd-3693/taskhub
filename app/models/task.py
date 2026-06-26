from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base
from app.models.task_label import task_labels


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True)

    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"), nullable=False)

    assignee_id: Mapped[int | None] = mapped_column(
        ForeignKey("users.id"), nullable=True
    )

    title: Mapped[str] = mapped_column(String(255), nullable=False)

    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    status: Mapped[str] = mapped_column(String(50), default="TODO")

    priority: Mapped[str] = mapped_column(String(50), default="MEDIUM")

    due_date: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    created_by: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    project = relationship("Project", back_populates="tasks")

    assignee = relationship(
        "User", back_populates="assigned_tasks", foreign_keys=[assignee_id]
    )

    creator = relationship(
        "User", back_populates="created_tasks", foreign_keys=[created_by]
    )

    labels = relationship("Label", secondary=task_labels, back_populates="tasks")

    comments = relationship(
        "Comment", back_populates="task", cascade="all, delete-orphan"
    )
