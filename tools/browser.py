import urllib.parse, webbrowser

def open_url(url: str):
    return webbrowser.open(url)

def search_web(query: str, engine: str = "google"):
    host = "www.google.com/search" if engine == "google" else "www.bing.com/search"
    return open_url(f"https://{host}?q={urllib.parse.quote_plus(query)}")
