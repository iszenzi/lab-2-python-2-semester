"""
Модуль настройки логирования
"""

import logging


def setup_logging() -> None:
    """
    Создает конфиг логирования
    """
    logging.basicConfig(
        filename="shell.log",
        level=logging.INFO,
        format="[%(asctime)s] %(message)s",
        datefmt="%y-%m-%d %H:%M:%S",
        encoding="utf-8",
    )
