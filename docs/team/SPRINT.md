# Aktif Sprint — 2026-11-09

Dal: `team/sprint-2026-11-09` (`team/sprint-2026-11-08` üstünden; o dal merge bekliyor). Push/deploy/prod erişimi yok, `.env` okunmaz.
Planlı sprint; kullanım tasarrufu gereği tek kod işi. Plan orkestratör tarafından yazıldı (BACKLOG önerilen sırası: B-32 → B-28).

## İş: B-32 — push izin anı — `developer` → `qa-reviewer`

Hipotez: Bildirim izni, kullanıcı ilk pratiğini kaydedip değeri gördükten sonra bağlamsal bir kartla istenirse kabul oranı artar. Bu da 7. güne ulaşan programa devamı (`program_day_complete` day≥7) yükseltir.

Kapsam: İlk gerçek (dinlenme günü olmayan) pratik kaydından sonra dashboard'da kapatılabilir bir kart çıkar. Tarayıcı izin penceresi yalnız "Hatırlatmayı aç" tıklamasında açılır. Kart şu durumlarda gizli kalır: izin granted/denied, abonelik var, tarayıcı desteklemiyor, kart daha önce kapatılmış (localStorage). Mevcut buton korunur.

## Başarı ölçütü
QA GEÇTİ (✓). Metrik (deploy'dan 14 gün, GA4): `push_prompt_accept / push_prompt_shown` oranı, `push_prompt_dismiss`, `program_day_complete` day≥7.

## QA
GEÇTİ (1. tur). 144 test geçti, 1 test kaldı. Kalan `test_sitemap_includes_blog_posts` B-32 değişiklikleri olmadan HEAD'de de kalıyor, yani önceden var olan bir sorun.
