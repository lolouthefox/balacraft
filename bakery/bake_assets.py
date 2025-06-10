import os
from PIL import Image  # type: ignore
from bakery.formater import progress_bar
import shutil
import time


def resize_images_to_2x(input_folder, output_folder):
    """
    Resizes all images in the input folder to 2x size and saves them in the output folder.

    Args:
      input_folder (str): Path to the folder containing the original images.
      output_folder (str): Path to the folder where resized images will be saved.
    """
    start_time = time.time()
    print(f"Deleting old renders")
    if os.path.exists(output_folder):
        shutil.rmtree(output_folder)
    os.makedirs(output_folder)

    # Gather all image files first
    image_files = [
        filename for filename in os.listdir(input_folder)
        if os.path.isfile(os.path.join(input_folder, filename))
        and filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif'))
    ]
    total_files = len(image_files)
    processed = 0

    print(f"Starting resizing ({total_files} files)")

    for filename in image_files:
        input_path = os.path.join(input_folder, filename)
        with Image.open(input_path) as img:
            new_size = (img.width * 2, img.height * 2)
            resized_img = img.resize(new_size, Image.Resampling.NEAREST)
            output_path = os.path.join(output_folder, filename)
            resized_img.save(output_path)
        processed += 1
        progress_bar(processed, total_files, bar_length=30,
                     prefix="", suffix=f" Resizing {filename}")
    if total_files > 0:
        progress_bar(processed, total_files, bar_length=30,
                     prefix="", suffix=" Done ✅")

    elapsed = time.time() - start_time
    print(f"\nExported 2x textures in {elapsed:.2f} seconds")

# Example usage:
# resize_images_to_2x("path/to/input_folder", "path/to/output_folder")
