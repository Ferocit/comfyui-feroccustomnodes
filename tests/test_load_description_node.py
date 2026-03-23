import os
import pytest

import load_description_node as ldn
from load_description_node import LoadDescriptionNode


class TestLoadDescription:
    """Integration tests for LoadDescriptionNode.load_description (Issue #4)."""

    def test_reads_existing_txt_file(self, tmp_path, monkeypatch):
        monkeypatch.setattr(ldn, "DESCRIPTION_PATH", str(tmp_path))
        txt_file = tmp_path / "myfile.txt"
        txt_file.write_text("Hello World", encoding="utf-8")

        node = LoadDescriptionNode()
        text, name = node.load_description("myfile.txt")

        assert text == "Hello World"
        assert name == "myfile"

    def test_returns_empty_tuple_when_file_missing(self, tmp_path, monkeypatch):
        monkeypatch.setattr(ldn, "DESCRIPTION_PATH", str(tmp_path))

        node = LoadDescriptionNode()
        text, name = node.load_description("nonexistent.txt")

        assert text == ""
        assert name == ""

    def test_accepts_path_without_txt_extension(self, tmp_path, monkeypatch):
        monkeypatch.setattr(ldn, "DESCRIPTION_PATH", str(tmp_path))
        txt_file = tmp_path / "myfile.txt"
        txt_file.write_text("Content", encoding="utf-8")

        node = LoadDescriptionNode()
        text, name = node.load_description("myfile")

        assert text == "Content"

    def test_reads_nested_file(self, tmp_path, monkeypatch):
        monkeypatch.setattr(ldn, "DESCRIPTION_PATH", str(tmp_path))
        sub = tmp_path / "sub"
        sub.mkdir()
        (sub / "nested.txt").write_text("Nested content", encoding="utf-8")

        node = LoadDescriptionNode()
        text, name = node.load_description("sub/nested.txt")

        assert text == "Nested content"
        assert name == "nested"


class TestAbsPath:
    """Tests for LoadDescriptionNode._abs_path (Issue #3 / #4)."""

    def test_adds_txt_extension(self, tmp_path, monkeypatch):
        monkeypatch.setattr(ldn, "DESCRIPTION_PATH", str(tmp_path))
        result = LoadDescriptionNode._abs_path("subdir/myfile")
        assert result.endswith(".txt")

    def test_does_not_double_add_txt_extension(self, tmp_path, monkeypatch):
        monkeypatch.setattr(ldn, "DESCRIPTION_PATH", str(tmp_path))
        result = LoadDescriptionNode._abs_path("subdir/myfile.txt")
        assert result.endswith("myfile.txt")
        assert "myfile.txt.txt" not in result

    def test_normalizes_backslashes(self, tmp_path, monkeypatch):
        monkeypatch.setattr(ldn, "DESCRIPTION_PATH", str(tmp_path))
        result = LoadDescriptionNode._abs_path("subdir\\myfile")
        assert "subdir" in result
        assert result.endswith("myfile.txt")

    def test_strips_leading_whitespace(self, tmp_path, monkeypatch):
        monkeypatch.setattr(ldn, "DESCRIPTION_PATH", str(tmp_path))
        result_stripped = LoadDescriptionNode._abs_path("  myfile  ")
        result_clean = LoadDescriptionNode._abs_path("myfile")
        assert result_stripped == result_clean

    def test_resolves_relative_to_description_path(self, tmp_path, monkeypatch):
        monkeypatch.setattr(ldn, "DESCRIPTION_PATH", str(tmp_path))
        result = LoadDescriptionNode._abs_path("sub/file")
        assert result.startswith(str(tmp_path))
