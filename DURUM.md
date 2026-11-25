# DURUM — GridGrade — ABD elektrik fiyatı ve şirket karnesi

> **Ne bu dosya:** sertifika değil **envanter**. Ölçülen gerçek durum. Faz durumu `docs/Roadmap.md`'de.

**Ölçüm tarihi:** 2026-11-25
**Tek cümle:** EIA'nın anahtarsız kamu dosyalarından her gün kendini güncelleyen statik site (51 eyalet, 1.328 şirket,
3.102 ilçe, A–F not); canlı https://scryne.github.io/gridgrade-site/. Kod ve hat bitti; gelir için alan adı ve AdSense
Scryne'da.

**Yayına hazır karnesi (2026-11-25):** Kod ✅ · Ürün ✅ · Ön yüz ✅ (vitrin: siniyor) · Belge ✅ · Kapı ✅ · Dış adımlar
listeli. Bitiş çizgisi ScryneOS `🎯 100-Command-Center/Yayina-Hazir-Karnesi.md`'de; sonradan bulunan şey aşağıdaki
"v2 fikirleri"ne girer.

## Ne çalışıyor (2026-11-25'te ölçüldü)

- **Kod:** pytest 21/21, ruff temiz; Dependabot #5 (ruff) yerel merge. CI ve Publish yeşil.
- **Ürün:** `gridgrade hepsi` yerelde gerçek veriyle 23 sn: EIA-861 2025 + 861M (24 Kasım 2026 güncellemesi), son ay
  2026-09, 4.490 sayfa, `kontrol` temiz. Zamanlanmış Publish her gün koşuyor (son 5 koşu başarılı); kaynak değişince
  `veri/kaynaklar.json`'u kendisi commit'liyor (11-24 güncellemesini aldı).
- **Canlı site:** 8 rota (ana sayfa, eyalet, ilçe, şirket, şirket dizini, hesaplayıcı, zam sıralaması, yöntem) × 4
  genişlik × 2 tema: taşma 0, konsol 0, başarısız istek 0. Site haritası 952 URL (kademeli indeksleme planına göre).
- **11-25 düzeltmesi:** telefonda eyalet haritası yana kayıyor ve doğu yakası (en pahalı eyaletler dahil) ekran dışında
  kalıyordu, bunu belli eden bir şey yoktu → haritanın altında yalnız telefonda görünen kaydırma ipucu.

## Bilinen sınırlar

- Koyu tema yok (tasarım kararı, `DESIGN.md`).
- Gelir yok: AdSense `github.io` adresini kabul etmiyor, alan adı şart. Google "scaled content" riski için sayfalar
  kademeli açılıyor (344 → 21/42/70. gün).

## Dış adımlar (kodla çözülmez, Scryne'da)

Adım adım rehber: `docs/alan-adi-ve-reklam.md`.
1. Alan adı al (~10–12 $/yıl; öneri gridgrade.org, 10-24'te boştu, alırken yeniden bak).
2. DNS kayıtları (rehberdeki A + CNAME). Sonrası Claude'da: `SITE_URL`, Publish, Pages CNAME, HTTPS.
3. Search Console: alan adı doğrulama + site haritası.
4. AdSense başvurusu; onay gelince `ADSENSE_CLIENT` değişkeni.

## v2 fikirleri

- Ticari ve sanayi tarifeleri (şu an yalnız konut).
- Eyalet sayfasında aylık fiyatın mevsimsellikten arındırılmış eğrisi.
