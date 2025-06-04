import zipfile
import os
import time
from bakery.formater import progress_bar
import shutil


def decompress_sfx_exe(sfx_exe_path, output_folder):
    """
    Decompresses a self-extracting executable (SFX ZIP archive) into a specified folder,
    showing a progress bar.

    Args:
      sfx_exe_path (str): Path to the SFX executable file.
      output_folder (str): Path to the folder where the contents will be extracted.

    Raises:
      FileNotFoundError: If the SFX executable file does not exist.
      zipfile.BadZipFile: If the file is not a valid ZIP archive.
    """
    if not os.path.exists(sfx_exe_path):
        raise FileNotFoundError(f"The file '{sfx_exe_path}' does not exist.")

    if os.path.exists(output_folder):
        # Removing old files
        print("Removing old imports")
        shutil.rmtree(output_folder)
    else:
        os.makedirs(output_folder)

    start_time = time.time()  # Start timing

    with zipfile.ZipFile(sfx_exe_path, 'r') as zip_ref:
        members = zip_ref.namelist()
        total = len(members)
        print(f"Starting extracting ({total} files)")
        for i, member in enumerate(members, 1):
            zip_ref.extract(member, output_folder)
            progress_bar(i, total, bar_length=30, prefix="",
                         suffix=f" Extracting {member}")
        progress_bar(i, total, bar_length=30, prefix="",
                     suffix=f" Done ✅")
        print()  # Newline after progress bar

    end_time = time.time()  # End timing
    elapsed_time = end_time - start_time
    print(f"Imported source code in {elapsed_time:.2f} seconds")

# Example usage:
# decompress_sfx_exe("path/to/your/file.exe", "path/to/output/folder")
