from dataclasses import asdict
import json
import typer
from pathlib import Path
from src.loader import TaskLoader
from src.sources import ApiTaskSource, FileTaskSource, GeneratorTaskSource
from src.task import Task
from src.protocol import TaskSource


cli = typer.Typer(no_args_is_help=True)


def print_tasks(tasks: list[Task]) -> None:
    for task in tasks:
        print(json.dumps(asdict(task), ensure_ascii=True))


SOURCE_REGISTRY: dict[str, type[TaskSource]] = {
    "file": FileTaskSource,
    "generator": GeneratorTaskSource,
    "api": ApiTaskSource,
}


@cli.command("sources")
def sources_list() -> None:
    print("Доступные источники:")
    for source in SOURCE_REGISTRY:
        print(f"- {source}")


@cli.command("read")
def read(
    file: list[Path] = typer.Option(
        default_factory=list,
        exists=True,
        dir_okay=False,
        readable=True,
        help="Читать задачи из JSON-файла (можно несколько раз)",
    ),
    generator: int | None = typer.Option(
        None,
        "--generator",
        min=1,
        help="Сгенерировать N задач",
    ),
    seed: int | None = typer.Option(
        None,
        "--seed",
        help="Seed для генератора",
    ),
    api: bool = typer.Option(
        False,
        "--api",
        help="Читать задачи из API-заглушки",
    ),
) -> None:
    sources: list[TaskSource] = []
    for path in file:
        sources.append(FileTaskSource(str(path)))
    if generator is not None:
        sources.append(GeneratorTaskSource(count=generator, seed=seed))
    if api:
        sources.append(ApiTaskSource())

    loader = TaskLoader(sources)
    tasks = loader.load_tasks()

    print_tasks(tasks)
    print(f"\nВсего: {len(tasks)}")


def main() -> None:
    cli()


if __name__ == "__main__":
    main()
