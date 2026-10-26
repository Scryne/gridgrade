---
proje: GridGrade
created: 2026-10-24
type: roadmap
status: aktif
---
# GridGrade — Roadmap

Durum sütunu session-start hook'u tarafından otomatik okunur — format bozulmasın:
⏳ Bekliyor / 🔄 Devam Ediyor / ✅ Tamamlandı / ⛔ Engelli.

| Faz | Adı | Durum | Bitti Kriteri |
| --- | --- | --- | --- |
| 0 | Araştırma ve veri doğrulaması | ✅ Tamamlandı | Niş seçildi (K-1), EIA dosyaları anahtarsız indirilip yapısı görüldü (`docs/arastirma/2026-10-24-nis.md`) |
| 1 | İskelet ve sağlık | ✅ Tamamlandı | uv projesi, CI (ruff + pytest + derleme) yeşil, dependabot, public repo + Pages |
| 2 | Veri hattı | ✅ Tamamlandı | `gridgrade cek` + `isle` gerçek EIA dosyalarından eyalet, şirket, ilçe modelini ve notları üretiyor; testler bilinen satırları doğruluyor |
| 3 | Site üretici ve tasarım | ✅ Tamamlandı | Tüm sayfa türleri üretiliyor, DESIGN.md'ye uygun, 4 genişlikte taşma yok, Lighthouse benzeri kontroller (başlık, açıklama, canonical, JSON-LD) geçiyor |
| 4 | Yayın ve otomasyon | ✅ Tamamlandı | Yayın öncesi kişisel veri taraması temiz; Pages'te canlı; günlük cron bir kez gerçek koştu |
| 5 | Alan adı + AdSense (Scryne) | ⏳ Bekliyor | Scryne alan adını aldı, CNAME bağlandı, Search Console'a site haritası verildi, AdSense başvurusu yapıldı |
| 6 | Gerçek kullanım | ⏳ Bekliyor | Search Console'da ilk gösterimler; AdSense onayı; 6. ayda trafik kararı |

## Faz Detayları

### Faz 1: İskelet ve sağlık
- **İşler:** pyproject (uv), `gridgrade/` paketi, ruff, pytest, `.github/workflows/ci.yml` + `yayin.yml`, dependabot (uv + actions).

### Faz 2: Veri hattı
- **İşler:** indirme + önbellek, xlsx sütunlarını başlıkla bulma, eyalet aylık seri, şirket yıllık metrikleri, güvenilirlik, ilçe eşleşmesi, not.

### Faz 3: Site üretici ve tasarım
- **İşler:** DESIGN.md, temel şablon, ana sayfa (eyalet karo haritası), eyalet, şirket, ilçe, sıralamalar, hesaplayıcı, yöntem,
  hakkında, gizlilik, 404, sitemap, robots, kademeli indeksleme.

### Durum (2026-10-24 gece)
- Faz 1–3 ✅: veri hattı (861M + 861 son yıl + 2 önceki yıl arşivden + EIA-923 üretim), not yöntemi, 4.490 sayfa, kontrol temiz, 21 test,
  axe 0 ihlal (9 sayfa türü), IndexNow çalışıyor (ilk ping 403 → ikincisi 345 URL kabul).
- Eklenenler: şirket fiyat geçmişi, zam sıralaması, akıllı sayaç/dinamik tarife/net metering, eyalet üretim kaynakları.
- Faz 4 ✅ (2026-10-26 doğrulandı): zamanlanmış koşular 10-24 17:27 ve 10-25 17:39 UTC'de başarılı (GitHub zamanlanmış
  işleri ~3 sa geciktiriyor); veri değişmediği için ikisi de "değişiklik yok" deyip site reposuna commit atmadı, doğru davranış.
  Faz 5 rehberi: `docs/alan-adi-ve-reklam.md`.
- Yayın: gizli `Scryne/gridgrade` (kaynak) + herkese açık `Scryne/gridgrade-site` (yalnız HTML, Pages), dağıtım anahtarı sırrı.
  Canlı: https://scryne.github.io/gridgrade-site/ (yayın öncesi tarama 0 bulgu).
- Öğrenilen: Part A satırları BA kodu başına bölünüyor (toplanmalı); EIA eski yılları `archive/zip/` altına taşıyor; Google
  "scaled content" riskine karşı ilk katman 344 sayfa.
