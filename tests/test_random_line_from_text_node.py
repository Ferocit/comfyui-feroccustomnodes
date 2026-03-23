import logging
import os
import pytest

import random_line_from_text_node as rltn
from random_line_from_text_node import RandomLineFromTextNode


class TestGetRandomLines:
    """Tests for RandomLineFromTextNode.get_random_lines (Issues #6, #9)."""

    def test_missing_file_logs_warning(self, caplog):
        with caplog.at_level(logging.WARNING, logger="file_utils"):
            node = RandomLineFromTextNode()
            node.get_random_lines(seed=0, file_path_1="/nonexistent/file.txt")
        assert any("File not found" in r.message for r in caplog.records)

    def test_returns_empty_string_when_no_files(self):
        node = RandomLineFromTextNode()
        result, = node.get_random_lines(seed=0)
        assert result == ""

    def test_same_seed_produces_same_result(self, tmp_path):
        f = tmp_path / "words.txt"
        f.write_text("apple\nbanana\ncherry\n", encoding="utf-8")
        node = RandomLineFromTextNode()
        result1, = node.get_random_lines(seed=42, file_path_1=str(f))
        result2, = node.get_random_lines(seed=42, file_path_1=str(f))
        assert result1 == result2

    def test_different_seeds_may_differ(self, tmp_path):
        f = tmp_path / "words.txt"
        # Many lines to make collision unlikely
        f.write_text("\n".join(f"word{i}" for i in range(100)), encoding="utf-8")
        node = RandomLineFromTextNode()
        results = {node.get_random_lines(seed=s, file_path_1=str(f))[0] for s in range(20)}
        assert len(results) > 1

    def test_empty_file_is_skipped(self, tmp_path):
        f = tmp_path / "empty.txt"
        f.write_text("\n\n   \n", encoding="utf-8")
        node = RandomLineFromTextNode()
        result, = node.get_random_lines(seed=0, file_path_1=str(f))
        assert result == ""

    def test_multiple_files_concatenated(self, tmp_path):
        f1 = tmp_path / "a.txt"
        f2 = tmp_path / "b.txt"
        f1.write_text("only_a\n", encoding="utf-8")
        f2.write_text("only_b\n", encoding="utf-8")
        node = RandomLineFromTextNode()
        result, = node.get_random_lines(seed=0, file_path_1=str(f1), file_path_2=str(f2))
        assert "only_a" in result
        assert "only_b" in result

    def test_blank_paths_are_ignored(self, tmp_path):
        f = tmp_path / "valid.txt"
        f.write_text("hello\n", encoding="utf-8")
        node = RandomLineFromTextNode()
        result, = node.get_random_lines(seed=0, file_path_1="", file_path_2=str(f), file_path_3="  ")
        assert result.strip() == "hello"
