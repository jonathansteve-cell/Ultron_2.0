import re
from llm.schemas import Command

def route_intent(text: str) -> Command:
    original = text.strip()
    t = original.lower()
    if re.search(r"\b(open|launch|start)\b", t) and any(x in t for x in ("chrome", "browser", "firefox", "edge")):
        app = next((x for x in ("chrome", "firefox", "edge") if x in t), "chrome")
        return Command(intent="open_browser", normalized_text=original, tool="open_app", params={"app_name": app}, confidence=.9)
    if "create" in t and "folder" in t:
        return Command(intent="create_folder", normalized_text=original, tool="create_folder", params={"path": "Desktop/UltronFolder"}, confidence=.8)
    if "search" in t or "google" in t:
        query = re.sub(r"\b(search|for|on|google)\b", " ", original, flags=re.I).strip()
        return Command(intent="search_web", normalized_text=original, tool="search_web", params={"query": query or "HoloMat projector camera"}, confidence=.7)
    return Command(intent="generic", normalized_text=original, confidence=.5)
