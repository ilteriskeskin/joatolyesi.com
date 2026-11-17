# Aktif Sprint — 2026-11-17

Dal: `team/sprint-2026-11-17` (`team/sprint-2026-11-16` üstünden; 11-15 ve 11-16 henüz merge edilmedi). Push, deploy ve prod erişimi yok, `.env` okunmaz.
Planlı sprint. Plan BACKLOG sırasını izler: B-41a-2 (küçük kod). Planı orkestratör yazdı (kullanım tasarrufu).

## İş 1: B-41a-2 — seed bokken suburi 1/2/4 metinleri onaylı belgeyle uyum — `developer` → `qa-reviewer`
Yalnız onaylı içerik: `docs/team/content/verified/2026-11-15-30-gun-bokken-programi.md` (4. bölüm).
- `app/seed.py` içindeki `bokken-shomen-suburi` (suburi 1), `aiki-ken-suburi-2`, `aiki-ken-suburi-4` TR/EN metinleri onaylı belgedeki metinle birebir olur. Belgede onaylı metni olmayan alan değişmez.
- Seed program başına idempotent kalır; mevcut DB'de metin güncellemesi seed'in mevcut düzeniyle yapılır (yeni migration gerekmiyorsa açılmaz).
- Test eklenir (metin onaylı belgeyle eşleşir), tüm paket geçer.

## Başarı ölçütü
Hijyen işi (B-41 bokken programının doğruluğu): seed metinleri ile onaylı belge arasında fark sıfır.

## Sonuç
İş 1: kod yazıldı ama **test paketi çalıştırılamadı** (Docker daemon kapalı, test Postgres açılmadı; yerel venv yok). QA'ya "GEÇTİ" verdirilemezdi, kod commit edilmedi. Değişiklik `docs/team/patches/2026-11-17-b41a-2.patch` olarak saklandı (`git apply --check` temiz). EN metinler (1/2/4) değişmedi: onaylı belgede suburi başına EN metin yok.
