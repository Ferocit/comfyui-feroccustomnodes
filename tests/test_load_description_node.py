import os
import pytest

import load_description_node as ldn
import file_utils
from load_description_node import LoadDescriptionNode


class TestLoadDescription:
    """Integration tests for LoadDescriptionNode.load_description (Issue #4)."""

    def test_reads_existing_txt_file(self, tmp_path, monkeypatch):
        monkeypatch.setattr(ldn, "DESCRIPTION_PATH", str(tmp_path))
        monkeypatch.setattr(file_utils, "DESCRIPTION_PATH", str(tmp_path))
        txt_file = tmp_path / "myfile.txt"
        txt_file.write_text("Hello World", encoding="utf-8")

        node = LoadDescriptionNode()
        text, name = node.load_description("myfile.txt")

        assert text == "Hello World"
        assert name == "myfile"

    def test_returns_empty_tuple_when_file_missing(self, tmp_path, monkeypatch):
        monkeypatch.setattr(ldn, "DESCRIPTION_PATH", str(tmp_path))
        monkeypatch.setattr(file_utils, "DESCRIPTION_PATH", str(tmp_path))

        node = LoadDescriptionNode()
        text, name = node.load_description("nonexistent.txt")

        assert text == ""
        assert name == ""

    def test_accepts_path_without_txt_extension(self, tmp_path, monkeypatch):
        monkeypatch.setattr(ldn, "DESCRIPTION_PATH", str(tmp_path))
        monkeypatch.setattr(file_utils, "DESCRIPTION_PATH", str(tmp_path))
        txt_file = tmp_path / "myfile.txt"
        txt_file.write_text("Content", encoding="utf-8")

        node = LoadDescriptionNode()
        text, name = node.load_description("myfile")

        assert text == "Content"

    def test_reads_nested_file(self, tmp_path, monkeypatch):
        monkeypatch.setattr(ldn, "DESCRIPTION_PATH", str(tmp_path))
        monkeypatch.setattr(file_utils, "DESCRIPTION_PATH", str(tmp_path))
        sub = tmp_path / "sub"
        sub.mkdir()
        (sub / "nested.txt").write_text("Nested content", encoding="utf-8")

        node = LoadDescriptionNode()
        text, name = node.load_description("sub/nested.txt")

        assert text == "Nested content"
        assert name == "nested"


class TestListAllDescriptionFiles:
    """Tests for list_all_description_files (Issue #9)."""

    def test_finds_flat_txt_files(self, tmp_path, monkeypatch):
        monkeypatch.setattr(ldn, "DESCRIPTION_PATH", str(tmp_path))
        monkeypatch.setattr(file_utils, "DESCRIPTION_PATH", str(tmp_path))
        (tmp_path / "a.txt").write_text("a", encoding="utf-8")
        (tmp_path / "b.txt").write_text("b", encoding="utf-8")
        result = ldn.list_all_description_files()
        assert "a.txt" in result
        assert "b.txt" in result

    def test_finds_nested_txt_files(self, tmp_path, monkeypatch):
        monkeypatch.setattr(ldn, "DESCRIPTION_PATH", str(tmp_path))
        monkeypatch.setattr(file_utils, "DESCRIPTION_PATH", str(tmp_path))
        sub = tmp_path / "sub"
        sub.mkdir()
        (sub / "nested.txt").write_text("n", encoding="utf-8")
        result = ldn.list_all_description_files()
        assert "sub/nested.txt" in result

    def test_returns_sorted_list(self, tmp_path, monkeypatch):
        monkeypatch.setattr(ldn, "DESCRIPTION_PATH", str(tmp_path))
        monkeypatch.setattr(file_utils, "DESCRIPTION_PATH", str(tmp_path))
        for name in ["z.txt", "a.txt", "m.txt"]:
            (tmp_path / name).write_text("x", encoding="utf-8")
        result = ldn.list_all_description_files()
        assert result == sorted(result)


class TestIsChanged:
    """Tests for LoadDescriptionNode.IS_CHANGED (Issue #9)."""

    def test_returns_string(self, tmp_path, monkeypatch):
        monkeypatch.setattr(ldn, "DESCRIPTION_PATH", str(tmp_path))
        monkeypatch.setattr(file_utils, "DESCRIPTION_PATH", str(tmp_path))
        (tmp_path / "f.txt").write_text("content", encoding="utf-8")
        result = LoadDescriptionNode.IS_CHANGED(file_path="f.txt")
        assert isinstance(result, str)

    def test_changes_after_file_modification(self, tmp_path, monkeypatch):
        monkeypatch.setattr(ldn, "DESCRIPTION_PATH", str(tmp_path))
        monkeypatch.setattr(file_utils, "DESCRIPTION_PATH", str(tmp_path))
        f = tmp_path / "f.txt"
        f.write_text("v1", encoding="utf-8")
        val1 = LoadDescriptionNode.IS_CHANGED(file_path="f.txt")
        f.write_text("v1_changed_longer_content", encoding="utf-8")
        val2 = LoadDescriptionNode.IS_CHANGED(file_path="f.txt")
        assert val1 != val2

    def test_returns_fallback_for_missing_file(self):
        result = LoadDescriptionNode.IS_CHANGED(file_path="/no/such/file.txt")
        assert isinstance(result, str)


class TestResolveFilePath:
    """Tests for LoadDescriptionNode._resolve_file_path (Issue #5)."""

    def test_returns_path_when_set(self):
        result = LoadDescriptionNode._resolve_file_path("some/path.txt")
        assert result == "some/path.txt"

    def test_falls_back_when_empty(self, tmp_path, monkeypatch):
        monkeypatch.setattr(ldn, "DESCRIPTION_PATH", str(tmp_path))
        monkeypatch.setattr(file_utils, "DESCRIPTION_PATH", str(tmp_path))
        (tmp_path / "first.txt").write_text("x", encoding="utf-8")
        result = LoadDescriptionNode._resolve_file_path("")
        assert result == "first.txt"

    def test_falls_back_when_none(self, tmp_path, monkeypatch):
        monkeypatch.setattr(ldn, "DESCRIPTION_PATH", str(tmp_path))
        monkeypatch.setattr(file_utils, "DESCRIPTION_PATH", str(tmp_path))
        (tmp_path / "first.txt").write_text("x", encoding="utf-8")
        result = LoadDescriptionNode._resolve_file_path(None)
        assert result == "first.txt"

    def test_falls_back_when_undefined(self, tmp_path, monkeypatch):
        monkeypatch.setattr(ldn, "DESCRIPTION_PATH", str(tmp_path))
        monkeypatch.setattr(file_utils, "DESCRIPTION_PATH", str(tmp_path))
        (tmp_path / "first.txt").write_text("x", encoding="utf-8")
        result = LoadDescriptionNode._resolve_file_path("undefined")
        assert result == "first.txt"


