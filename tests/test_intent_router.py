from core.intent_router import route_intent

def test_open_browser_tool_call():
    cmd = route_intent("Open Chrome for me")
    assert cmd.tool == "open_app" and cmd.params["app_name"] == "chrome"

def test_create_folder_tool_call():
    assert route_intent("Create a folder named HoloMat on Desktop").tool == "create_folder"

def test_search_web_tool_call():
    cmd = route_intent("Search for HoloMat projector camera")
    assert cmd.tool == "search_web" and "HoloMat projector camera" in cmd.params["query"]
