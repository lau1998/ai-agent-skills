#!/usr/bin/env python3
"""校验并登记当前仓库管理的 AI Agent Skill。"""

from __future__ import annotations

import argparse
import os
import re
import stat
import sys
import tempfile
from pathlib import Path
from typing import Any, Sequence

import yaml

ALLOWED_CATEGORIES = frozenset({"development", "other"})
NAME_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
REQUIRED_FIELDS = frozenset({"name", "category", "path", "description"})


class CatalogError(ValueError):
    """表示目录索引或待登记 Skill 不符合项目约束。"""


def load_catalog(catalog_path: Path) -> dict[str, Any]:
    """读取并验证目录索引的根结构。

    Args:
        catalog_path: 待读取的 YAML 目录索引路径。

    Returns:
        包含版本号和 Skill 记录列表的目录索引。

    Raises:
        CatalogError: 文件无法读取、YAML 无效或根结构不符合约定。
    """
    try:
        catalog = yaml.safe_load(catalog_path.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as error:
        raise CatalogError(f"cannot read catalog: {error}") from error

    if not isinstance(catalog, dict):
        raise CatalogError("catalog root must be a mapping")
    if catalog.get("version") != 1:
        raise CatalogError("catalog version must be 1")
    if not isinstance(catalog.get("skills"), list):
        raise CatalogError("catalog skills must be a list")
    return catalog


def validate_entry(root: Path, entry: dict[str, str]) -> None:
    """验证单个 Skill 记录的字段、分类、名称和本地路径。

    Args:
        root: 仓库根目录。
        entry: 包含名称、分类、相对路径和简介的 Skill 记录。

    Raises:
        CatalogError: 记录缺少字段、字段值非法或目标目录不存在。
    """
    if not isinstance(entry, dict) or set(entry) != REQUIRED_FIELDS:
        raise CatalogError("entry fields must be name, category, path, description")
    if not all(isinstance(entry[field], str) for field in REQUIRED_FIELDS):
        raise CatalogError("entry values must be strings")

    name = entry["name"]
    category = entry["category"]
    relative_path = Path(entry["path"])
    if len(name) > 64 or not NAME_PATTERN.fullmatch(name):
        raise CatalogError("name must use lowercase letters, digits, and hyphens")
    if category not in ALLOWED_CATEGORIES:
        raise CatalogError("category must be development or other")
    if not entry["description"].strip():
        raise CatalogError("description must not be empty")
    if relative_path.is_absolute() or ".." in relative_path.parts:
        raise CatalogError("path must be relative to the repository root")

    expected_path = Path("skills") / category / name
    if relative_path != expected_path:
        raise CatalogError(f"path must be {expected_path.as_posix()}")
    if not (root / relative_path).is_dir():
        raise CatalogError(f"skill directory does not exist: {relative_path.as_posix()}")


def _validate_existing_entries(root: Path, entries: list[Any]) -> None:
    """验证既有记录并拒绝索引内部的重复项。

    Args:
        root: 仓库根目录。
        entries: 从目录索引读取的既有记录。

    Raises:
        CatalogError: 既有记录非法或包含重复名称、重复路径。
    """
    names: set[str] = set()
    paths: set[str] = set()
    for entry in entries:
        validate_entry(root, entry)
        if entry["name"] in names:
            raise CatalogError(f"duplicate name in catalog: {entry['name']}")
        if entry["path"] in paths:
            raise CatalogError(f"duplicate path in catalog: {entry['path']}")
        names.add(entry["name"])
        paths.add(entry["path"])


def _write_catalog_atomically(catalog_path: Path, catalog: dict[str, Any]) -> None:
    """使用同目录临时文件原子替换目录索引。

    Args:
        catalog_path: 最终目录索引路径。
        catalog: 已验证且需要写回的数据。

    Raises:
        CatalogError: 临时文件或最终文件无法写入。
    """
    temporary_path: Path | None = None
    try:
        catalog_mode = stat.S_IMODE(catalog_path.stat().st_mode)
        catalog_path.parent.mkdir(parents=True, exist_ok=True)
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            dir=catalog_path.parent,
            prefix=f".{catalog_path.name}.",
            suffix=".tmp",
            delete=False,
        ) as temporary_file:
            temporary_path = Path(temporary_file.name)
            yaml.safe_dump(
                catalog,
                temporary_file,
                allow_unicode=True,
                sort_keys=False,
            )
            temporary_file.flush()
            os.fsync(temporary_file.fileno())

        # 保留原权限，再用同一文件系统的原子替换避免半写入索引。
        os.chmod(temporary_path, catalog_mode)
        os.replace(temporary_path, catalog_path)
        temporary_path = None
    except OSError as error:
        raise CatalogError(f"cannot write catalog: {error}") from error
    finally:
        if temporary_path is not None:
            temporary_path.unlink(missing_ok=True)


def register_skill(
    catalog_path: Path,
    root: Path,
    entry: dict[str, str],
) -> None:
    """校验新记录并通过原子替换写回目录索引。

    Args:
        catalog_path: 目录索引文件路径。
        root: 仓库根目录。
        entry: 待登记的 Skill 记录。

    Raises:
        CatalogError: 新记录或既有目录索引不符合项目约束。
    """
    root = root.resolve()
    catalog_path = catalog_path.resolve()
    catalog = load_catalog(catalog_path)
    existing_entries = catalog["skills"]
    _validate_existing_entries(root, existing_entries)

    # 先保证重复检查访问的键和值安全，再判断索引冲突。
    if (
        not isinstance(entry, dict)
        or set(entry) != REQUIRED_FIELDS
        or not all(isinstance(entry[field], str) for field in REQUIRED_FIELDS)
    ):
        validate_entry(root, entry)

    # 重复项优先报告，避免其他字段错误掩盖索引冲突。
    if any(item["name"] == entry["name"] for item in existing_entries):
        raise CatalogError(f"name already registered: {entry['name']}")
    if any(item["path"] == entry["path"] for item in existing_entries):
        raise CatalogError(f"path already registered: {entry['path']}")

    validate_entry(root, entry)
    catalog["skills"].append(entry)
    _write_catalog_atomically(catalog_path, catalog)


def build_parser() -> argparse.ArgumentParser:
    """创建登记命令的参数解析器。

    Returns:
        配置好所有必填参数的 ArgumentParser。
    """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--catalog", required=True, type=Path)
    parser.add_argument("--root", required=True, type=Path)
    parser.add_argument("--name", required=True)
    parser.add_argument("--category", required=True)
    parser.add_argument("--path", required=True)
    parser.add_argument("--description", required=True)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    """执行命令行登记流程并返回进程退出码。

    Args:
        argv: 可选的命令行参数；省略时读取当前进程参数。

    Returns:
        成功时返回 0，目录校验失败时返回 2。
    """
    parser = build_parser()
    arguments = parser.parse_args(argv)
    entry = {
        "name": arguments.name,
        "category": arguments.category,
        "path": arguments.path,
        "description": arguments.description,
    }
    try:
        register_skill(arguments.catalog, arguments.root, entry)
    except CatalogError as error:
        print(f"error: {error}", file=sys.stderr)
        return 2

    print(f"Registered {arguments.name} as {arguments.category}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
