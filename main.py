from bakery.import_sounds import import_minecraft_sounds
from bakery.bake_sounds import bake_sounds
from bakery.get_balatro_source import decompress_sfx_exe
import time
import os
import argparse
from rich import print

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Bake Minecraft assets.")
    parser.add_argument(
        "--bake",
        action="store_true",
        help="Include this flag to bake sounds after importing."
    )
    parser.add_argument(
        "--skip-import",
        action="store_true",
        help="Include this flag to skip importing sounds."
    )
    args = parser.parse_args()

    start_time = time.time()
    minecraft_path = os.path.join(os.environ["APPDATA"], ".minecraft")

    if args.bake:
        if not args.skip_import:
            print("\n[bold magenta]IMPORTING SOUNDS[/bold magenta]")
            import_minecraft_sounds(
                minecraft_path,
                "./assets/imported_sounds",
                "24.json",
                import_map_file="./import_map.json"
            )

        print("\n[bold magenta]BAKING SOUNDS[/bold magenta]")
        bake_sounds("./assets/imported_sounds", "./assets/sounds")

        print("\n[bold magenta]IMPORTING BALATRO SOURCE[/bold magenta]")
        decompress_sfx_exe(
            "C:/Program Files (x86)/Steam/steamapps/common/Balatro/Balatro.exe",
            "./dependencies/balatro_source"
        )

    elapsed = time.time() - start_time
    print(f"\n🎉 Process completed in {elapsed:.2f} seconds 🎉\n")
