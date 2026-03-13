import pytest
from src.loader import TaskLoader
from src.sources import ApiTaskSource, FileTaskSource, GeneratorTaskSource
import json


class TestFileTaskSource:
    """
    Тесты источника задач из файла
    """

    def test_loads_and_sets_defaults(self, tmp_path):
        """
        Проверяет загрузку задач и проставление значений по умолчанию
        :param tmp_path: Временная директория pytest
        """
        data = [
            {"id": 1, "payload": {"note": "from_file"}},
            {"id": 2, "payload": {"type": "custom"}},
        ]
        file_path = tmp_path / "tasks.json"
        file_path.write_text(json.dumps(data), encoding="utf-8")

        source = FileTaskSource(str(file_path))
        tasks = source.get_tasks()

        assert len(tasks) == 2
        assert tasks[0].payload["type"] == "file_task"
        assert tasks[0].payload["priority"] == 1
        assert tasks[0].payload["sequence"] == 1
        assert tasks[1].payload["type"] == "custom"
        assert tasks[1].payload["priority"] == 1
        assert tasks[1].payload["sequence"] == 2

    def test_missing_file_raises(self):
        """
        Проверяет ошибку при отсутствии файла
        """
        source = FileTaskSource("missing.json")
        with pytest.raises(FileNotFoundError):
            source.get_tasks()


class TestGeneratorTaskSource:
    """
    Тесты источника генератора задач
    """

    def test_seed_is_deterministic(self):
        """
        Проверяет детерминированность генератора при одинаковом seed
        """
        source_a = GeneratorTaskSource(count=5, seed=7)
        source_b = GeneratorTaskSource(count=5, seed=7)

        tasks_a = source_a.get_tasks()
        tasks_b = source_b.get_tasks()

        assert tasks_a[0].payload == tasks_b[0].payload
        assert tasks_a[1].payload == tasks_b[1].payload

    def test_invalid_count_and_seed(self):
        """
        Проверяет ошибки при неверных параметрах генератора
        """
        with pytest.raises(TypeError):
            GeneratorTaskSource(count=0)
        with pytest.raises(TypeError):
            GeneratorTaskSource(count=-1)
        with pytest.raises(TypeError):
            GeneratorTaskSource(count=1, seed="bad")


class TestApiTaskSource:
    """
    Тесты API-заглушки
    """

    def test_returns_tasks(self):
        """
        Проверяет получение задач из API-заглушки
        """
        source = ApiTaskSource()
        tasks = source.get_tasks()

        assert len(tasks) == 3
        assert tasks[0].payload["type"] == "process_order"
        assert tasks[0].payload["sequence"] == 1


class TestTaskLoader:
    """
    Тесты загрузчика задач
    """

    def test_add_source_rejects_invalid(self):
        """
        Проверяет отказ добавления источника без контракта
        """
        loader = TaskLoader()
        with pytest.raises(TypeError):
            loader.add_source(object())

    def test_load_tasks_grouped_order(self, tmp_path):
        """
        Проверяет порядок источников и группировку задач
        :param tmp_path: Временная директория pytest
        """
        data = [
            {"id": 1, "payload": {"type": "file_task"}},
        ]
        file_path = tmp_path / "tasks.json"
        file_path.write_text(json.dumps(data), encoding="utf-8")

        source_a = FileTaskSource(str(file_path))
        source_b = GeneratorTaskSource(count=2, seed=7)

        loader = TaskLoader([source_a, source_b])
        grouped = loader.load_tasks()

        assert grouped[0][0] is source_a
        assert len(grouped[0][1]) == 1
        assert grouped[1][0] is source_b
        assert len(grouped[1][1]) == 2
        assert grouped[1][1][0].payload == {
            "type": "data_processing",
            "sequence": 1,
            "priority": 2,
        }
        assert grouped[1][1][1].payload == {
            "type": "monitoring_task",
            "sequence": 2,
            "priority": 1,
        }
