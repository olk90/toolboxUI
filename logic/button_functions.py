import shutil
import subprocess


def enter_selected_container(selection_model):
    if not selection_model.hasSelection():
        print("No container selected.")
        return

    selected_row = selection_model.selectedColumns()[1]  # Assuming 'CONTAINER NAME' is in column 1
    container_name = selected_row.data()
    if not container_name:
        print("Failed to retrieve container name.")
        return

    spawn_terminal_with_command(f"toolbox enter {container_name}")


def spawn_terminal_with_command(command):
    """
    Spawn a terminal emulator and execute the specified command.

    Args:
        command (str): The command to execute in the terminal

    Returns:
        bool: True if a terminal was successfully launched, False otherwise
    """
    # Dictionary of common terminal emulators and their command execution options
    terminal_exec_flags = {
        "konsole": ["--noclose", "-e"],  # KDE's terminal
        "gnome-terminal": ["--", "bash", "-c"],  # GNOME's terminal
        "xfce4-terminal": ["--command"],  # XFCE's terminal
        "alacritty": ["-e"],  # Alacritty
        "kitty": ["-e"],  # Kitty
        "terminator": ["-x"],  # Terminator
        "xterm": ["-e"],  # xterm
        "tilix": ["-e"]  # Tilix
    }

    # Try each terminal in the list
    for terminal, flags in terminal_exec_flags.items():
        if shutil.which(terminal):  # Check if the terminal is available
            try:
                if terminal == "gnome-terminal":
                    # Special case for gnome-terminal which needs a different structure
                    subprocess.Popen([terminal] + flags + [f"{command}; exec bash"])
                else:
                    # For other terminals, flags come first, then the full command
                    subprocess.Popen([terminal] + flags + [command])
                return True
            except subprocess.SubprocessError as e:
                print(f"Failed to launch {terminal}: {e}")
                continue

    # If no specific terminal worked, try a generic approach with xdg-terminal-exec
    # Note: xdg-terminal-exec may not support passing commands directly
    try:
        if shutil.which("xdg-terminal-exec"):
            subprocess.Popen(["xdg-terminal-exec"])
            print("Warning: Launched default terminal but could not pass command to it")
            return True
    except (subprocess.SubprocessError, FileNotFoundError):
        pass

    # If we get here, no terminal could be launched
    print("Could not find or launch any terminal emulator")
    return False
