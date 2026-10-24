"""Sabitler: site kimliği, kaynak adresleri, eyaletler, karo harita yerleşimi, kademeli indeksleme takvimi."""
import datetime as dt
import os
from pathlib import Path
from urllib.parse import urlparse

KOK = Path(__file__).resolve().parent.parent
HAM = KOK / "veri" / "ham"
MODEL = KOK / "veri" / "model.json"
KAYNAK_KAYDI = KOK / "veri" / "kaynaklar.json"  # dosyaların son değişme tarihleri (repoda)
DIST = KOK / "dist"

SITE_ADI = "GridGrade"
SITE_URL = os.environ.get("GRIDGRADE_URL", "https://scryne.github.io/gridgrade-site").rstrip("/")
TABAN = urlparse(SITE_URL).path.rstrip("/")  # "/gridgrade" ya da alan adında ""
ADSENSE_ISTEMCI = os.environ.get("GRIDGRADE_ADSENSE", "")  # onaydan sonra "ca-pub-…"; boşsa reklam kodu basılmaz

EIA_861M = "https://www.eia.gov/electricity/data/eia861m/xls/sales_revenue.xlsx"
EIA_861_ZIP = "https://www.eia.gov/electricity/data/eia861/zip/f861{yil}.zip"
EIA_861_ARSIV = "https://www.eia.gov/electricity/data/eia861/archive/zip/f861{yil}.zip"  # EIA eski yılları taşıyor
EIA_URETIM = "https://www.eia.gov/electricity/data/state/annual_generation_state.xlsx"  # EIA-923 eyalet üretimi, yıllık
GECMIS_YIL = 2  # şirket sayfalarında son yılla birlikte gösterilen önceki yıl sayısı
EIA_861_SAYFA = "https://www.eia.gov/electricity/data/eia861/"

# IndexNow (Bing/Yandex anlık bildirim): anahtar gizli değildir, sitede dosya olarak yayınlanır
INDEXNOW_ANAHTARI = "71e6bfc5672350bb7bd6521bb83cc73c"
INDEXNOW_UCU = "https://api.indexnow.org/indexnow"

# Kademeli indeksleme (K-6): yayın gününden itibaren katmanlar açılır.
YAYIN_GUNU = dt.date(2026, 10, 24)
KATMANLAR = [  # (gün, şirket için asgari konut abonesi, ilçeler açık mı)
    (0, 50_000, False),
    (21, 10_000, False),
    (42, 2_000, True),
    (70, 100, True),
]

EYALETLER = {
    "AL": "Alabama", "AK": "Alaska", "AZ": "Arizona", "AR": "Arkansas", "CA": "California", "CO": "Colorado",
    "CT": "Connecticut", "DE": "Delaware", "DC": "District of Columbia", "FL": "Florida", "GA": "Georgia", "HI": "Hawaii",
    "ID": "Idaho", "IL": "Illinois", "IN": "Indiana", "IA": "Iowa", "KS": "Kansas", "KY": "Kentucky", "LA": "Louisiana",
    "ME": "Maine", "MD": "Maryland", "MA": "Massachusetts", "MI": "Michigan", "MN": "Minnesota", "MS": "Mississippi",
    "MO": "Missouri", "MT": "Montana", "NE": "Nebraska", "NV": "Nevada", "NH": "New Hampshire", "NJ": "New Jersey",
    "NM": "New Mexico", "NY": "New York", "NC": "North Carolina", "ND": "North Dakota", "OH": "Ohio", "OK": "Oklahoma",
    "OR": "Oregon", "PA": "Pennsylvania", "RI": "Rhode Island", "SC": "South Carolina", "SD": "South Dakota",
    "TN": "Tennessee", "TX": "Texas", "UT": "Utah", "VT": "Vermont", "VA": "Virginia", "WA": "Washington",
    "WV": "West Virginia", "WI": "Wisconsin", "WY": "Wyoming",
}

# NPR tarzı karo harita (sütun, satır)
KARO = {
    "AK": (0, 0), "ME": (10, 0), "VT": (9, 1), "NH": (10, 1),
    "WA": (0, 2), "ID": (1, 2), "MT": (2, 2), "ND": (3, 2), "MN": (4, 2), "IL": (5, 2), "WI": (6, 2), "MI": (7, 2),
    "NY": (8, 2), "RI": (9, 2), "MA": (10, 2),
    "OR": (0, 3), "NV": (1, 3), "WY": (2, 3), "SD": (3, 3), "IA": (4, 3), "IN": (5, 3), "OH": (6, 3), "PA": (7, 3),
    "NJ": (8, 3), "CT": (9, 3),
    "CA": (0, 4), "UT": (1, 4), "CO": (2, 4), "NE": (3, 4), "MO": (4, 4), "KY": (5, 4), "WV": (6, 4), "VA": (7, 4),
    "MD": (8, 4), "DE": (9, 4),
    "AZ": (1, 5), "NM": (2, 5), "KS": (3, 5), "AR": (4, 5), "TN": (5, 5), "NC": (6, 5), "SC": (7, 5), "DC": (8, 5),
    "OK": (3, 6), "LA": (4, 6), "MS": (5, 6), "AL": (6, 6), "GA": (7, 6),
    "HI": (0, 7), "TX": (3, 7), "FL": (8, 7),
}
