"""Small, inspectable planning layer used by the web UI."""
from llm.client import call_llm
from llm.prompts import ULTRON_SYSTEM_PROMPT

ACTIONS = {
    "open_app": {"requires_confirmation": True, "description": "Open an installed application"},
    "search_web": {"requires_confirmation": True, "description": "Open a web search"},
    "create_folder": {"requires_confirmation": True, "description": "Create a folder"},
    "click": {"requires_confirmation": True, "description": "Click at a screen coordinate"},
    "type": {"requires_confirmation": True, "description": "Type text into the focused application"},
    "hotkey": {"requires_confirmation": True, "description": "Press an allow-listed keyboard shortcut"},
    "describe_screen": {"requires_confirmation": False, "description": "Read visible screen text with OCR"},
}

def plan_for(text: str):
    t = text.lower()
    steps = []
    if any(word in t for word in ("screen", "see", "look")): steps.append({"action": "describe_screen", "label": "Read visible screen text"})
    if "search" in t or "google" in t: steps.append({"action": "search_web", "label": "Open a browser search", "requires_confirmation": True})
    if "open" in t and any(app in t for app in ("chrome", "firefox", "edge", "code")): steps.append({"action": "open_app", "label": "Open the requested application", "requires_confirmation": True})
    if not steps: steps.append({"action": "respond", "label": "Ask Ultron for a response", "requires_confirmation": False})
    return {"goal": text, "steps": steps, "safety": "Actions marked confirmation will not run until you approve them."}

def respond(text: str):
    return call_llm(ULTRON_SYSTEM_PROMPT, text).message.content
