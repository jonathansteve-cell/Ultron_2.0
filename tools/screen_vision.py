import mss
import pytesseract
from PIL import Image

def capture_screen_region(mon=1, left=0, top=0, width=None, height=None):
    with mss.mss() as sct:
        monitors = sct.monitors; mon = mon if 0 <= mon < len(monitors) else 1
        rect = monitors[mon] if width is None or height is None else {"left": left, "top": top, "width": width, "height": height}
        img = sct.grab(rect)
        return Image.frombytes("RGB", img.size, img.bgra, "raw", "BGRX")

def ocr_image(image: Image.Image) -> str: return pytesseract.image_to_string(image)

def describe_screen(mon=1) -> str:
    lines = [line.strip() for line in ocr_image(capture_screen_region(mon)).splitlines() if line.strip()]
    return "I see a screen, but OCR did not detect any text." if not lines else "I captured your screen and read some text:\n" + " ".join(lines[:40])
