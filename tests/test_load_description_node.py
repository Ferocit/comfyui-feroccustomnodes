import os
import pytest

import load_description_node as ldn
from load_description_node import LoadDescriptionNode


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
