"""Derleme sonrası ürün kontrolü: kırık iç bağlantı, eksik/yinelenen başlık ve açıklama, sızan 'None'/'nan', site haritası."""
import re
from collections import Counter
from html.parser import HTMLParser

from . import ayar

SIZINTI = re.compile(r">[^<]*\b(None|nan|undefined|NaN)\b[^<]*<|\{\{|\{%")


class _Okuyucu(HTMLParser):
    def __init__(self):
        super().__init__()
        self.linkler, self.baslik, self.aciklama, self.kanonik, self.noindex, self.h1 = [], "", "", "", False, 0
        self._baslikta = False

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "a" and a.get("href"):
            self.linkler.append(a["href"])
        elif tag == "title":
            self._baslikta = True
        elif tag == "meta" and a.get("name") == "description":
            self.aciklama = a.get("content") or ""
        elif tag == "meta" and a.get("name") == "robots" and "noindex" in (a.get("content") or ""):
            self.noindex = True
        elif tag == "link" and a.get("rel") == "canonical":
            self.kanonik = a.get("href") or ""
        elif tag == "h1":
            self.h1 += 1

    def handle_endtag(self, tag):
        if tag == "title":
            self._baslikta = False

    def handle_data(self, data):
        if self._baslikta:
            self.baslik += data


def _hedef_var(href: str) -> bool:
    yol = href.split("#")[0].split("?")[0]
    if not yol.startswith(ayar.TABAN + "/") and yol != ayar.TABAN + "/":
        return True  # dış bağlantı ya da çapa
    goreli = yol[len(ayar.TABAN):].lstrip("/")
    hedef = ayar.DIST / goreli
    return hedef.is_file() or (hedef / "index.html").is_file()


def kontrol() -> list[str]:
    hatalar = []
    basliklar = Counter()
    indeksli = 0
    for dosya in ayar.DIST.rglob("*.html"):
        goreli = dosya.relative_to(ayar.DIST).as_posix()
        html = dosya.read_text(encoding="utf-8")
        o = _Okuyucu()
        o.feed(html)
        if m := SIZINTI.search(html):
            hatalar.append(f"{goreli}: sızıntı {m.group(0)[:80]!r}")
        if not o.baslik.strip():
            hatalar.append(f"{goreli}: başlık yok")
        if goreli != "404.html":
            if not 50 <= len(o.aciklama) <= 320:
                hatalar.append(f"{goreli}: açıklama uzunluğu {len(o.aciklama)}")
            if o.h1 != 1:
                hatalar.append(f"{goreli}: {o.h1} adet h1")
            if not o.kanonik.startswith(ayar.SITE_URL):
                hatalar.append(f"{goreli}: kanonik {o.kanonik}")
        if not o.noindex and goreli != "404.html":
            indeksli += 1
            basliklar[o.baslik.strip()] += 1
        for href in o.linkler:
            if not _hedef_var(href):
                hatalar.append(f"{goreli}: kırık bağlantı {href}")
    hatalar += [f"yinelenen başlık ({n}): {b}" for b, n in basliklar.items() if n > 1]
    harita = (ayar.DIST / "sitemap.xml").read_text(encoding="utf-8")
    n_harita = harita.count("<loc>")
    if n_harita != indeksli:
        hatalar.append(f"site haritası {n_harita} URL, indekslenebilir sayfa {indeksli}")
    return hatalar
