"""static/og.png (1200x630) paylaşım görseli; elle, gerektiğinde çalıştırılır."""
from pathlib import Path

from playwright.sync_api import sync_playwright

KOK = Path(__file__).resolve().parents[1]
HTML = """<!doctype html><meta charset=utf-8>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,650&family=Inter:wght@500;700&display=swap" rel="stylesheet">
<style>*{margin:0;box-sizing:border-box}body{width:1200px;height:630px;background:#FAF8F3;font-family:Inter;color:#17181C;
padding:70px 80px;position:relative;border-top:10px solid #F2B705}
.logo{display:flex;align-items:center;gap:14px;font:650 40px Fraunces}h1{font:650 68px/1.05 Fraunces;margin-top:46px;max-width:760px;letter-spacing:-.02em}
p{font-size:26px;color:#5B616B;margin-top:22px;max-width:700px}.g{position:absolute;right:80px;top:150px;display:grid;gap:14px}
.g span{display:grid;place-items:center;width:86px;height:86px;border-radius:14px;color:#fff;font:650 54px Fraunces}</style>
<div class=logo><svg viewBox="0 0 32 32" width="52" height="52"><rect width="32" height="32" rx="7" fill="#17181C"/><path d="M18.5 4 8 18h7l-2 10 11-15h-7z" fill="#F2B705"/></svg>GridGrade</div>
<h1>US electricity prices and utility report cards</h1><p>Every state, utility and county, graded on price and reliability. Rebuilt from public EIA data.</p>
<div class=g><span style="background:#1E8550">A</span><span style="background:#C99A00;color:#17181C">C</span><span style="background:#C2302A">F</span></div>"""
with sync_playwright() as p:
    b = p.chromium.launch(executable_path=str(Path.home() / "AppData/Local/ms-playwright/chromium-1243/chrome-win64/chrome.exe"))
    s = b.new_page(viewport={"width": 1200, "height": 630})
    s.set_content(HTML)
    s.wait_for_timeout(1500)
    s.screenshot(path=str(KOK / "static" / "og.png"))
    b.close()
