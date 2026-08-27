try:
    from .random_line_from_text_node import RandomLineFromTextNode
    from .load_description_node import LoadDescriptionNode
    from .text_template_node import TextTemplateNode
    from .megapixel_scale_node import MegapixelScaleNode

    NODE_CLASS_MAPPINGS = {
        "RandomLineFromText": RandomLineFromTextNode,
        "LoadDescriptionNode": LoadDescriptionNode,
        "TextTemplate": TextTemplateNode,
        "MegapixelScale": MegapixelScaleNode,
    }

    NODE_DISPLAY_NAME_MAPPINGS = {
        "RandomLineFromText": "Random Line From Text",
        "LoadDescriptionNode": "Load Description",
        "TextTemplate": "Text Template",
        "MegapixelScale": "Megapixel Scale",
    }

    __all__ = [
        'NODE_CLASS_MAPPINGS',
        'NODE_DISPLAY_NAME_MAPPINGS',
    ]
except ImportError:
    # Outside of a ComfyUI package context (e.g., running tests standalone)
    pass