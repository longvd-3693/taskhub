from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base
from app.models.task_label import task_labels


class Label(Base):
    __tablename__ = "labels"

    id: Mapped[int] = mapped_column(primary_key=True)

    project_id: Mapped[int] = mapped_column(
        ForeignKey("projects.id"),
        nullable=False
    )

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    color: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    project = relationship(
        "Project",
        back_populates="labels"
    )

    tasks = relationship(
        "Task",
        secondary=task_labels,
        back_populates="labels"
    )