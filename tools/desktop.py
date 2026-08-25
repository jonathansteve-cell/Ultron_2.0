"""Conservative desktop controls for the local Ultron agent.

Every potentially impactful action is explicit and allow-listed. The UI should
request confirmation before calling click, type, or hotkey.
"""
from __future__ import annotations
from typing import Any

try:
    import pyautogui
except ImportError:  # Optional dependency: the rest of Ultron still works.
    pyautogui = None

SAFE_HOTKEYS = {"ctrl+c", "ctrl+v", "ctrl+x", "ctrl+s", "ctrl+z", "alt+tab", "esc"}

def _require():
    if pyautogui is None:
        raise RuntimeError("Desktop control is unavailable. Install pyautogui first.")
    pyautogui.PAUSE = 0.08

def screenshot():
    _require()
    return pyautogui.screenshot()

def move_mouse(x: int, y: int):
    _require(); pyautogui.moveTo(int(x), int(y), duration=.2)
    return {"x": int(x), "y": int(y)}

def click_mouse(x: int, y: int, button: str = "left"):
    _require()
    if button not in {"left", "right"}: raise ValueError("Only left and right clicks are allowed")
    pyautogui.click(int(x), int(y), button=button)
    return {"clicked": [int(x), int(y)], "button": button}

def type_text(text: str):
    _require()
    if len(text) > 500: raise ValueError("Text input is limited to 500 characters")
    pyautogui.write(text, interval=.01)
    return {"typed_characters": len(text)}

def press_hotkey(combo: str):
    _require()
    combo = combo.lower().replace(" ", "")
    if combo not in SAFE_HOTKEYS: raise ValueError(f"Hotkey is not allow-listed: {combo}")
    pyautogui.hotkey(*combo.split("+"))
    return {"hotkey": combo}
