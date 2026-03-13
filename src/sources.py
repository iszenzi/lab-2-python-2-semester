"""
Модуль источников задач
"""

import json
import logging
import random

from src.task import Task


class FileTaskSource:
    """
    Источник задач из JSON-файла
    """
    def __init__(self, path: str):
        """
        Создает источник задач из файла
        :param path: Путь к JSON-файлу
        """
        if not isinstance(path, str):
            raise TypeError("Путь к файлу должен быть строкой")
        self.path = path

    def get_tasks(self) -> list[Task]:
        """
        Загружает задачи из файла
        :return: Список задач
        """
        try:
            tasks = []
            with open(self.path, "r", encoding="utf-8") as f:
                data = json.load(f)
            for i in data:
                tasks.append(Task(id=i["id"], payload=i["payload"]))
            logging.info(f"Загружено {len(tasks)} задач из файла {self.path}")
            return tasks
        except FileNotFoundError:
            logging.error(f"ERROR: Файл {self.path} не найден")
            raise FileNotFoundError(f"Файл {self.path} не найден")


class GeneratorTaskSource:
    """
    Источник задач на основе генератора
    """
    def __init__(self, count: int = 10, seed: int | None = None):
        """
        Создает источник задач-генератор
        :param count: Количество задач
        :param seed: Seed для генератора
        """
        if not isinstance(count, int) or count <= 0:
            raise TypeError("Количество задач должно быть целым положительным числом")
        if seed is not None and not isinstance(seed, int):
            raise TypeError("Seed должен быть целым числом или None")
        self.count = count
        self._random = random.Random(seed)

    def get_tasks(self) -> list[Task]:
        """
        Генерирует задачи
        :return: Список задач
        """
        tasks = []
        tasks_type = [
            "process_order",
            "send_notification",
            "recalculate_stats",
            "check_resource",
            "ingest_external",
            "send_email",
            "send_sms",
            "push_notification",
            "call_api",
            "generate_report",
            "data_processing",
            "update_database",
            "monitoring_task",
            "logging_task",
            "validation_task",
            "integration_task",
        ]
        for i in range(self.count):
            task_type = tasks_type[i % len(tasks_type)]
            tasks.append(
                Task(
                    id=i + 1,
                    payload={
                        "type": task_type,
                        "sequence": i + 1,
                        "priority": self._random.randint(1, 5),
                    },
                )
            )
        logging.info(f"Сгенерировано {len(tasks)} задач с seed={self._random.seed}")
        return tasks


class ApiTaskSource:
    """
    Источник задач из API-заглушки
    """
    def __init__(self):
        """
        Создает API-заглушку с задачами
        """
        self._api_data = [
            {"id": 1, "payload": {"type": "process_order", "priority": 3}},
            {"id": 2, "payload": {"type": "send_notification", "priority": 2}},
            {"id": 3, "payload": {"type": "recalculate_stats", "priority": 4}},
        ]

    def get_tasks(self) -> list[Task]:
        """
        Возвращает задачи из API-заглушки
        :return: Список задач
        """
        tasks = []
        for i in self._api_data:
            tasks.append(Task(id=i["id"], payload=i["payload"]))
        logging.info(f"Загружено {len(tasks)} задач из API-заглушки")
        return tasks
