def progress_bar(current, total, bar_length=30, prefix="", suffix="", fill="=", empty="-"):
    """
    Prints a progress bar on the previous line.

    Args:
        current (int): Current progress value.
        total (int): Total value for completion.
        bar_length (int): Length of the progress bar.
        prefix (str): String to display before the bar.
        suffix (str): String to display after the bar.
        fill (str): Character for filled part.
        empty (str): Character for empty part.
    """
    if current == 1:
        print()  # Ensure a blank line for the progress bar to overwrite
    percent = current / total if total else 0
    filled_length = int(bar_length * percent)
    bar = fill * filled_length + empty * (bar_length - filled_length)
    percent_display = round(percent * 100)
    # Move cursor up one line, then print the progress bar
    print(
        '\033[F' + f"{prefix}[{percent_display:3d}%] [{bar}]{suffix}".ljust(200), end='\r', flush=True)
