from assets.import_sounds import import_minecraft_sounds
from assets.bake_sounds import bake_sounds
import time
import os

if __name__ == "__main__":
    start_time = time.time()
    minecraft_path = os.path.join(os.environ["APPDATA"], ".minecraft")
    print("\nIMPORTING SOUNDS")
    import_minecraft_sounds(
        minecraft_path,
        "./assets/imported_sounds",
        "24.json",
        import_map_file="./import_map.json"
    )
    print("\nBAKING SOUNDS")
    bake_sounds("./assets/imported_sounds", "./assets/sounds")
    elapsed = time.time() - start_time
    print(f"\n🎉 Baked all assets in {elapsed:.2f} seconds 🎉\n")
