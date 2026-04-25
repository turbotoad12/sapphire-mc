# MADE WITH AI XD

import shutil
import subprocess
import sys
import tempfile
from datetime import datetime
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parent
SERVER_DIR = ROOT_DIR / "server"
START_SCRIPT = SERVER_DIR / "start.bat"
PROXY_DIR = ROOT_DIR / "proxy"
PROXY_START_BAT = PROXY_DIR / "start.bat"
PROXY_START_SH = PROXY_DIR / "start.sh"
WORLDS = [
    SERVER_DIR / "world",
    SERVER_DIR / "world_nether",
    SERVER_DIR / "world_the_end",
]
BACKUP_DIR = ROOT_DIR / "backups"


def run_start_script() -> None:
    if not START_SCRIPT.exists():
        print(f"Error: Could not find start script at {START_SCRIPT}")
        sys.exit(1)

    subprocess.run(["cmd", "/c", "start.bat"], cwd=SERVER_DIR, check=False)


def run_proxy_script() -> None:
    if sys.platform.startswith("win"):
        if not PROXY_START_BAT.exists():
            print(f"Error: Could not find proxy start script at {PROXY_START_BAT}")
            sys.exit(1)
        subprocess.run(["cmd", "/c", "start.bat"], cwd=PROXY_DIR, check=False)
        return

    if not PROXY_START_SH.exists():
        print(f"Error: Could not find proxy start script at {PROXY_START_SH}")
        sys.exit(1)
    subprocess.run(["sh", "start.sh"], cwd=PROXY_DIR, check=False)


def reset_world() -> None:
    for world_path in WORLDS:
        shutil.rmtree(world_path, ignore_errors=True)
    print("World folders deleted.")


def backup_world() -> None:
    existing_worlds = [path for path in WORLDS if path.exists()]
    if not existing_worlds:
        print("No world folders found to back up.")
        return

    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    archive_path = BACKUP_DIR / f"world-backup-{timestamp}"

    # Stage only world folders so backup zip stays focused and smaller.
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        for world_path in existing_worlds:
            shutil.copytree(world_path, temp_path / world_path.name)
        shutil.make_archive(str(archive_path), "zip", root_dir=temp_path, base_dir=".")

    print(f"Backup created: {archive_path.with_suffix('.zip')}")


def status() -> None:
    print("Server directory:", SERVER_DIR)
    print("Start script:", "found" if START_SCRIPT.exists() else "missing")
    print("Proxy script (bat):", "found" if PROXY_START_BAT.exists() else "missing")
    print("Proxy script (sh):", "found" if PROXY_START_SH.exists() else "missing")
    print()
    print("World folders:")
    for world_path in WORLDS:
        print(f"  {world_path.name}: {'present' if world_path.exists() else 'missing'}")


def print_help() -> None:
    print("Usage: python manage.py <command>")
    print()
    print("Commands:")
    print("  start        Start the server")
    print("  start_proxy  Start the proxy")
    print("  start_all    Start server and proxy")
    print("  reset_world  Delete world folders and start the server")
    print("  backup       Create a timestamped zip backup")
    print("  status       Show basic server/world status")
    print("  help         Show this message")


if __name__ == "__main__":
    command = sys.argv[1] if len(sys.argv) > 1 else "help"

    if command in {"help", "-h", "--help"}:
        print_help()
    elif command == "start":
        run_start_script()
    elif command == "start_proxy":
        run_proxy_script()
    elif command == "start_all":
        run_start_script()
        run_proxy_script()
    elif command == "reset_world":
        reset_world()
        run_start_script()
    elif command == "backup":
        backup_world()
    elif command == "status":
        status()
    else:
        print(f"Unknown command: {command}")
        print()
        print_help()
        sys.exit(1)


