"""EIA dosyalarını indirir. Yeni yıllık 861 sürümünü kendisi arar; kaynakların son değişme tarihini kaydeder."""
import datetime as dt
import json

import httpx

from . import ayar

BASLIK = {"User-Agent": "GridGrade data pipeline (+https://github.com/Scryne/gridgrade-site)"}


def _istemci() -> httpx.Client:
    # Yalnız IPv4: AAAA'sız alan adlarında DNS ~12 sn bekliyor (yerel makine); CI'da zararsız
    tasima = httpx.HTTPTransport(local_address="0.0.0.0", retries=3)
    return httpx.Client(headers=BASLIK, timeout=120, follow_redirects=True, transport=tasima)


def son_861_yili(c: httpx.Client, bugun: dt.date | None = None) -> int:
    """Yayımlanmış en yeni EIA-861 yılını bulur (ör. 2026'da 2025 ya da 2024)."""
    yil = (bugun or dt.date.today()).year - 1
    for y in range(yil, yil - 4, -1):
        r = c.head(ayar.EIA_861_ZIP.format(yil=y))
        if r.status_code == 200 and "zip" in r.headers.get("content-type", ""):
            return y
    raise RuntimeError("EIA-861 zip bulunamadı")


def indir() -> dict:
    ayar.HAM.mkdir(parents=True, exist_ok=True)
    with _istemci() as c:
        yil = son_861_yili(c)
        kayit = {}
        for ad, url in [("eia861m.xlsx", ayar.EIA_861M), ("eia861.zip", ayar.EIA_861_ZIP.format(yil=yil))]:
            r = c.get(url)
            r.raise_for_status()
            (ayar.HAM / ad).write_bytes(r.content)
            kayit[ad] = {"url": url, "boyut": len(r.content), "son_degisme": r.headers.get("last-modified", "")}
    kayit["eia861_yili"] = yil
    ayar.KAYNAK_KAYDI.parent.mkdir(parents=True, exist_ok=True)
    ayar.KAYNAK_KAYDI.write_text(json.dumps(kayit, indent=1), encoding="utf-8")
    return kayit
