"""gridgrade cek | isle | uret | kontrol | hepsi"""
import argparse
import sys

from . import ayar


def main(argv: list[str] | None = None) -> int:
    for akis in (sys.stdout, sys.stderr):
        if hasattr(akis, "reconfigure"):
            akis.reconfigure(encoding="utf-8", errors="replace")
    p = argparse.ArgumentParser(prog="gridgrade")
    p.add_argument("komut", choices=["cek", "isle", "uret", "kontrol", "hepsi"])
    a = p.parse_args(argv)

    if a.komut in ("cek", "hepsi"):
        from .cek import indir

        k = indir()
        print(f"indirildi: EIA-861 {k['eia861_yili']}, 861M {k['eia861m.xlsx']['son_degisme']}")
    if a.komut in ("isle", "hepsi"):
        from .isle import kaydet, model_kur

        m = model_kur()
        kaydet(m)
        print(f"model: {len(m['eyaletler'])} eyalet, {len(m['sirketler'])} şirket, {len(m['ilceler'])} ilçe, "
              f"son ay {m['abd']['ozet']['y']}-{m['abd']['ozet']['m']:02d}")
    if a.komut in ("uret", "hepsi"):
        from .uret import uret

        n = uret()
        print(f"üretildi: {n} sayfa → {ayar.DIST}")
    if a.komut in ("kontrol", "hepsi"):
        from .kontrol import kontrol

        hatalar = kontrol()
        for h in hatalar[:50]:
            print("HATA:", h)
        if hatalar:
            print(f"{len(hatalar)} hata")
            return 1
        print("kontrol temiz")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
