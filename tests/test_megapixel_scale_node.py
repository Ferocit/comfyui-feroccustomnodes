import pytest

from megapixel_scale_node import MegapixelScaleNode


class TestScale:
    def test_square_one_megapixel(self):
        node = MegapixelScaleNode()
        width, height = node.scale(512, 512, 1.0)
        assert width == height
        assert abs(width * height - 1_000_000) < 2000

    def test_preserves_aspect_ratio(self):
        node = MegapixelScaleNode()
        width, height = node.scale(1920, 1080, 1.0)
        original_ratio = 1920 / 1080
        new_ratio = width / height
        assert abs(original_ratio - new_ratio) < 0.01

    def test_upscale(self):
        node = MegapixelScaleNode()
        width, height = node.scale(512, 512, 2.0)
        assert width > 512
        assert height > 512

    def test_downscale(self):
        node = MegapixelScaleNode()
        width, height = node.scale(2048, 2048, 1.0)
        assert width < 2048
        assert height < 2048

    def test_already_at_target_is_unchanged(self):
        node = MegapixelScaleNode()
        width, height = node.scale(1000, 1000, 1.0)
        assert width == 1000
        assert height == 1000

    def test_returns_tuple_of_ints(self):
        node = MegapixelScaleNode()
        result = node.scale(512, 512, 1.0)
        assert isinstance(result, tuple)
        assert len(result) == 2
        assert all(isinstance(v, int) for v in result)

    def test_minimum_size_clamped_to_one(self):
        node = MegapixelScaleNode()
        width, height = node.scale(1, 1_000_000, 0.01)
        assert width >= 1
        assert height >= 1
