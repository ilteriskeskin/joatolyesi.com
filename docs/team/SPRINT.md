# Aktif Sprint — 2026-11-10

Dal: `team/sprint-2026-11-10` (`team/sprint-2026-11-09` üstünden, o dal da merge bekliyor). Push, deploy ve prod erişimi yok, `.env` okunmaz.
Planlı sprint. Kullanım tasarrufu için tek küçük iş seçildi. Planı orkestratör yazdı ve BACKLOG'daki önerilen sırayı izledi.

## İş: B-36 — kırık sitemap testi — `developer` → `qa-reviewer`

Amaç: Test paketi temiz ortamda tamamen yeşil olsun. Böylece sonraki işlerde (B-28) gerçek regresyonlar kırık bir testin arkasında saklanmaz.

## Başarı ölçütü
Temiz ortamda (`.env` yok) tüm testler geçer. ✓ 145/145.

## QA
GEÇTİ (1. tur). Yalnız `tests/conftest.py` değişti, uygulama koduna dokunulmadı.
