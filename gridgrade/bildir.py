"""IndexNow: site haritasındaki URL'leri Bing/Yandex'e bildirir. Yalnız site değiştiğinde çağrılır (yayın iş akışı)."""
import re
from urllib.parse import urlparse

import httpx

from . import ayar


def bildir() -> int:
    harita = (ayar.DIST / "sitemap.xml").read_text(encoding="utf-8")
    urller = re.findall(r"<loc>(.*?)</loc>", harita)[:10_000]
    govde = {"host": urlparse(ayar.SITE_URL).netloc, "key": ayar.INDEXNOW_ANAHTARI,
             "keyLocation": f"{ayar.SITE_URL}/{ayar.INDEXNOW_ANAHTARI}.txt", "urlList": urller}
    r = httpx.post(ayar.INDEXNOW_UCU, json=govde, timeout=60)
    if r.status_code not in (200, 202):
        raise RuntimeError(f"IndexNow {r.status_code}: {r.text[:200]}")
    return len(urller)
