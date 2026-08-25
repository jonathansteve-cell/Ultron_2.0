# Ultron AI — Complete Build

A practical, experimental desktop assistant for designer students. Ultron combines a FastAPI server, optional Gemini LLM integration, safe local tools, OCR screen awareness, a browser orb interface, and a HoloMat marker-projection demo.

## Quick start

```bash
python -m venv .venv
# Windows: .venv\\Scripts\\activate
source .venv/bin/activate
pip install -r requirements.txt
cp config/sample.env config/.env   # Windows: copy config\\sample.env config\\.env
uvicorn server.main:app --host 0.0.0.0 --port 8000
```

Open `http://localhost:8000/` for chat or `/orb` for the orb. The browser uses relative API URLs, so it also works through a LAN or hosted preview. Without a provider key, chat uses a local mock response. Screen vision and projector demos need a machine with the relevant camera/display permissions.

## Optional configuration

Edit `config/.env` and set `LLM_PROVIDER=google` plus `GOOGLE_API_KEY`. The provider/model can be changed with `GOOGLE_MODEL`. Do not commit credentials. Run tests with `pytest`.

## Safety

Actions such as opening programs, creating folders, launching a browser search, and screen capture happen on the host running FastAPI. Run this service only on a trusted network. The tool layer intentionally avoids arbitrary shell execution.

## HoloMat demo

```bash
python demos/demo_marker_projection.py --camera 0 --display 1
```

The demo tracks red/blue markers, draws a ruler between the first two objects, and provides keyboard/button-style controls. Press `q` to quit, `c` to clear points, or `m` to toggle the ruler.
