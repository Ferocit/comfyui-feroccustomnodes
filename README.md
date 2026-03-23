# ComfyUI-Feroc Custom Nodes

This repository contains custom nodes for ComfyUI, designed to enhance your workflow with text-based operations, particularly for managing and utilizing descriptive texts.

## Installation

1. **Clone this repository** into your `ComfyUI/custom_nodes/` directory:
    ```bash
    cd ComfyUI/custom_nodes/
    git clone https://github.com/Ferocit/comfyui-feroccustomnodes.git
    ```
2. **Restart ComfyUI** to load the new nodes.

## Nodes Included

### 1. `LoadDescriptionNode` (Category: Feroc)

Loads a text file from the `descriptions` folder inside this plugin's directory. Ideal for managing character descriptions, lore, or any other text snippets you frequently use in your workflows.

**Inputs:**

* `file_path` (Dropdown): A dynamic list of all `.txt` files found recursively under the `descriptions` folder, including their subdirectory path (e.g., `characters/lyraniel_stormweaver.txt`).

**Outputs:**

* `description_text` (STRING): The full content of the selected text file.
* `description_name` (STRING): The filename without extension (e.g., `lyraniel_stormweaver`).

**Usage:**

Place your `.txt` files inside `ComfyUI/custom_nodes/comfyui-feroccustomnodes/descriptions/`. Subdirectories are supported (e.g., `descriptions/characters/my_character.txt`).

If no `.txt` files exist yet, the node automatically creates `descriptions/examples/example.txt` as a placeholder.

---

### 2. `RandomLineFromText` (Category: Feroc)

Selects a random line from one or more text files. Useful for injecting variability into prompts by drawing from a pool of predefined lines.

**Inputs:**

* `seed` (INT): Seed for reproducible random selection. The same seed always produces the same output.
* `file_path_1` to `file_path_5` (STRING, Optional): Absolute paths to text files. Up to 5 files can be provided.

**Outputs:**

* (STRING): A newline-separated string of randomly selected lines, one from each provided file.

**Usage:**

Provide the full absolute path to your text files (e.g., `/home/user/my_lines.txt`). The node reads each file, picks a random non-empty line, and combines them into a single output string. Missing or unreadable files are skipped and logged.

---

## Development

Run tests with:
```bash
python -m pytest tests/ -v
```

## Contributing

Feel free to open issues or pull requests if you have suggestions or improvements.
