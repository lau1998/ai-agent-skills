"""测试 Skill 目录索引的登记行为。"""

from __future__ import annotations

import contextlib
import io
import sys
import tempfile
import unittest
from pathlib import Path

import yaml

SCRIPT_DIR = (
    Path(__file__).resolve().parents[1]
    / "skills"
    / "development"
    / "create-skill"
    / "scripts"
)
sys.path.insert(0, str(SCRIPT_DIR))

from register_skill import CatalogError, main, register_skill  # noqa: E402


class RegisterSkillTests(unittest.TestCase):
    """验证合法登记和所有必须拒绝的输入。"""

    def setUp(self) -> None:
        """为每个测试创建独立的目录索引和 Skill 目录。"""
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary_directory.cleanup)
        self.root = Path(self.temporary_directory.name)
        self.catalog_path = self.root / "catalog.yaml"
        self.catalog_path.write_text("version: 1\nskills: []\n", encoding="utf-8")

        self.entry = {
            "name": "example-skill",
            "category": "development",
            "path": "skills/development/example-skill",
            "description": "Example development skill",
        }
        self.other_entry = {
            "name": "writing-helper",
            "category": "other",
            "path": "skills/other/writing-helper",
            "description": "Example writing skill",
        }
        (self.root / self.entry["path"]).mkdir(parents=True)
        (self.root / self.other_entry["path"]).mkdir(parents=True)

    def test_register_skill_appends_valid_entry(self) -> None:
        """合法记录应追加到目录索引。"""
        register_skill(self.catalog_path, self.root, self.entry)

        catalog = yaml.safe_load(self.catalog_path.read_text(encoding="utf-8"))
        self.assertEqual(catalog["skills"], [self.entry])

    def test_register_skill_accepts_other_category(self) -> None:
        """其他类 Skill 应使用与开发类相同的登记流程。"""
        register_skill(self.catalog_path, self.root, self.other_entry)

        catalog = yaml.safe_load(self.catalog_path.read_text(encoding="utf-8"))
        self.assertEqual(catalog["skills"], [self.other_entry])

    def test_register_skill_rejects_duplicate_name(self) -> None:
        """同名 Skill 即使路径不同也不得重复登记。"""
        register_skill(self.catalog_path, self.root, self.entry)
        duplicate = {**self.other_entry, "name": self.entry["name"]}

        with self.assertRaisesRegex(CatalogError, "name already registered"):
            register_skill(self.catalog_path, self.root, duplicate)

    def test_register_skill_rejects_duplicate_path(self) -> None:
        """同一路径即使名称不同也不得重复登记。"""
        register_skill(self.catalog_path, self.root, self.entry)
        duplicate = {**self.other_entry, "path": self.entry["path"]}

        with self.assertRaisesRegex(CatalogError, "path already registered"):
            register_skill(self.catalog_path, self.root, duplicate)

    def test_register_skill_rejects_invalid_category(self) -> None:
        """目录索引只接受项目定义的两个分类。"""
        invalid = {**self.entry, "category": "business"}

        with self.assertRaisesRegex(CatalogError, "category must be"):
            register_skill(self.catalog_path, self.root, invalid)

    def test_register_skill_rejects_missing_fields(self) -> None:
        """缺少必填字段时应返回统一的目录校验错误。"""
        register_skill(self.catalog_path, self.root, self.entry)
        invalid = {key: value for key, value in self.entry.items() if key != "name"}

        with self.assertRaisesRegex(CatalogError, "entry fields must be"):
            register_skill(self.catalog_path, self.root, invalid)

    def test_register_skill_rejects_invalid_name(self) -> None:
        """名称不符合 Skill 命名规则时不得登记。"""
        invalid = {
            **self.entry,
            "name": "Example Skill",
            "path": "skills/development/Example Skill",
        }
        (self.root / invalid["path"]).mkdir(parents=True)

        with self.assertRaisesRegex(CatalogError, "name must use"):
            register_skill(self.catalog_path, self.root, invalid)

    def test_register_skill_rejects_missing_skill_directory(self) -> None:
        """不存在的 Skill 路径不能写入目录索引。"""
        missing = {
            **self.entry,
            "name": "missing",
            "path": "skills/development/missing",
        }

        with self.assertRaisesRegex(CatalogError, "skill directory does not exist"):
            register_skill(self.catalog_path, self.root, missing)

    def test_main_registers_skill_and_reports_category(self) -> None:
        """命令行入口应登记 Skill 并输出分类结果。"""
        stdout = io.StringIO()
        arguments = [
            "--catalog",
            str(self.catalog_path),
            "--root",
            str(self.root),
            "--name",
            self.entry["name"],
            "--category",
            self.entry["category"],
            "--path",
            self.entry["path"],
            "--description",
            self.entry["description"],
        ]

        with contextlib.redirect_stdout(stdout):
            exit_code = main(arguments)

        self.assertEqual(exit_code, 0)
        self.assertIn("Registered example-skill as development", stdout.getvalue())


if __name__ == "__main__":
    unittest.main()
