"""
Модуль модели задачи
"""

from dataclasses import dataclass
from typing import Any


@dataclass
class Task:
    """
    Модель задачи
    :param id: Идентификатор задачи
    :param payload: Данные задачи
    """
    id: int
    payload: Any
