import os
from pathlib import Path
from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel
from dotenv import load_dotenv
from llm.client import call_llm
from llm.prompts import ULTRON_SYSTEM_PROMPT
from core.intent_router import route_intent
from tools.apps import open_app
from tools.files import create_folder
from tools.browser import search_web
from tools.design import create_design_project, organize_assets, suggest_palette_from_names, analyze_design_context, DESIGN_TEMPLATES
from tools.screen_vision import describe_screen

load_dotenv("config/.env")
app = FastAPI(title="Ultron AI — Complete Build")
class ChatRequest(BaseModel): message: str

def page(name): return HTMLResponse((Path(__file__).parent / name).read_text(encoding="utf-8"))
@app.get("/")
async def root(): return page("chat_ui.html")
@app.get("/orb")
async def orb(): return page("orb_ui.html")
@app.get("/pwa")
async def pwa_manifest():
    return JSONResponse({"name":"Ultron Designer","short_name":"Ultron","start_url":"/orb","display":"standalone","background_color":"#05080d","theme_color":"#1f6feb","icons":[]})
@app.get("/health")
async def health(): return {"status":"ok"}
@app.get("/vision/describe")
async def vision_describe():
    try:
        desc = describe_screen(); return {"screen_text": desc, "context": analyze_design_context(desc)}
    except Exception as exc: return JSONResponse({"error": str(exc)}, status_code=500)
@app.post("/chat")
async def chat(req: ChatRequest):
    text = req.message.strip(); t = text.lower()
    if not text: return {"reply":"Please enter a command."}
    if "see" in t and any(x in t for x in ("screen", "display", "monitor")):
        try:
            desc = describe_screen(); context = analyze_design_context(desc)
            prompt = f"The user asked: {text}\nOCR: {desc}\nContext: {context}\nAnswer in 2–4 sentences."
            return {"reply": call_llm(ULTRON_SYSTEM_PROMPT, prompt).message.content}
        except Exception as exc: return {"reply": f"Screen vision error: {exc}"}
    if "create" in t and ("project" in t or "scaffold" in t):
        kind = next((k for k in DESIGN_TEMPLATES if k in t), "poster")
        marker = "named" if "named" in t else "name" if "name" in t else None
        name = text.split(marker, 1)[-1].strip().split()[0] if marker else "MyDesignProject"
        return {"reply": f"Executed: created {kind} project '{name}' at {create_design_project(name, kind)}"}
    if "organize" in t and ("assets" in t or "project" in t):
        target = str(Path.home() / "Desktop" / "MyDesignProject")
        try: return {"reply": f"Executed: organized assets in {organize_assets(target)}"}
        except Exception as exc: return {"reply": f"Failed to organize assets: {exc}"}
    if "palette" in t or "color" in t:
        p = suggest_palette_from_names(["designer"])
        return {"reply": f"Suggested palette:\n- Primary: {p['primary']}\n- Secondary: {p['secondary']}\n- Accent: {p['accent']}\nNote: {p['note']}"}
    cmd = route_intent(text)
    try:
        if cmd.tool == "open_app": open_app(cmd.params["app_name"]); reply = f"Executing: opening {cmd.params['app_name']}."
        elif cmd.tool == "create_folder": reply = f"Executing: created folder at {create_folder(cmd.params['path'])}."
        elif cmd.tool == "search_web": search_web(cmd.params["query"]); reply = f"Executing: searching web for '{cmd.params['query']}'."
        else: reply = call_llm(ULTRON_SYSTEM_PROMPT, text).message.content
    except Exception as exc: reply = f"I could not complete that action: {exc}"
    return {"reply": reply}
