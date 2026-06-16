from sqlalchemy import Column, ForeignKey, Table

from app.models.base import Base


task_labels = Table(
    "task_labels",
    Base.metadata,
    Column(
        "task_id",
        ForeignKey("tasks.id"),
        primary_key=True
    ),
    Column(
        "label_id",
        ForeignKey("labels.id"),
        primary_key=True
    )
)