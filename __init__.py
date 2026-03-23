try:
    from .random_line_from_text_node import RandomLineFromTextNode
    from .load_description_node import LoadDescriptionNode

    NODE_CLASS_MAPPINGS = {
        "RandomLineFromText": RandomLineFromTextNode,
        "LoadDescriptionNode": LoadDescriptionNode,
    }

    NODE_DISPLAY_NAME_MAPPINGS = {
        "RandomLineFromText": "Random Line From Text",
        "LoadDescriptionNode": "Load Description",
    }

    __all__ = [
        'NODE_CLASS_MAPPINGS',
        'NODE_DISPLAY_NAME_MAPPINGS',
    ]
except ImportError:
    # Outside of a ComfyUI package context (e.g., running tests standalone)
    pass