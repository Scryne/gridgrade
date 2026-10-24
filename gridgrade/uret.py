"""Modelden statik siteyi üretir: sayfalar, sitemap.xml, robots.txt, arama dizini, statik dosyalar."""
import calendar
import datetime as dt
import json
import shutil
import statistics
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, StrictUndefined, select_autoescape

from . import ayar, grafik, notlar

SABLONLAR = ayar.KOK / "templates"
STATIK = ayar.KOK / "static"


# ---- Biçimlendirme ----

def sent(x) -> str:
    return "—" if x is None else f"{x:.2f}¢"


def dolar(x, ondalik: int = 0) -> str:
    return "—" if x is None else f"${x:,.{ondalik}f}"


def sayi(x) -> str:
    return "—" if x is None else f"{x:,.0f}"


def yuzde(x, isaret: bool = True) -> str:
    if x is None:
        return "—"
    return f"{x:+.1f}%" if isaret else f"{abs(x):.1f}%"


def ay_adi(m: int) -> str:
    return calendar.month_name[m]


def ilce_adi(ad: str, ey: str) -> str:
    if ey == "LA":
        return f"{ad} Parish"
    if ey == "AK" or ad.lower().endswith((" city", " borough", " census area", " municipality")):
        return ad
    return f"{ad} County"


def fark(a, b) -> float | None:
    return None if a is None or not b else round((a - b) / b * 100, 1)


def karsilastir(a, b, birim: str = "") -> str:
    """'14% below' / '9% above' / 'in line with'"""
    f = fark(a, b)
    if f is None:
        return "not comparable to"
    if abs(f) < 2:
        return "in line with"
    return f"{abs(f):.0f}% {'below' if f < 0 else 'above'}"


# ---- Kademeli indeksleme (K-6) ----

def katman(bugun: dt.date) -> tuple[int, bool]:
    gun = (bugun - ayar.YAYIN_GUNU).days
    secili = ayar.KATMANLAR[0]
    for k in ayar.KATMANLAR:
        if gun >= k[0]:
            secili = k
    return secili[1], secili[2]


