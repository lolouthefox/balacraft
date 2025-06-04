import os
import shutil
import time
import re
from .progress_bar import progress_bar


def flatten_and_rename_files(src_dir, dest_dir):
    # Map: {normalized_key: (abs_path, new_filename)}
    unique_files = {}
    for root, _, files in os.walk(src_dir):
        rel_path = os.path.relpath(root, src_dir)
        safe_path = rel_path.replace(os.sep, "_")
        if safe_path == ".":
            safe_path = ""
        for file in files:
            if file.startswith("#"):
                continue  # Ignore files that start with #
            name, ext = os.path.splitext(file)
            # Match pattern: name ending with digits (e.g., test1.ogg)
            m = re.match(r"^(.*?)(\d+)$", name)
            if m:
                base_name = m.group(1)
                normalized_name = base_name
            else:
                normalized_name = name
            # Build new filename (preserving path format)
            new_filename = f"mc__{safe_path}__{normalized_name}{ext}" if safe_path else f"mc__{normalized_name}{ext}"
            # Use (safe_path, normalized_name, ext) as key
            key = (safe_path, normalized_name, ext)
            if key not in unique_files:
                abs_path = os.path.join(root, file)
                unique_files[key] = (abs_path, new_filename)

    files_to_bake = len(unique_files)
    files_baked = 0

    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    print(f"Starting baking ({files_to_bake} files)")

    for _, (abs_path, new_filename) in unique_files.items():
        files_baked += 1
        progress_bar(files_baked, files_to_bake, bar_length=30,
                     prefix="", suffix=f" Moving {new_filename}")
        dest_path = os.path.join(dest_dir, new_filename)
        shutil.copy2(abs_path, dest_path)


def bake_sounds(source_folder, destination_folder):
    start_time = time.time()
    print("Deleting old sounds")
    if os.path.exists(destination_folder):
        shutil.rmtree(destination_folder)
    print("Moving files")
    flatten_and_rename_files(source_folder, destination_folder)
    elapsed = time.time() - start_time
    print(f"\nBaked sounds in {elapsed:.2f} seconds")
