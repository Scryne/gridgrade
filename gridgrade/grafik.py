"""Derleme anında SVG grafikler (JS yok). Her grafik <title>/<desc> taşır; sayfada ayrıca metin özeti ve tablo bulunur."""
from html import escape
from itertools import count

from . import ayar

_SAYAC = count(1)  # aynı sayfadaki grafiklerin <title> kimlikleri çakışmasın

RENK = {"paper": "#FAF8F3", "ink": "#17181C", "muted": "#5B616B", "line": "#E3DED3", "primary": "#1F4FD1",
        "cheaper": "#1F6FB2", "pricier": "#D2611C", "wire": "#F2B705"}


def _hex(h: str) -> tuple[int, int, int]:
    h = h.lstrip("#")
    return int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)


def karistir(a: str, b: str, t: float) -> str:
    ra, rb = _hex(a), _hex(b)
    return "#" + "".join(f"{round(x + (y - x) * t):02x}" for x, y in zip(ra, rb))


def ayrisan(deger: float, referans: float, aralik: float = 0.6) -> str:
    """Referansa göre ucuz → mavi, pahalı → turuncu; fark ±%60'ta doyar."""
    oran = max(-1.0, min(1.0, (deger - referans) / referans / aralik))
    hedef = RENK["pricier"] if oran > 0 else RENK["cheaper"]
    return karistir("#F4F1EA", hedef, abs(oran) ** 0.8 * 0.92)


def yazi_rengi(arka: str) -> str:
    r, g, b = _hex(arka)
    return RENK["ink"] if (0.299 * r + 0.587 * g + 0.114 * b) > 150 else "#FFFFFF"


