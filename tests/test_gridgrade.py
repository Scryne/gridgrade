import datetime as dt

import pytest

from gridgrade import ayar, isle, kontrol, notlar, uret


@pytest.mark.parametrize("ham,temiz", [
    ("Borough of Chambersburg - (PA)", "Borough of Chambersburg"),
    ("Central Electric Coop, Inc - (PA)", "Central Electric Coop, Inc"),
    ("Tri-County Rural Elec Coop Inc (PA)", "Tri-County Rural Elec Coop Inc"),
    ("PECO Energy Co", "PECO Energy Co"),
    ("City of  Aberdeen - (MS)", "City of Aberdeen"),
])
def test_temiz_ad(ham, temiz):
    assert isle.temiz_ad(ham) == temiz


def test_fiyat_bin_dolar_ve_mwh_den_sent():
    assert isle.fiyat(1000, 10000) == 10.0  # 1 M$ / 10 GWh = 10 ¢/kWh
    assert isle.fiyat(None, 5) is None and isle.fiyat(5, 0) is None


def test_slug():
    assert isle.slug("Pacific Gas & Electric Co.") == "pacific-gas-and-electric-co"
    assert isle.slug("Doña Ana") == "dona-ana"


@pytest.mark.parametrize("puan,harf", [(100, "A"), (80, "A"), (79.9, "B"), (60, "B"), (40, "C"), (20, "D"), (19.9, "F"), (0, "F")])
def test_harf_esikleri(puan, harf):
    assert notlar.harf(puan) == harf


def _sirket(fiyat, saidi=None, abone=5000, tahmini=False):
    return {"fiyat": fiyat, "abone": abone, "tahmini": tahmini, "guv": {"saidi": saidi} if saidi is not None else None}


def test_notlar_yuzdelik_agirlik_ve_dislamalar():
    s = {"ucuz": _sirket(10, 50), "orta": _sirket(15, 100), "pahali": _sirket(20, 200), "fiyatsiz_guv": _sirket(15),
         "kucuk": _sirket(5, 10, abone=50), "tahmini": _sirket(5, 10, tahmini=True)}
    notlar.hesapla(s)
    assert s["ucuz"]["not"]["harf"] == "A" and s["ucuz"]["not"]["puan"] == 100
    assert s["pahali"]["not"]["harf"] == "F" and s["pahali"]["not"]["puan"] == 0
    assert s["orta"]["not"]["puan"] == 50  # 0.6*50 + 0.4*50
    assert s["fiyatsiz_guv"]["not"]["yalniz_fiyat"] and s["fiyatsiz_guv"]["not"]["puan"] == 50
    assert s["kucuk"]["not"] is None and s["tahmini"]["not"] is None  # en ucuz olsalar da sıralamayı bozmazlar


def test_kademeli_indeksleme_takvimi():
    g = ayar.YAYIN_GUNU
    assert uret.katman(g) == (50_000, False)
    assert uret.katman(g + dt.timedelta(days=21)) == (10_000, False)
    assert uret.katman(g + dt.timedelta(days=42)) == (2_000, True)
    assert uret.katman(g + dt.timedelta(days=400)) == (100, True)


def test_karsilastir_metni():
    assert uret.karsilastir(9, 10) == "10% below"
    assert uret.karsilastir(12, 10) == "20% above"
    assert uret.karsilastir(10.1, 10) == "in line with"
    assert uret.karsilastir(None, 10) == "not comparable to"


def test_ilce_adi():
    assert uret.ilce_adi("Orleans", "LA") == "Orleans Parish"
    assert uret.ilce_adi("Bucks", "PA") == "Bucks County"
    assert uret.ilce_adi("Richmond City", "VA") == "Richmond City"


def _sayfa(baslik, href, govde="ok"):
    return (f'<html><head><title>{baslik}</title><meta name="description" content="{"x" * 80}">'
            f'<link rel="canonical" href="{ayar.SITE_URL}/a/"></head><body><h1>H</h1><a href="{href}">l</a><p>{govde}</p></body></html>')


def test_kontrol_kirik_baglanti_sizinti_ve_yinelenen_baslik(tmp_path, monkeypatch):
    monkeypatch.setattr(ayar, "DIST", tmp_path)
    monkeypatch.setattr(ayar, "TABAN", "/gridgrade")
    (tmp_path / "a").mkdir()
    (tmp_path / "a" / "index.html").write_text(_sayfa("A", "/gridgrade/a/"), encoding="utf-8")
    (tmp_path / "b").mkdir()
    (tmp_path / "b" / "index.html").write_text(_sayfa("A", "/gridgrade/yok/", "price None"), encoding="utf-8")
    (tmp_path / "sitemap.xml").write_text("<loc>x</loc><loc>y</loc>", encoding="utf-8")
    hatalar = kontrol.kontrol()
    assert any("kırık bağlantı /gridgrade/yok/" in h for h in hatalar)
    assert any("sızıntı" in h for h in hatalar)
    assert any("yinelenen başlık" in h for h in hatalar)
    (tmp_path / "b" / "index.html").write_text(_sayfa("B", "/gridgrade/a/"), encoding="utf-8")
    assert kontrol.kontrol() == []


@pytest.mark.skipif(not (ayar.HAM / "eia861.zip").exists(), reason="EIA dosyaları indirilmemiş (gridgrade cek)")
def test_gercek_veri_model_akli_basinda():
    m = isle.model_kur()
    assert len(m["eyaletler"]) == 51 and len(m["sirketler"]) > 1000 and len(m["ilceler"]) > 2500
    abd = m["abd"]["ozet"]["fiyat"]["res"]
    assert 8 < abd < 40
    for s in m["sirketler"].values():
        assert s["fiyat"] is None or 2 < s["fiyat"] < 120, s
        assert "(" not in s["ad"][-4:], s["ad"]
    peco = next(s for s in m["sirketler"].values() if s["ad"] == "PECO Energy Co")
    assert peco["abone"] > 1_000_000 and peco["ey"] == "PA"
    harfler = [s["not"]["harf"] for s in m["sirketler"].values() if s["not"]]
    assert set(harfler) == {"A", "B", "C", "D", "F"}
