import os
import random
import pytest

import file_utils


class TestReadTextFile:
    def test_returns_file_content(self, tmp_path):
        f = tmp_path / "hello.txt"
        f.write_text("Hello World", encoding="utf-8")
        assert file_utils.read_text_file(str(f)) == "Hello World"

    def test_returns_empty_string_when_file_missing(self):
        assert file_utils.read_text_file("/nonexistent/path/file.txt") == ""

    def test_returns_empty_string_on_empty_file(self, tmp_path):
        f = tmp_path / "empty.txt"
        f.write_text("", encoding="utf-8")
        assert file_utils.read_text_file(str(f)) == ""


class TestReadRandomLine:
    def test_returns_a_line_from_file(self, tmp_path):
        f = tmp_path / "lines.txt"
        f.write_text("line1\nline2\nline3\n", encoding="utf-8")
        rng = random.Random(42)
        result = file_utils.read_random_line(str(f), rng)
        assert result is not None
        assert result.strip() in ["line1", "line2", "line3"]

    def test_same_seed_produces_same_result(self, tmp_path):
        f = tmp_path / "lines.txt"
        f.write_text("apple\nbanana\ncherry\n", encoding="utf-8")
        result1 = file_utils.read_random_line(str(f), random.Random(0))
        result2 = file_utils.read_random_line(str(f), random.Random(0))
        assert result1 == result2

    def test_returns_none_for_missing_file(self):
        rng = random.Random(0)
        assert file_utils.read_random_line("/nonexistent/file.txt", rng) is None

    def test_returns_none_for_empty_file(self, tmp_path):
        f = tmp_path / "empty.txt"
        f.write_text("\n\n   \n", encoding="utf-8")
        rng = random.Random(0)
        assert file_utils.read_random_line(str(f), rng) is None

    def test_skips_blank_lines(self, tmp_path):
        f = tmp_path / "sparse.txt"
        f.write_text("\n\nonly_line\n\n", encoding="utf-8")
        rng = random.Random(0)
        result = file_utils.read_random_line(str(f), rng)
        assert result is not None
        assert result.strip() == "only_line"

    def test_no_trailing_newline_in_result(self, tmp_path):
        f = tmp_path / "lines.txt"
        f.write_text("apple\nbanana\ncherry\n", encoding="utf-8")
        rng = random.Random(0)
        result = file_utils.read_random_line(str(f), rng)
        assert result is not None
        assert not result.endswith('\n')


class TestNormalizeDescriptionPath:
    def test_adds_txt_extension(self, tmp_path, monkeypatch):
        monkeypatch.setattr(file_utils, "DESCRIPTION_PATH", str(tmp_path))
        result = file_utils.normalize_description_path("myfile")
        assert result.endswith(".txt")

    def test_does_not_double_add_extension(self, tmp_path, monkeypatch):
        monkeypatch.setattr(file_utils, "DESCRIPTION_PATH", str(tmp_path))
        result = file_utils.normalize_description_path("myfile.txt")
        assert not result.endswith(".txt.txt")

    def test_normalizes_backslashes(self, tmp_path, monkeypatch):
        monkeypatch.setattr(file_utils, "DESCRIPTION_PATH", str(tmp_path))
        result = file_utils.normalize_description_path("sub\\myfile")
        assert "sub" in result
        assert result.endswith("myfile.txt")

    def test_result_is_under_description_path(self, tmp_path, monkeypatch):
        monkeypatch.setattr(file_utils, "DESCRIPTION_PATH", str(tmp_path))
        result = file_utils.normalize_description_path("sub/file")
        assert result.startswith(str(tmp_path))