def cizgi(seriler: list[dict], baslik: str, aciklama: str, birim: str = "¢", genislik: int = 720,
          yukseklik: int = 300) -> str:
    """seriler: [{"ad", "renk", "noktalar": [(yil_ondalik, deger), ...]}]"""
    sol, sag, ust, alt = 44, 70, 16, 30
    tum = [p for s in seriler for p in s["noktalar"] if p[1] is not None]
    x0, x1 = min(p[0] for p in tum), max(p[0] for p in tum)
    y_min, y_max = min(p[1] for p in tum), max(p[1] for p in tum)
    pay = (y_max - y_min) * 0.12 or 1
    y0, y1 = max(0, y_min - pay), y_max + pay

    def X(x):
        return sol + (x - x0) / ((x1 - x0) or 1) * (genislik - sol - sag)

    def Y(y):
        return ust + (1 - (y - y0) / ((y1 - y0) or 1)) * (yukseklik - ust - alt)

    n_ = next(_SAYAC)
    p = [(f'<svg viewBox="0 0 {genislik} {yukseklik}" role="img" aria-labelledby="ct{n_} cd{n_}" class="chart" '
         f'xmlns="http://www.w3.org/2000/svg"><title id="ct{n_}">{escape(baslik)}</title>'
         f'<desc id="cd{n_}">{escape(aciklama)}</desc>')]
    adim = _guzel_adim((y1 - y0) / 4)
    v = (y0 // adim + 1) * adim
    while v < y1:
        p.append(f'<line x1="{sol}" x2="{genislik - sag}" y1="{Y(v):.1f}" y2="{Y(v):.1f}" stroke="{RENK["line"]}"/>'
                 f'<text x="{sol - 8}" y="{Y(v) + 4:.1f}" text-anchor="end" class="ax">{v:g}{birim}</text>')
        v += adim
    yil_adim = 1 if x1 - x0 <= 6 else 2 if x1 - x0 <= 12 else 4
    for yil in range(int(x0) + (1 if x0 % 1 else 0), int(x1) + 1, 1):
        if (yil - int(x0)) % yil_adim:
            continue
        p.append(f'<text x="{X(yil):.1f}" y="{yukseklik - 8}" text-anchor="middle" class="ax">{yil}</text>')
    etiketler = []
    for s in seriler:
        n = [q for q in s["noktalar"] if q[1] is not None]
        yol = " ".join(f"{'M' if i == 0 else 'L'}{X(x):.1f},{Y(y):.1f}" for i, (x, y) in enumerate(n))
        p.append(f'<path d="{yol}" fill="none" stroke="{s["renk"]}" stroke-width="{s.get("kalinlik", 2.25)}" '
                 f'stroke-linejoin="round" stroke-linecap="round"/>')
        sx, sy = n[-1]
        p.append(f'<circle cx="{X(sx):.1f}" cy="{Y(sy):.1f}" r="3.5" fill="{s["renk"]}"/>')
        etiketler.append([Y(sy), sy, s])
    etiketler.sort(key=lambda e: e[0])
    for i in range(1, len(etiketler)):  # son değer etiketleri üst üste binmesin
        if etiketler[i][0] - etiketler[i - 1][0] < 16:
            etiketler[i][0] = etiketler[i - 1][0] + 16
    for y, deger, s in etiketler:
        p.append(f'<text x="{genislik - sag + 8}" y="{y + 4:.1f}" class="lbl" fill="{s["renk"]}">{deger:.1f}{birim} '
                 f'<tspan class="ax">{escape(s["ad"])}</tspan></text>')
    p.append("</svg>")
    return "".join(p)


def _guzel_adim(ham: float) -> float:
    for a in (0.5, 1, 2, 2.5, 5, 10, 20, 25, 50, 100):
        if ham <= a:
            return a
    return 100


def karo_harita(degerler: dict[str, float], referans: float, yollar: dict[str, str], baslik: str, aciklama: str) -> str:
    k, bosluk = 58, 5
    gen, yuk = 11 * (k + bosluk), 8 * (k + bosluk)
    n_ = next(_SAYAC)
    p = [(f'<svg viewBox="0 0 {gen} {yuk}" role="img" aria-labelledby="mt{n_} md{n_}" class="tilemap" '
         f'xmlns="http://www.w3.org/2000/svg"><title id="mt{n_}">{escape(baslik)}</title>'
         f'<desc id="md{n_}">{escape(aciklama)}</desc>')]
    for ey, (sx, sy) in ayar.KARO.items():
        d = degerler.get(ey)
        arka = ayrisan(d, referans) if d else "#E9E5DC"
        yazi = yazi_rengi(arka)
        x, y = sx * (k + bosluk), sy * (k + bosluk)
        ad = escape(ayar.EYALETLER[ey])
        p.append(f'<a href="{yollar[ey]}" aria-label="{ad}: {d:.1f} cents per kWh"><g class="tile">'
                 f'<rect x="{x}" y="{y}" width="{k}" height="{k}" rx="6" fill="{arka}"/>'
                 f'<text x="{x + k / 2}" y="{y + 24}" text-anchor="middle" class="tk" fill="{yazi}">{ey}</text>'
                 f'<text x="{x + k / 2}" y="{y + 42}" text-anchor="middle" class="tv" fill="{yazi}">{d:.1f}</text></g></a>')
    p.append("</svg>")
    return "".join(p)


def cubuklar(satirlar: list[tuple[str, float, str]], baslik: str, birim: str = "¢", vurgu: str | None = None) -> str:
    """Yatay çubuklar: (etiket, değer, renk). vurgu etiketi koyu yazılır."""
    sat, sol, gen = 26, 190, 720
    yuk = sat * len(satirlar) + 8
    en_buyuk = max(v for _, v, _ in satirlar) or 1
    p = [(f'<svg viewBox="0 0 {gen} {yuk}" role="img" aria-label="{escape(baslik)}" class="bars" '
         f'xmlns="http://www.w3.org/2000/svg">')]
    for i, (etiket, deger, renk) in enumerate(satirlar):
        y = i * sat + 4
        w = (gen - sol - 70) * deger / en_buyuk
        kalin = ' font-weight="700"' if etiket == vurgu else ""
        p.append(f'<text x="{sol - 8}" y="{y + 15}" text-anchor="end" class="bl"{kalin}>{escape(etiket[:28])}</text>'
                 f'<rect x="{sol}" y="{y + 3}" width="{w:.1f}" height="16" rx="3" fill="{renk}"/>'
                 f'<text x="{sol + w + 6:.1f}" y="{y + 15}" class="bv"{kalin}>{deger:.1f}{birim}</text>')
    p.append("</svg>")
    return "".join(p)
