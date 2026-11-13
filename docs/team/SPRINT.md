# Aktif Sprint — 2026-11-13

Dal: `team/sprint-2026-11-13` (`main`'den; 12 dalları merge edildi). Push, deploy ve prod erişimi yok, `.env` okunmaz.
Planlı sprint. Plan BACKLOG'daki sırayı izler: B-40 şablonu + B-37 ilk 5 sayfa. Planı orkestratör yazdı.

## İş 1: B-37 ilk 5 sayfa içeriği — `content-writer` → `fact-checker`
Gösterim sırasına göre ilk 5 kata/teknik sayfası (guide/blog şablonu farklı, sonraki partide):
`tkd-dwit-chagi`, `karate-zenkutsu-dachi`, `tkd-naeryo-chagi`, `kendo-kodachi-1`, `karate-kiba-dachi`.
Her biri için TR/EN: title, meta, "Nedir", "Nasıl yapılır" (adımlar), "Sık hatalar", "İlgili teknikler" (yalnız mevcut slug'lar).
Fact-checker onayı olmayan madde koda girmez.

## İş 2: B-40 detay sayfası şablonu — `developer` → `qa-reviewer`
Migration'sız, slug'a göre içerik modülü (`app/kata_content.py`). Bölümü olmayan sayfa eski görünümde kalır. Title/meta içerikten gelir. Mobil öncelikli.

## Başarı ölçütü
Testler yeşil; 5 sayfa yeni düzende. Ölçüm: 4 hafta sonra bu sayfaların GSC TO'su (hedef %2).

## Sonuç
İş 1: fact-checker 4 slug'ı kısmi onayladı. kendo-kodachi-1 ertelendi: tek bağımsız kaynak var ve adım dökümü yok.
İş 2: developer uyguladı, QA GEÇTİ verdi (f5ef0df). Test Postgres'iyle tam koşu: 154/154.
