"""A–F not (Final-Doküman, not yöntemi v1). Yöntem değişirse YONTEM_SURUMU artar ve yöntem sayfası güncellenir."""

YONTEM_SURUMU = "1.0"
ASGARI_ABONE = 100
AGIRLIK_FIYAT, AGIRLIK_GUV = 0.6, 0.4
ESIKLER = [(80, "A"), (60, "B"), (40, "C"), (20, "D"), (0, "F")]


def harf(puan: float) -> str:
    return next(h for esik, h in ESIKLER if puan >= esik)


def _yuzdelik(degerler: dict[str, float]) -> dict[str, float]:
    """Küçük değer iyi: en düşük 100, en yüksek 0. Eşit değerler aynı puanı alır."""
    sirali = sorted(set(degerler.values()))
    n = len(sirali)
    if n == 1:
        return {k: 100.0 for k in degerler}
    yer = {v: i for i, v in enumerate(sirali)}
    return {k: round(100 * (1 - yer[v] / (n - 1)), 1) for k, v in degerler.items()}


def hesapla(sirketler: dict) -> None:
    uygun = {k: s for k, s in sirketler.items() if not s["tahmini"] and s["abone"] >= ASGARI_ABONE and s["fiyat"]}
    fiyat_puani = _yuzdelik({k: s["fiyat"] for k, s in uygun.items()})
    guv_puani = _yuzdelik({k: s["guv"]["saidi"] for k, s in uygun.items() if s.get("guv") and s["guv"].get("saidi")})
    for k, s in sirketler.items():
        if k not in uygun:
            s["not"] = None
            continue
        fp, gp = fiyat_puani[k], guv_puani.get(k)
        puan = round(AGIRLIK_FIYAT * fp + AGIRLIK_GUV * gp, 1) if gp is not None else fp
        s["not"] = {"harf": harf(puan), "puan": puan, "fiyat_puani": fp, "fiyat_harf": harf(fp),
                    "guv_puani": gp, "guv_harf": harf(gp) if gp is not None else None, "yalniz_fiyat": gp is None}
