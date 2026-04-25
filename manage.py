import shutil
import subprocess
import sys





def print_help() -> None:
    print("Usage: python manage.py <command>")
    print()
    print("Commands:")
    print("  start        Start the server")
    print("  reset_world   Delete world folders and start the server")
    print("  help         Show this message")


if __name__ == "__main__":
    command = sys.argv[1] if len(sys.argv) > 1 else "help"
    if command in {"help", "-h", "--help"}:
        print_help()
    elif command == "start":
        subprocess.run(["cmd", "/c", "start.bat"], cwd="server", check=False)
    elif command == "reset_world":
        shutil.rmtree("server/world", ignore_errors=True)
        shutil.rmtree("server/world_nether", ignore_errors=True)
        shutil.rmtree("server/world_the_end", ignore_errors=True)
        subprocess.run(["cmd", "/c", "start.bat"], cwd="server", check=False)
    else:
        print_help()
        sys.exit(1)


