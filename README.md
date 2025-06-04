# ⛏️ Balacraft
A Balatro mod that adds Minecraft related content to your game!

## Installation
Go to the releases section on the right. Select latest release. Please note that you need Steamodded and Lovely (LÖVE injector). Latest version always prefered. If you find any bug, don't hesitate to open an issue!

## Developpement
### Requirements
- Be on windows
- Have Minecraft latest minecraft version installed using the default launcher (launched at least once)
- Have python 3 installed
- Have Balatro installed (through steam preferably)
- Have WinRar or similar installed

### Running the baker
1. Open powershell
2. Create a python environement: ```python3 -m venv ./.venv```
3. Activate the [environement based on your OS](https://docs.python.org/3/library/venv.html#how-venvs-work), here is an example for windows: ```./.venv/Scripts/Activate.ps1```
4. Install the dependencies: ```python3 -m pip install -r ./requirements.txt```
5. Run the bakery: ```python3 ./main.py --bake```

### Bakery tips:
- To bake the whole project you can simply use the `--bake` flag.
- You dont need to reimport everything everytime, it do be a very long process and it can help to skip it if already imported using the `--skip-import` flag.

*Not an official Minecraft product. Not affiliated with Mojang nor Microsoft.*
