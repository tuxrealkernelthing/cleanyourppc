import os
import platform
import tempfile
from pathlib import Path

# Renkler
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'

def banner():
    print(f"{Colors.HEADER}{Colors.BOLD}\n===============================")
    print("        CleanYourPC v1.0       ")
    print("===============================\n{Colors.END}")

def footer():
    print(f"\n{Colors.CYAN}{Colors.BOLD}CleanYourPC v1.0{Colors.END}  "
          f"{Colors.GREEN}by Mami{Colors.END}  "
          f"{Colors.YELLOW}This project is secured by GPL 3.0 license{Colors.END}\n")

def get_os():
    return platform.system()

def get_file_size(file_path):
    try:
        return os.path.getsize(file_path)
    except OSError:
        return 0

def list_files_with_size(directory):
    files = []
    total_size = 0
    if os.path.exists(directory):
        for root, dirs, filenames in os.walk(directory):
            for f in filenames:
                path = os.path.join(root, f)
                size = get_file_size(path)
                files.append((path, size))
                total_size += size
    return files, total_size

def list_temp_files():
    temp_dir = tempfile.gettempdir()
    return list_files_with_size(temp_dir)

def list_trash_files():
    system = get_os()
    home = str(Path.home())

    if system == "Windows":
        trash_dir = os.path.join(home, "Recycle.Bin")
    elif system == "Darwin":  # macOS
        trash_dir = os.path.join(home, ".Trash")
    else:  # Linux
        trash_dir = os.path.join(home, ".local", "share", "Trash", "files")

    return list_files_with_size(trash_dir)

def list_cache_files():
    system = get_os()
    home = str(Path.home())

    if system == "Windows":
        cache_dir = os.path.join(home, "AppData", "Local", "Temp")
    else:
        cache_dir = os.path.join(home, ".cache")

    return list_files_with_size(cache_dir)

def format_size(size_bytes):
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_bytes < 1024:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.2f} PB"

def display_files(category, files_with_size, total_size, color):
    print(f"{color}\n--- {category} ---{Colors.END}")
    for path, size in files_with_size:
        print(f"{path} ({format_size(size)})")
    print(f"{color}Toplam boyut: {format_size(total_size)}{Colors.END}")

def main():
    banner()
    temp_files, temp_size = list_temp_files()
    trash_files, trash_size = list_trash_files()
    cache_files, cache_size = list_cache_files()

    display_files("Geçici Dosyalar", temp_files, temp_size, Colors.YELLOW)
    display_files("Çöp Kutusu Dosyaları", trash_files, trash_size, Colors.RED)
    display_files("Cache Dosyaları", cache_files, cache_size, Colors.BLUE)

    footer()

if __name__ == "__main__":
    main()
