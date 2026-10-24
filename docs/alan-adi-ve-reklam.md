# Alan adı, Search Console ve AdSense — adım adım

Site şu an `https://scryne.github.io/gridgrade-site/` adresinde canlı. AdSense `github.io` adreslerini kabul etmediği için kendi
alan adı gerekiyor. Önerilen: **gridgrade.org** (2026-10-24 RDAP sorgusunda boştu; gridgrade.com alınmış).

## 1. Alan adını al (Scryne — para harcaması)
- Kayıt şirketi: Cloudflare Registrar, Porkbun ya da Namecheap. `.org` yıllık ~10–12 $.
- WHOIS gizliliği açık olsun (çoğu ücretsiz verir).

## 2. DNS kayıtları (Scryne, kayıt şirketinin DNS panelinde)
| Tür | Ad | Değer |
|---|---|---|
| A | `@` | `185.199.108.153` |
| A | `@` | `185.199.109.153` |
| A | `@` | `185.199.110.153` |
| A | `@` | `185.199.111.153` |
| CNAME | `www` | `scryne.github.io` |

Cloudflare kullanılıyorsa bu kayıtlarda turuncu bulutu (proxy) kapat ("DNS only"), yoksa GitHub sertifikası üretilemez.

## 3. Siteyi alan adına geçir (Claude, Scryne "alan adı alındı" deyince)
```bash
gh variable set SITE_URL --body "https://gridgrade.org" -R Scryne/gridgrade
gh workflow run Publish -R Scryne/gridgrade          # TABAN "" olur, dist/CNAME üretilir
gh api -X PUT repos/Scryne/gridgrade-site/pages -f cname=gridgrade.org
# sertifika gelince (birkaç dakika–1 saat):
gh api -X PUT repos/Scryne/gridgrade-site/pages -F https_enforced=true
```
Eski github.io adresleri GitHub tarafından yeni alan adına yönlendirilir.

## 4. Google Search Console (Scryne'ın Google hesabı)
- search.google.com/search-console → **Alan adı (Domain)** mülkü → `gridgrade.org` → verilen TXT kaydını DNS'e ekle → Doğrula.
- Sol menü **Site haritaları** → `https://gridgrade.org/sitemap.xml` gönder.
- Bing Webmaster Tools'a Search Console'dan içe aktararak eklenebilir (IndexNow zaten çalışıyor).

## 5. AdSense başvurusu (Scryne'ın hesabı)
- adsense.google.com → site ekle: `gridgrade.org`.
- Verilen yayıncı kimliğini (`ca-pub-…`) Claude'a ilet. Claude:
  `gh variable set ADSENSE_CLIENT --body "ca-pub-…" -R Scryne/gridgrade` → yayın; sayfalara reklam kodu ve `ads.txt` kendiliğinden eklenir.
- Onay birkaç gün–birkaç hafta sürer. Reddedilirse genelde sebep "yetersiz içerik/trafik"tir; ilk katmanların açılmasını (21. ve
  42. gün) bekleyip yeniden başvurulur.
- AB/İngiltere ziyaretçileri için AdSense, Google'ın onaylı rıza (CMP) mesajını ister: AdSense → Gizlilik ve mesajlar → GDPR mesajını aç.

## Beklenti
Yeni alan adında ilk 3 ay trafik ihmal edilebilir, anlamlı gelir en erken 6–12. ayda (araştırma, `docs/arastirma/2026-10-24-nis.md`).
Kademeli indeksleme kendiliğinden açılır: 21. günde ≥10.000 aboneli şirketler, 42. günde ilçeler, 70. günde tümü.
