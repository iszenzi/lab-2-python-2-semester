"""
Модуль протоколов источников задач
"""

from typing import runtime_checkable, Protocol

from src.task import Task


@runtime_checkable
class TaskSource(Protocol):
    """
    Протокол источника задач
    """
    def get_tasks(self) -> list[Task]: ...
