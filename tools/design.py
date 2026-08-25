from pathlib import Path
DESIGN_TEMPLATES = {"poster": ["assets", "exports", "refs", "poster_v1", "poster_v2"], "branding": ["assets", "exports", "logo_concepts", "color_palettes", "typography"], "ui": ["assets", "exports", "screens", "components", "prototypes"]}

def create_design_project(name: str, kind: str = "poster", base_path: str = None):
    safe_name = Path(name).name or "MyDesignProject"
    root = Path(base_path).expanduser() if base_path else Path.home() / "Desktop"
    project = root / safe_name; project.mkdir(parents=True, exist_ok=True)
    template = DESIGN_TEMPLATES.get(kind, DESIGN_TEMPLATES["poster"])
    for folder in template: (project / folder).mkdir(exist_ok=True)
    (project / "README.md").write_text(f"# {safe_name} ({kind})\n\nProject scaffold created by Ultron AI.\n", encoding="utf-8")
    return str(project)

def organize_assets(project_path: str):
    root = Path(project_path).expanduser(); assets = root / "assets"; assets.mkdir(exist_ok=True)
    for p in list(root.iterdir()):
        if p.name in {"assets", "exports", "refs", "README.md"} or not p.is_file(): continue
        if p.suffix.lower() in {".png", ".jpg", ".jpeg", ".svg", ".webp"}: p.rename(assets / p.name)
        elif p.suffix.lower() in {".ttf", ".otf"}:
            (assets / "fonts").mkdir(exist_ok=True); p.rename(assets / "fonts" / p.name)
    return str(assets)

def suggest_palette_from_names(names: list[str]):
    return {"primary": "#1F6FEB", "secondary": "#58A6FF", "accent": "#238636", "note": "Placeholder palette; refine in Figma or Photoshop."}

def analyze_design_context(screen_text: str) -> str:
    t = screen_text.lower(); hints = []
    if "figma" in t: hints.append("You seem to be working in Figma.")
    if "photoshop" in t or "psd" in t: hints.append("Looks like Photoshop or a PSD file.")
    if "illustrator" in t or ".ai" in t: hints.append("Possibly Adobe Illustrator.")
    if "brief" in t or "requirements" in t: hints.append("A brief or requirements document may be visible.")
    return " ".join(hints) or "OCR found text, but the design tool is unclear."
