# Aktif Sprint — 2026-11-05

Dal: `team/sprint-2026-11-05` (`main`'den; önceki sprint dalları merge edilmiş). Push/deploy/prod erişimi yok, `.env` okunmaz.
Planlı (zamanlanmış) sprint; kullanım tasarrufu kuralı gereği iki küçük iş. Plan tasarruf için orkestratör tarafından yazıldı.

## İşler

### B-17 Test izolasyonu — `developer` → `qa-reviewer`
`tests/test_demo_hidden.py::test_demo_hidden_from_public_surfaces` aynı test DB'sinde ikinci koşuda düşüyor (`weekly_leaders` önceki testlerin verisini görüyor). Hedef: test suite aynı DB'de art arda iki kez yeşil. Uygulama kodu değişmez (yalnız testler/fixture).

### B-12 İçerik denetimi (3 iddia) — `fact-checker`
`scripts/seed_blog.py` jo yazısında audit-log'da bekleyen adaylardan 3 iddia: "128 cm / 4 shaku 2 sun 1 bu", Muso Gonnosuke–Musashi tarihi, "iki tarafı eşit çalıştıran nadir silah". Sonuç `docs/team/content/audit-log.md`'ye. Bu sprintte koda içerik girmez; düzeltme gerekiyorsa taslak `content/verified/`a yazılır, uygulama sonraki sprint.

## Başarı ölçütü
B-17: `pytest` aynı DB'de iki kez art arda geçer. B-12: 3 iddia kaynaklı sonuçla kayıtlı.
