import os
from typing import Any, Callable


def load_option_from_env(
    option: str, default: any, transform: Callable = None, default_is_empty=False
) -> Any | str:
    value = os.environ.get(option, default)
    if default_is_empty and value is None:
        value = default
    if transform:
        value = transform(value)
    return value


def numeric_to_bool(numeric_string) -> bool:
    return bool(int(numeric_string))


def split_by_coma(coma_string) -> list[str]:
    return coma_string.split(",")
