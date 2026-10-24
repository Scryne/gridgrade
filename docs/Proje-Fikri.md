---
proje: GridGrade
created: 2026-10-24
type: proje-fikri
status: kesin
---
# GridGrade — Proje Fikri

## Problem
ABD'de elektrik faturaları 2025–26'da hızla arttı. İnsanlar "eyaletimde elektrik kWh kaç sent", "ortalama fatura ne kadar",
"ilçemde elektriği kim sağlıyor" diye arıyor. Mevcut siteler eyalet ortalamasında kalıyor; şirket (utility) bazında fiyat, fatura
ve kesinti güvenilirliğini bir arada, anlaşılır bir notla veren bir kaynak yok. EIA'nın kamu verisi bunu mümkün kılıyor ama ham
Excel dosyalarında, sıradan kullanıcının erişemeyeceği hâlde duruyor.

Scryne için amaç: hiç bakım gerektirmeden kendini güncelleyen, arama trafiği çeken, reklamla gelir getiren bir site
(Tezgah'tan ayrı pasif kol; Scryne "her şeyi sana bırakıyorum, tüm yetki sende", 2026-10-24).

## Hedef Kullanıcı
ABD'de fatura ödeyen hane; taşınmayı düşünen; yerel haberci; enerji/güneş paneli araştıran kişi.

## v1: Kapsam ve "Bitti" Tanımı
- **Süre tavanı:** tek gece (2026-10-24) inşa + yayın; sonrası otomatik.
- **Bitti = kullanıldı:** site herkese açık adreste yayında, her gün GitHub Actions ile EIA'dan veri kontrol edip yeni veri varsa
  kendini yeniden üretiyor; Google'a site haritası verilebilir durumda; Scryne'a kalan yalnız alan adı + AdSense başvurusu.
  Gelir ölçütü ayrı: Search Console'da ilk gösterimler (~1 ay), AdSense onayı, 6. ayda trafik kararı.
- **Temel özellikler:**
  1. Eyalet sayfaları: aylık fiyat trendi (grafik), sektörler, ABD ortalamasıyla kıyas, sıralama, eyaletteki şirketler.
  2. Şirket karneleri: ortalama fiyat, fatura, tüketim, abone, sahiplik türü, kesinti istatistikleri; şeffaf yöntemle A–F not.
  3. İlçe sayfaları: ilçede hizmet veren şirketler ve karşılaştırması.
  4. Sıralamalar ve fatura hesaplayıcı.
  5. Otomatik güncelleme hattı + kademeli indeksleme (başta ~500 sayfa, haftalar içinde açılır).
  6. Yöntem, hakkında, gizlilik sayfaları (AdSense ve güven için).

## Kapsam Dışı
- Kullanıcı hesabı, yorum, form, kişisel veri toplama.
- Tarife (rate schedule) ayrıntısı, tedarikçi karşılaştırma/affiliate, enerji tavsiyesi.
- Türkçe sürüm (araştırma tamamlanmadı).

## Açık Sorular
- Alan adı (gridgrade.org önerisi) ve AdSense: Scryne'ın kararı ve hesabı.
