# Aktif Sprint — 2026-11-15

Dal: `team/sprint-2026-11-15` (`main`'den; önceki sprint dalları merge edilmiş). Push, deploy ve prod erişimi yok, `.env` okunmaz.
Planlı sprint. Plan BACKLOG sırasını izler: B-41a. Kullanım tasarrufu gereği bugün yalnız içerik kısmı yapılır; program seçimi kodu (B-41a kod) sonraki sprintte, onaylı içerikle. Planı orkestratör yazdı.

## İş 1: B-41a bokken 30 günlük program içeriği — `content-writer` → `fact-checker`
Kaynak taslak: `app/guide_content.py` `PROGRAMS["bokken"]`. Biçim örneği: `docs/team/content/verified/2026-11-05-30-gun-jo-programi.md` (WEEKS + gün metinleri).
- Aikiken suburi 1-7 (Saito/Iwama numaralandırması), 4 hafta + 2 gün; her günün odağı, TR/EN kısa açıklama.
- B-33 kuralları: her suburi ≥10 tekrar önerisi, önce temel (ichi no suburi) — yalnız tavsiye, sayaç/kilit yok.
- Gün planı bizim pedagojik tasarımımız; teknik açıklamalar (her suburinin hareketi) kaynaklı. Partnerli kata (kumitachi) programa girmez.
- Fact-checker onayı olmayan madde `verified`'e girmez.

## Başarı ölçütü
Onaylı içerik `docs/team/content/verified/` altında, koda girmeye hazır. Ölçüm (kod deploy'undan sonra): bokken programına başlayan kullanıcı sayısı, 4 hafta.

## Sonuç
İş 1: fact-checker KISMİ ONAY verdi (düzeltilmiş). Onaylı metin: `docs/team/content/verified/2026-11-15-30-gun-bokken-programi.md`. Tek kaynağa dayanan ayrıntılar (ichi'de ayak, go'da açı, roku'da ayak/kesiş türü) çıkarıldı. San no suburi'de waki gamae/gedan çelişkisi metne yazıldı. Seed'deki bokken suburi 3/5/6/7 metinleri kaynaksız; audit-log'a eklendi.
