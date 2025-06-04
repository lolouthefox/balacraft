import time
import os
import shutil
import json
import re
from assets.progress_bar import progress_bar


def import_minecraft_sounds(minecraft_dir, output_dir, index_file='24.json', import_map_file=None):
    """
    Copies selected Minecraft sound files from the assets directory to a custom output directory,
    using an import map JSON file listing filenames to import.

    Args:
        minecraft_dir (str): Path to the .minecraft directory.
        output_dir (str): Path to the output directory.
        index_file (str): Name of the index JSON file (default: '24.json').
        import_map_file (str, optional): Path to a JSON file containing a list of filenames to import.

    Returns:
        int: The total number of files imported.
    """

    start_time = time.time()
    print("Loading json")
    # Load objects from JSON file
    with open(os.path.join(minecraft_dir, 'assets', 'indexes', index_file), 'r', encoding='utf-8') as f:
        objects = json.load(f)['objects']

    # Load import map if provided
    import_map = None
    if import_map_file:
        with open(import_map_file, 'r', encoding='utf-8') as f:
            import_map_data = json.load(f)
            import_map = set(import_map_data.get("sounds", []))

    # Regex patterns
    sounds_pattern = re.compile(r'/sounds/')
    categories_pattern = re.compile(
        r'/(ambient|block|damage|dig|enchant|entity|event|fire|fireworks|item|liquid|minecart|mob|music|note|portal|random|records|step|title|ui)/'
    )

    # Removing old files
    print("Removing old imports")
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)

    # Collect files to import
    files_to_import = []
    for file_path in objects:
        if not sounds_pattern.search(file_path):
            continue
        if not categories_pattern.search(file_path):
            continue
        files_to_import.append(file_path)

    total_files = len(files_to_import)
    print(f"Starting import ({total_files} files)")

    file_count = 0
    bar_length = 30

    for file_path in files_to_import:
        hash_val = objects[file_path]['hash']
        object_path = os.path.join(
            minecraft_dir, 'assets', 'objects', hash_val[:2], hash_val)

        # Remove leading slash if present
        rel_path = file_path.lstrip('/')

        # Remove "minecraft/sounds/" prefix if present
        prefix = 'minecraft/sounds/'
        if rel_path.startswith(prefix):
            rel_path = rel_path[len(prefix):]

        # Determine if file should be prefixed with #
        output_rel_path = rel_path
        if import_map is not None:
            basename = os.path.basename(rel_path)
            if basename not in import_map:
                dirname = os.path.dirname(rel_path)
                filename = os.path.basename(rel_path)
                output_rel_path = os.path.join(
                    dirname, f"#{filename}") if dirname else f"#{filename}"

        output_path = os.path.join(output_dir, output_rel_path)

        # Ensure target directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        shutil.copy2(object_path, output_path)
        file_count += 1

        # Progress bar
        progress_bar(file_count, total_files, bar_length=30,
                     prefix="", suffix=f" Moving {output_rel_path}")

    print()  # Newline after progress bar
    elapsed = time.time() - start_time
    print(f"Import finished in {elapsed:.2f} seconds")
    print(f"Total files imported: {file_count}")
    return file_count
