# Лабораторная работа №1 - Источники задач и контракты

## Описание
Проект демонстрирует работу с duck typing и контрактами через typing.Protocol на примере источников задач. Реализованы три независимых источника: файл, генератор и API-заглушка. Все источники предоставляют задачи через единый контракт get_tasks() и используются в модуле загрузки.

## Структура проекта
```
|-- src/
|   |-- __init__.py
|   |-- main.py           # CLI для запуска и демонстрации работы
|   |-- loader.py         # Загрузчик задач 
|   |-- sources.py        # Источники задач
|   |-- protocol.py       # typing.Protocol для источников
|   |-- task.py           # Модель задачи
|   |-- logger.py         # Логгер
|
|-- tests/
|   |-- __init__.py
|   |-- test_sources_loader.py # Тесты источников и загрузчика
|
|-- tasks.json            # Пример входных задач
|-- tasks_no_defaults.json # Пример неполного payload
|-- pyproject.toml        # Конфиг проекта
|-- requirements.txt      # Зависимости проекта
|-- README.md             # Документация
|-- .pre-commit-config.yaml # Конфиг pre-commit
|-- .gitignore            # Файл .gitignore
|-- uv.lock               # Файл блокировки uv
```
## Реализованные компоненты

### Контракт источника

- TaskSource — Protocol с единым методом get_tasks()

### Модель задачи

- Task(id: int, payload: Any) — минимальная структура задачи

### Источники задач

- FileTaskSource(path: str) — загрузка задач из JSON-файла
- GeneratorTaskSource(count: int = 10, seed: int | None = None) — генерация задач
- ApiTaskSource() — API-заглушка

### Загрузчик

- TaskLoader — сбор задач из источников с runtime-проверкой контракта (isinstance)

### Логирование

- setup_logging() — настройка логирования в файл shell.log

## Установка зависимостей 
```
pip install -r requirements.txt
```

## Запуск программы
Вывод общей информации для взаимодействия с программой:
```
python -m src.main --help
```
Подробнее про запуск программы
```
python -m src.main read --help
```
