from pathlib import Path

def create_folder(path: str):
    p = Path(path).expanduser()
    p.mkdir(parents=True, exist_ok=True)
    return str(p)

def search_files(query: str, root_path: str = None):
    root = Path(root_path).expanduser() if root_path else Path.home()
    results = []
    try:
        for p in root.rglob(f"*{query}*"):
            if p.is_file(): results.append(str(p))
            if len(results) >= 50: break
    except (OSError, PermissionError):
        pass
    return results