class Uretici:
    def __init__(self, model: dict, bugun: dt.date | None = None):
        self.m = model
        self.bugun = bugun or dt.date.today()
        self.asgari_abone, self.ilceler_acik = katman(self.bugun)
        self.sayfalar: list[tuple[str, bool]] = []  # (yol, indekslenebilir)
        self.env = Environment(loader=FileSystemLoader(SABLONLAR), autoescape=select_autoescape(["html", "xml"]),
                               undefined=StrictUndefined, trim_blocks=True, lstrip_blocks=True)
        self.env.filters.update(sent=sent, dolar=dolar, sayi=sayi, yuzde=yuzde, ay_adi=ay_adi)
        self.env.globals.update(url=self.url, mutlak=self.mutlak, ayar=ayar, karsilastir=karsilastir, fark=fark,
                                ilce_adi=ilce_adi, model=model, notlar=notlar, simdi=self.bugun)
        abd = model["abd"]["ozet"]
        self.veri_donemi = f"{ay_adi(abd['m'])} {abd['y']}"
        self.sirket_yili = model["sirket_yili"]
        s = model["sirketler"]
        saidi = [x["guv"]["saidi"] for x in s.values() if x.get("guv") and x["guv"].get("saidi")]
        self.saidi_medyan = round(statistics.median(saidi), 1) if saidi else None
        self.env.globals.update(veri_donemi=self.veri_donemi, sirket_yili=self.sirket_yili, saidi_medyan=self.saidi_medyan)

    # yollar
    def url(self, yol: str = "") -> str:
        yol = yol.strip("/")
        return f"{ayar.TABAN}/{yol}/" if yol else f"{ayar.TABAN}/"

    def mutlak(self, yol: str = "") -> str:
        yol = yol.strip("/")
        return f"{ayar.SITE_URL}/{yol}/" if yol else f"{ayar.SITE_URL}/"

    def sirket_indekslenir(self, s: dict) -> bool:
        return s["abone"] >= self.asgari_abone and not s["tahmini"]

    def yaz(self, yol: str, sablon: str, indeks: bool = True, **baglam) -> None:
        hedef = ayar.DIST / yol / "index.html" if yol else ayar.DIST / "index.html"
        hedef.parent.mkdir(parents=True, exist_ok=True)
        html = self.env.get_template(sablon).render(yol=yol, indeks=indeks, kanonik=self.mutlak(yol), **baglam)
        hedef.write_text(html, encoding="utf-8")
        self.sayfalar.append((yol, indeks))

    # ---- sayfalar ----
    def ana_sayfa(self):
        e = self.m["eyaletler"]
        abd = self.m["abd"]["ozet"]
        harita = grafik.karo_harita({k: v["ozet"]["fiyat"]["res"] for k, v in e.items()}, abd["fiyat"]["res"],
                                    {k: self.url(v["yol"]) for k, v in e.items()},
                                    f"Residential electricity price by state, {self.veri_donemi}",
                                    "Each square is a state; blue is cheaper and orange is pricier than the US average.")
        sirali = sorted(e.values(), key=lambda x: x["ozet"]["fiyat"]["res"])
        self.yaz("", "index.html", harita=harita, ucuz=sirali[:5], pahali=sirali[::-1][:5],
                 grafik=self._abd_grafik(), abd=abd)

    def _seri_noktalari(self, seri: list, sutun: int = 2, yil_sayisi: int = 10) -> list[tuple[float, float]]:
        son_yil = seri[-1][0]
        return [(y + (m - 1) / 12, r[sutun]) for r in seri for y, m in [(r[0], r[1])] if y > son_yil - yil_sayisi]

    def _abd_grafik(self) -> str:
        abd = self.m["abd"]["seri"]
        return grafik.cizgi([{"ad": "US", "renk": grafik.RENK["ink"], "noktalar": self._seri_noktalari(abd)}],
                            "US average residential electricity price, monthly",
                            "Monthly average residential price in cents per kilowatt-hour over the last ten years.")

    def eyaletler(self):
        e = self.m["eyaletler"]
        s = self.m["sirketler"]
        abd_seri = self.m["abd"]["seri"]
        for ey, d in e.items():
            sirketler = [s[a] for a in d["sirketler"]]
            ilceler = sorted((i for i in self.m["ilceler"].values() if i["ey"] == ey), key=lambda i: i["ad"])
            g = grafik.cizgi([
                {"ad": "US", "renk": grafik.RENK["muted"], "kalinlik": 1.75, "noktalar": self._seri_noktalari(abd_seri)},
                {"ad": ey, "renk": grafik.RENK["primary"], "noktalar": self._seri_noktalari(d["seri"])},
            ], f"Residential electricity price in {d['ad']} vs US, monthly",
                f"Monthly average residential price in {d['ad']} and the US over the last ten years, in cents per kWh.")
            yillik = sorted(((int(y), v) for y, v in d["yillik"].items()), reverse=True)
            self.yaz(d["yol"], "state.html", e=d, sirketler=sirketler, ilceler=ilceler, grafik=g, yillik=yillik,
                     abd=self.m["abd"], ilceler_acik=self.ilceler_acik)

    def sirketler(self):
        s = self.m["sirketler"]
        e = self.m["eyaletler"]
        for d in s.values():
            ey = e[d["ey"]]
            eyalet_yil = ey["yillik"].get(str(d["yil"])) or {}
            abd_yil = self.m["abd"]["yillik"].get(str(d["yil"])) or {}
            komsular = [s[a] for a in ey["sirketler"] if a != d["anahtar"]]
            fiyatli = sorted((x for x in [d, *komsular] if x["fiyat"]), key=lambda x: x["fiyat"])
            sira = next(i for i, x in enumerate(fiyatli, 1) if x["anahtar"] == d["anahtar"])
            eyalet_saidi = [x["guv"]["saidi"] for x in [d, *komsular] if x.get("guv") and x["guv"].get("saidi")]
            ilce_yollari = [(ad, f"counties/{d['ey'].lower()}/{_slug(ad)}") for ad in d["ilceler"]]
            self.yaz(d["yol"], "utility.html", indeks=self.sirket_indekslenir(d), s=d, ey=ey, eyalet_yil=eyalet_yil,
                     abd_yil=abd_yil, komsular=komsular[:12], sira=sira, sira_n=len(fiyatli),
                     eyalet_saidi=round(statistics.median(eyalet_saidi), 1) if eyalet_saidi else None,
                     ilce_yollari=ilce_yollari, ilceler_acik=self.ilceler_acik)

    def ilceler(self):
        s = self.m["sirketler"]
        e = self.m["eyaletler"]
        for d in self.m["ilceler"].values():
            sirketler = [s[a] for a in d["sirketler"]]
            fiyatli = [x for x in sirketler if x["fiyat"]]
            self.yaz(d["yol"], "county.html", indeks=self.ilceler_acik and bool(fiyatli), il=d, sirketler=sirketler,
                     ucuz=min(fiyatli, key=lambda x: x["fiyat"]) if fiyatli else None, ey=e[d["ey"]])

    def siralamalar(self):
        e = sorted(self.m["eyaletler"].values(), key=lambda x: x["ozet"]["fiyat"]["res"])
        abd = self.m["abd"]["ozet"]
        cubuk = grafik.cubuklar([(x["ad"], x["ozet"]["fiyat"]["res"],
                                  grafik.ayrisan(x["ozet"]["fiyat"]["res"], abd["fiyat"]["res"])) for x in e],
                                f"Residential electricity price by state, {self.veri_donemi}")
        self.yaz("rankings/states", "rank_states.html", eyaletler=e, cubuk=cubuk, abd=abd)
        s = [x for x in self.m["sirketler"].values() if x["not"] and x["abone"] >= 1000]
        guv = [x for x in s if x.get("guv") and x["guv"].get("saidi")]
        degisen = [x for x in s if x["degisim"] is not None and x["abone"] >= 50_000]
        self.yaz("rankings/price-increases", "rank_changes.html",
                 artan=sorted(degisen, key=lambda x: -x["degisim"])[:40],
                 azalan=sorted(degisen, key=lambda x: x["degisim"])[:20],
                 eyaletler=sorted(self.m["eyaletler"].values(), key=lambda x: -(x["ozet"]["yillik_degisim"] or -99)),
                 n=len(degisen), artan_n=sum(1 for x in degisen if x["degisim"] > 0))
        self.yaz("rankings/utilities", "rank_utilities.html",
                 ucuz=sorted(s, key=lambda x: x["fiyat"])[:50], pahali=sorted(s, key=lambda x: -x["fiyat"])[:50],
                 guvenilir=sorted(guv, key=lambda x: x["guv"]["saidi"])[:50],
                 kesintili=sorted(guv, key=lambda x: -x["guv"]["saidi"])[:50],
                 buyuk=sorted(s, key=lambda x: -x["abone"])[:50], toplam=len(s))

    def diger(self):
        e = self.m["eyaletler"]
        s = self.m["sirketler"]
        self.yaz("utilities", "utilities_index.html",
                 gruplar=[(v, sorted((s[a] for a in v["sirketler"]), key=lambda x: x["ad"])) for v in
                          sorted(e.values(), key=lambda v: v["ad"])])
        hesap = {k: {"ad": v["ad"], "fiyat": v["ozet"]["fiyat"]["res"], "tuketim": v["ozet"]["tuketim"]}
                 for k, v in e.items()}
        self.yaz("electricity-bill-calculator", "calculator.html", hesap=json.dumps(hesap, separators=(",", ":")),
                 abd=self.m["abd"]["ozet"])
        self.yaz("methodology", "methodology.html")
        self.yaz("about", "about.html")
        self.yaz("privacy", "privacy.html")
        (ayar.DIST / "404.html").write_text(self.env.get_template("404.html").render(
            yol="404", indeks=False, kanonik=self.mutlak("")), encoding="utf-8")

    def ekler(self):
        donem = dt.date(self.m["abd"]["ozet"]["y"], self.m["abd"]["ozet"]["m"], 1).isoformat()
        satirlar = ['<?xml version="1.0" encoding="UTF-8"?>',
                    '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
        for yol, indeks in sorted(self.sayfalar):
            if indeks:
                satirlar.append(f"<url><loc>{self.mutlak(yol)}</loc><lastmod>{donem}</lastmod></url>")
        satirlar.append("</urlset>")
        (ayar.DIST / "sitemap.xml").write_text("\n".join(satirlar), encoding="utf-8")
        (ayar.DIST / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {ayar.SITE_URL}/sitemap.xml\n",
                                              encoding="utf-8")
        if ayar.ADSENSE_ISTEMCI:
            pub = ayar.ADSENSE_ISTEMCI.replace("ca-", "")
            (ayar.DIST / "ads.txt").write_text(f"google.com, {pub}, DIRECT, f08c47fec0942fa0\n", encoding="utf-8")
        e, s = self.m["eyaletler"], self.m["sirketler"]
        dizin = [[v["ad"], "State", self.url(v["yol"])] for v in e.values()]
        dizin += [[x["ad"], e[x["ey"]]["ad"], self.url(x["yol"])] for x in s.values()]
        dizin += [[ilce_adi(i["ad"], i["ey"]), e[i["ey"]]["ad"], self.url(i["yol"])] for i in self.m["ilceler"].values()]
        (ayar.DIST / "search.json").write_text(json.dumps(dizin, separators=(",", ":")), encoding="utf-8")
        hedef = ayar.DIST / "static"
        shutil.copytree(STATIK, hedef, dirs_exist_ok=True)
        if not ayar.TABAN:  # kendi alan adında Pages için CNAME
            (ayar.DIST / "CNAME").write_text(ayar.SITE_URL.split("://", 1)[1] + "\n", encoding="utf-8")

    def hepsi(self) -> int:
        ayar.DIST.mkdir(parents=True, exist_ok=True)
        for eski in ayar.DIST.iterdir():  # klasörün kendisi değil içeriği: açık bir sunucu klasörü kilitleyebilir
            shutil.rmtree(eski) if eski.is_dir() else eski.unlink()
        (ayar.DIST / ".nojekyll").write_text("", encoding="utf-8")
        self.ana_sayfa()
        self.eyaletler()
        self.sirketler()
        self.ilceler()
        self.siralamalar()
        self.diger()
        self.ekler()
        return len(self.sayfalar)


def _slug(metin: str) -> str:
    from .isle import slug

    return slug(metin)


def uret(model_yolu: Path = ayar.MODEL, bugun: dt.date | None = None) -> int:
    model = json.loads(model_yolu.read_text(encoding="utf-8"))
    return Uretici(model, bugun).hepsi()
