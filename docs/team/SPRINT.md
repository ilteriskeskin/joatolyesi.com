# Aktif Sprint — 2026-11-04 (ikinci tur)

Dal: `team/sprint-2026-11-04` (main ile aynı noktadan devam). İlteriş, raporu okuduktan sonra canlı olarak "bugün yeni işler" istedi.
Push/deploy/prod erişimi yok, `.env` okunmaz.

## Kısa teşhis

- B-09 kartı prod'da görünmüyor. Sebep kod değil: `/practitioners` hâlâ demo profilleri listeliyor ve `/u/aksam-keiko` 200 dönüyor, yani prod B-03/B-09 öncesi imajla çalışıyor. `ea769bd` için CI imajı başarıyla üretilmiş (GitHub Actions), sunucu henüz çekmemiş.
- Instagram trafiği geliyor ama aramadan gelen trafik için temel eksik: base.html'de canonical/hreflang/og var; yapılandırılmış veri (JSON-LD) ve sayfaya özel meta yok.

## İşler

### B-06 Teknik SEO — `developer` → `qa-reviewer`
Kata detay, rehber ve blog yazısı sayfalarında sayfaya özel title/meta description, JSON-LD (Article / BreadcrumbList), sayfalar arası iç linkler. Yeni bağımlılık yok, ek sorgu en fazla 1.

### B-05 SEO anahtar kelime haritası — `growth-marketer`
Mevcut kata, rehber ve blog sayfaları için TR+EN hedef sorgu, title/meta/H1 önerisi. Taslak `docs/team/marketing/` altına yazılır; kod değişmez. B-06'nın title önerilerini sonraki turda besler.

## Başarı ölçütü
Deploy sonrası Google Search Console'da yapılandırılmış veri hatası 0; 4 hafta içinde organik tıklamalar (GSC) referans alınır.
