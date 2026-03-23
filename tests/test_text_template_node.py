import pytest

import text_template_node as ttn
from text_template_node import TextTemplateNode


class TestFillTemplate:
    def test_single_substitution(self):
        node = TextTemplateNode()
        result, = node.fill_template("{name}", key_1="name", value_1="Alice")
        assert result == "Alice"

    def test_multiple_substitutions(self):
        node = TextTemplateNode()
        result, = node.fill_template(
            "{adj} {noun}",
            key_1="adj", value_1="brave",
            key_2="noun", value_2="warrior",
        )
        assert result == "brave warrior"

    def test_unknown_placeholder_preserved(self):
        node = TextTemplateNode()
        result, = node.fill_template("{unknown}")
        assert result == "{unknown}"

    def test_empty_key_is_skipped(self):
        node = TextTemplateNode()
        result, = node.fill_template("{x}", key_1="", value_1="something")
        assert result == "{x}"

    def test_whitespace_key_is_stripped(self):
        node = TextTemplateNode()
        result, = node.fill_template("{name}", key_1="  name  ", value_1="Bob")
        assert result == "Bob"

    def test_multiline_value_inserted_verbatim(self):
        node = TextTemplateNode()
        multiline = "line one\nline two\nline three"
        result, = node.fill_template("{desc}", key_1="desc", value_1=multiline)
        assert result == multiline

    def test_literal_braces_not_treated_as_placeholder(self):
        node = TextTemplateNode()
        result, = node.fill_template("{{not a placeholder}}")
        assert result == "{not a placeholder}"

    def test_malformed_template_returns_original(self):
        node = TextTemplateNode()
        malformed = "unclosed { brace"
        result, = node.fill_template(malformed)
        assert result == malformed

    def test_all_five_pairs_substituted(self):
        node = TextTemplateNode()
        template = "{a} {b} {c} {d} {e}"
        result, = node.fill_template(
            template,
            key_1="a", value_1="1",
            key_2="b", value_2="2",
            key_3="c", value_3="3",
            key_4="d", value_4="4",
            key_5="e", value_5="5",
        )
        assert result == "1 2 3 4 5"

    def test_returns_tuple(self):
        node = TextTemplateNode()
        result = node.fill_template("hello")
        assert isinstance(result, tuple)
        assert len(result) == 1

    def test_no_keys_leaves_template_unchanged(self):
        node = TextTemplateNode()
        result, = node.fill_template("{foo} {bar}")
        assert result == "{foo} {bar}"

    def test_partial_substitution_leaves_unknown_intact(self):
        node = TextTemplateNode()
        result, = node.fill_template("{known} {unknown}", key_1="known", value_1="X")
        assert result == "X {unknown}"
