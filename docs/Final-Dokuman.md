---
proje: GridGrade
created: 2026-10-24
type: final-dokuman
status: aktif
---
# GridGrade — Final Doküman

## Özet
EIA'nın anahtarsız kamu dosyalarından her gün kendini güncelleyen İngilizce statik site: ABD eyaletleri, ~2.800 elektrik şirketi
(utility × eyalet) ve ~3.100 ilçe için elektrik fiyatı, ortalama fatura, tüketim ve kesinti güvenilirliği; şirketlere şeffaf
yöntemle A–F not. GitHub Pages'te yayında, GitHub Actions ile günlük güncelleme, reklam alanları AdSense onayına hazır.

## Kararlar

| # | Karar | Gerekçe |
| --- | --- | --- |
| K-1 | Niş: ABD elektrik fiyatı + şirket karnesi, İngilizce | Global araştırmada 1 numara; ABD RPM'i TR'nin katları; veri kamu malı; rakipler küçük/orta (2026-10-24) |
| K-2 | Veri: EIA-861 (yıllık, şirket), EIA-861M sales_revenue (aylık, eyalet), anahtarsız indirme | API anahtarı kayıt ister (hesap açılmaz); dosyalar yeterli ve kararlı |
| K-3 | Üretici: Python + Jinja2, statik HTML, grafikler derleme anında SVG | Tek dil (veri hattı Python), framework sürüklenmesi yok, JS'siz hızlı sayfa |
| K-4 | Barındırma: public repo `Scryne/gridgrade` + GitHub Pages + Actions cron (günlük) | Bedava, sınırsız Actions; alan adı gelince CNAME |
| K-5 | Not yöntemi (aşağıda) yayınlanır, değişirse sürümlenir | Güven (E-E-A-T) ve "değer katmayan seri içerik" riskine karşı özgün hesap |
| K-6 | Kademeli indeksleme: ilk katman ~500 sayfa sitemap + index; diğerleri `noindex` ile üretilir, tarih eşiğiyle açılır | Araştırma önerisi; yeni alan adında tarama bütçesi sınırlı |
| K-7 | Kişisel veri yok: commit kimliği GitHub noreply, sayfada ad/e-posta yok; iletişim yalnız GitHub üzerinden | Kurallar (herkese açık yüzey anonim) |
| K-8 | Reklam alanları sabit yükseklikli rezerv kutu; AdSense kodu onaydan sonra tek ayarla açılır | CLS olmadan, onaysız reklam kodu yok |
| K-9 | Tasarım: açık tema, "karne" kimliği (DESIGN.md) — global koyu glassmorphism ezilir | Veri/başvuru sitesi okunabilirliği, reklam uyumu |

## Not yöntemi (v1)
- **Fiyat puanı:** şirketin konut ortalama fiyatı (konut geliri ÷ konut satışı, ¢/kWh) tüm ABD şirketleri arasında yüzdelik dilim;
  ucuz olan yüksek puan. Yalnız ≥ 100 konut abonesi olan, EIA'nın gözlenmiş (O) verisi olan satırlar sıralanır.
- **Güvenilirlik puanı:** SAIDI, büyük olay günleri hariç (IEEE 1366, dakika/yıl) yüzdelik dilim; az kesinti yüksek puan.
- **Genel not:** güvenilirlik varsa %60 fiyat + %40 güvenilirlik, yoksa yalnız fiyat ("price-only" etiketiyle).
- **Harf:** puan ≥ 80 → A, 60–80 → B, 40–60 → C, 20–40 → D, < 20 → F.
- Ortalama aylık fatura = konut geliri ÷ abone ÷ 12; ortalama tüketim = konut satışı (kWh) ÷ abone ÷ 12. İklim ve ev büyüklüğünü
  yansıtmaz, sayfada söylenir.

## Teknoloji Stack

| Katman | Seçim | Gerekçe |
| --- | --- | --- |
| Veri çekme/işleme | Python 3.12, uv, httpx, openpyxl | EIA dosyaları xlsx |
| Şablon | Jinja2 | Basit, hızlı |
| Grafik | Kendi SVG üreticimiz | JS'siz, erişilebilir, küçük |
| Barındırma | GitHub Pages (actions/deploy-pages) | Bedava |
| Zamanlama | GitHub Actions cron (günlük 14:00 UTC) + elle tetikleme | EIA aylık yayınları ~24'ünde |
| Test | pytest, ruff; derleme çıktısı kontrolü (bağlantı, sitemap, başlık benzersizliği) | Ürün doğrulama |

## Mimari
```
Actions (cron) → gridgrade.cek (indir, önbellek, değişim karşılaştırma) → gridgrade.isle (normalize, not hesap)
  → data/*.json → gridgrade.uret (Jinja2 + SVG) → dist/ (HTML, sitemap.xml, robots.txt, 404) → Pages
```

## Kapsam (v1)
Bkz. Proje-Fikri. Bitti: herkese açık adreste yayında + günlük güncelleme çalışıyor + site haritası hazır.

## Riskler ve Doğrulamalar
- Google "scaled content abuse": her sayfada hesaplanmış özgün değer (not, kıyas, sıralama, trend), kademeli indeksleme.
- EIA dosya biçimi değişirse işleyici kırılır: işleyici sütunları başlık metniyle bulur, beklenmeyen biçimde derleme başarısız
  olur ve canlı site eski hâliyle kalır (Actions hata verir).
- 2024 şirket verisi bir yıl geride: sayfada veri yılı açıkça yazılır; hat yeni yılı (f861{yıl}.zip) kendisi arar.
- AdSense onayı garanti değil; github.io kabul edilmez → alan adı şart (Scryne).

## Kapsam Dışı
Bkz. Proje-Fikri.
