from src.protocol import TaskSource
from src.task import Task
import logging


class TaskLoader:
    def __init__(self, sources: list[TaskSource] | None = None):
        self.sources: list[TaskSource] = []
        if sources is not None:
            for source in sources:
                self.add_source(source)

    def add_source(self, source: TaskSource) -> None:
        if not isinstance(source, TaskSource):
            raise TypeError("Источник должен соответствовать протоколу TaskSource")
        self.sources.append(source)

    def load_tasks(self) -> list[Task]:
        logging.info(f"Загрузка задач из {len(self.sources)} источников")
        tasks: list[Task] = []
        for source in self.sources:
            tasks.extend(source.get_tasks())
        logging.info(f"Загружено {len(tasks)} задач из {len(self.sources)} источников")
        return tasks
