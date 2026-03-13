from src.protocol import TaskSource
from src.task import Task
import logging


class TaskLoader:
    """
    Загрузчик задач из источников
    """

    def __init__(self, sources: list[TaskSource] | None = None):
        """
        Создает загрузчик задач
        :param sources: Список источников задач
        """
        self.sources: list[TaskSource] = []
        if sources is not None:
            for source in sources:
                self.add_source(source)

    def add_source(self, source: TaskSource) -> None:
        """
        Добавляет источник задач
        :param source: Источник задач
        """
        if not isinstance(source, TaskSource):
            logging.error("ERROR: Источник должен соответствовать протоколу TaskSource")
            raise TypeError("Источник должен соответствовать протоколу TaskSource")
        self.sources.append(source)

    def load_tasks(self) -> list[Task]:
        """
        Загружает задачи из всех источников
        :return: Список задач
        """
        logging.info(f"Загрузка задач из {len(self.sources)} источников")
        tasks: list[Task] = []
        for source in self.sources:
            tasks.extend(source.get_tasks())
        logging.info(f"Загружено {len(tasks)} задач из {len(self.sources)} источников")
        return tasks
