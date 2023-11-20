from importlib import import_module


def get_repository_by_name(package_name: str, repository_object_name: str) -> object | None:
    package = import_module(f"app.repository.{package_name}")
    return getattr(package, repository_object_name, None)
