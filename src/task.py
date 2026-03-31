from typing import Any
from enum import Enum
from datetime import datetime
from exceptions import InvalidPriorityError
from descriptors import PriorityDescriptor


class TaskStatus(Enum):
    """Статусы задачи"""

    NEW = "new"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"


class Task:

    priority = PriorityDescriptor(min_val=1, max_val=5)

    def __init__(
        self, id: int, payload: Any, priority: int, descripton: str = ""
    ) -> None:
        self._id = id
        self.payload = payload
        self.priority = priority
        self.description = description
        self.status = TaskStatus.NEW
        self.created_at = datetime.now()

    @property
    def id(self) -> int:
        return self._id

    @property
    def ready_for_execution(self) -> bool:
        return self.status == TaskStatus.NEW
