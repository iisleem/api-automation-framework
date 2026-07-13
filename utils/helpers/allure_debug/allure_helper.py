from __future__ import annotations

import json
from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path
from typing import Any

import allure


@contextmanager
def step(title: str) -> Iterator[None]:
    with allure.step(title):
        yield


def attach_text(
    content: str,
    name: str = "text attachment",
    *,
    allure_api: Any = allure,
) -> None:
    allure_api.attach(
        content,
        name=name,
        attachment_type=allure_api.attachment_type.TEXT,
    )


def attach_json(
    data: Any,
    name: str = "json attachment",
    *,
    indent: int = 2,
    allure_api: Any = allure,
) -> None:
    allure_api.attach(
        json.dumps(data, indent=indent, ensure_ascii=False, default=str),
        name=name,
        attachment_type=allure_api.attachment_type.JSON,
    )


def attach_file(
    path: Path | str,
    name: str | None = None,
    *,
    attachment_type: Any | None = None,
    extension: str | None = None,
    allure_api: Any = allure,
) -> Path:
    file_path = Path(path)
    assert file_path.exists(), f"Attachment file does not exist: {file_path}"
    assert file_path.is_file(), f"Attachment path is not a file: {file_path}"

    allure_api.attach.file(
        str(file_path),
        name=name or file_path.name,
        attachment_type=attachment_type,
        extension=extension,
    )
    return file_path
