-- B-19 (B-12 düzeltmeleri): "Jo Nedir?" yazısında 3, "Jodo ve Jojutsu" yazısında 1 fact-check onaylı düzeltme.
-- Tek seferlik, idempotent (eski metin yoksa 0 satır günceller). Silme yok.
-- 2026-11-04-jo-nedir-notr.sql (B-16) uygulanmış olabilir; buradaki old parçalar o güncellemeden etkilenmeyen cümleleri kapsar.
-- Çalıştırma (prod, İlteriş): docker compose exec -T db psql -U <kullanıcı> <db> < docs/team/content/verified/2026-11-05-jo-yazisi-duzeltme.sql
BEGIN;

-- 1) Kısa tarih (Jo Nedir?)
UPDATE posts
SET body = replace(
  body,
  $old$Jo'nun en bilinen hikâyesi 17. yüzyıla dayanır. Rivayete göre samuray Muso Gonnosuke, efsanevi kılıç ustası Miyamoto Musashi'ye yenildikten sonra inzivaya çekilir, daha kısa ve daha çevik bir sopa üzerine çalışır ve Shinto Muso-ryu jojutsu'yu kurar. Bugün$old$,
  $new$Jo'nun en bilinen hikâyesi 17. yüzyılın başına dayanır. Rivayete göre samuray Muso Gonnosuke, efsanevi kılıç ustası Miyamoto Musashi'ye yenildikten sonra inzivaya çekilir, yeni bir sopa tekniği geliştirir ve Shinto Muso-ryu jojutsu'yu kurar. Okulun kendi aktarımına göre Gonnosuke daha sonra Musashi'yle yeniden karşılaşıp onu yenmiştir; bu ikinci karşılaşma okul dışındaki kaynaklarla doğrulanamaz. Bugün$new$
)
WHERE title = 'Jo Nedir? Dört Şeftali Ağacından Dojoya'
  AND body LIKE '%daha kısa ve daha çevik bir sopa üzerine çalışır%';
-- Beklenen: UPDATE 1 (zaten uygulandıysa UPDATE 0)

-- 2) Alıntı kutusu (Jo Nedir?)
UPDATE posts
SET body = replace(
  body,
  $old$> Jo, vücudunuzun iki tarafını da eşit çalıştıran nadir silahlardandır — sol elinizle de vurursunuz, sağ elinizle de.$old$,
  $new$> Jo, özellikle jododa, vücudun iki yanında da kullanılır: temel teknikler hem sağdan hem soldan çalışılır, eller yer değiştirir. Kılıç çalışmasında bu kadar iki taraflı bir kullanım daha az görülür.$new$
)
WHERE title = 'Jo Nedir? Dört Şeftali Ağacından Dojoya'
  AND body LIKE '%iki tarafını da eşit çalıştıran nadir silahlardandır%';
-- Beklenen: UPDATE 1 (zaten uygulandıysa UPDATE 0)

-- 3) Uzunluk (Jo Nedir?)
UPDATE posts
SET body = replace(
  body,
  $old$- **Uzunluk:** klasik ölçü 128 cm (4 shaku 2 sun 1 bu). Boyunuz kısaysa koltuk altı hizası da kabul görür.$old$,
  $new$- **Uzunluk:** geleneksel ölçü yaklaşık 128 cm (4 shaku 2 sun 1 bu). Boyunuza uygun ölçü dojodan dojoya değişebilir; satın almadan önce hocanıza danışın.$new$
)
WHERE title = 'Jo Nedir? Dört Şeftali Ağacından Dojoya'
  AND body LIKE '%Boyunuz kısaysa koltuk altı hizası da kabul görür.%';
-- Beklenen: UPDATE 1 (zaten uygulandıysa UPDATE 0)

-- 4) Giriş cümlesi (Jodo ve Jojutsu)
UPDATE posts
SET body = replace(
  body,
  $old$Jo'nun tarihi 17. yüzyıla, samuray Muso Gonnosuke'nin Shinto Muso-ryu jojutsu'yu kurmasına dayanır — bu hikâye$old$,
  $new$Jojutsu'nun en bilinen geleneği, okulun kendi aktarımına göre 17. yüzyıl başında samuray Muso Gonnosuke'nin kurduğu Shinto Muso-ryu'dur — bu hikâye$new$
)
WHERE title = 'Jodo ve Jojutsu: Aynı Silah, İki Farklı Yol'
  AND body LIKE '%Jo''nun tarihi 17. yüzyıla, samuray Muso Gonnosuke''nin%';
-- Beklenen: UPDATE 1 (zaten uygulandıysa UPDATE 0)

COMMIT;
