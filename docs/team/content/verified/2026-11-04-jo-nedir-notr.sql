-- B-16: "Jo Nedir?" yazısındaki birinci şahıs cümleyi fact-check onaylı metinle değiştirir.
-- Tek seferlik, idempotent (eski metin yoksa 0 satır günceller). Silme yok.
-- Çalıştırma (prod, İlteriş): docker compose exec -T db psql -U <kullanıcı> <db> < docs/team/content/verified/2026-11-04-jo-nedir-notr.sql
BEGIN;
UPDATE posts
SET body = replace(
  body,
  $old$Benim için cevap basit: **jo affedicidir ama yalan söylemez.** Kılıçta kesişin doğru olup olmadığını başta göremezsiniz; jo'da dengesiz bir tsuki attığınızda sopa elinizde kımıldar, hemen söyler.$old$,
  $new$Jo ile başlamanın bir gerekçesi şu görüşle özetlenebilir: **jo affedicidir ama yalan söylemez.** Bu bakışa göre kılıçta kesişin doğru olup olmadığı başlangıçta her zaman kolay fark edilmez; jo'da ise dengesiz bir tsuki çoğu zaman sopanın elinizde kımıldamasıyla kendini belli eder.$new$
)
WHERE title = 'Jo Nedir? Dört Şeftali Ağacından Dojoya'
  AND body LIKE '%Benim için cevap basit:%';
-- Beklenen: UPDATE 1 (zaten uygulandıysa UPDATE 0)
COMMIT;
