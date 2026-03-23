try:
    from .feroc_node import RandomLineFromText
    from .load_description_node import LoadDescriptionNode

    NODE_CLASS_MAPPINGS = {
        "RandomLineFromText": RandomLineFromText,
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