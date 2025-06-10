from bakery.import_sounds import import_minecraft_sounds
from bakery.bake_sounds import bake_sounds
from bakery.get_balatro_source import decompress_sfx_exe
from bakery.bake_assets import resize_images_to_2x
import time
import os
import argparse
from rich import print

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Bake Minecraft assets.")
    parser.add_argument(
        "--bake",
        action="store_true",
        help="Include this flag to bake the project's assets. Run with the --bake-all flag first to run first time imports."
    )
    parser.add_argument(
        "--bake-all",
        action="store_true",
        help="Include this flag to bake all assets."
    )
    args = parser.parse_args()

    start_time = time.time()
    minecraft_path = os.path.join(os.environ["APPDATA"], ".minecraft")

    if args.bake or args.bake_all:
        if args.bake_all:
            print("\n[bold magenta]IMPORTING SOUNDS[/bold magenta]")
            import_minecraft_sounds(
                minecraft_path,
                "./assets/imported_sounds",
                "24.json",
                import_map_file="./import_map.json"
            )

        print("\n[bold magenta]BAKING SOUNDS[/bold magenta]")
        bake_sounds("./assets/imported_sounds", "./assets/sounds")

        print("\n[bold magenta]BAKING TEXTURES[/bold magenta]")
        resize_images_to_2x("./assets/1x", "./assets/2x")

        if args.bake_all:
            print("\n[bold magenta]IMPORTING BALATRO SOURCE[/bold magenta]")
            decompress_sfx_exe(
                "C:/Program Files (x86)/Steam/steamapps/common/Balatro/Balatro.exe",
                "./dependencies/balatro_source"
            )

    elapsed = time.time() - start_time
    print(f"\n🎉 Process completed in {elapsed:.2f} seconds 🎉\n")
