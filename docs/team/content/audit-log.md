# İçerik denetim kaydı

fact-checker her sprint mevcut site içeriğinden örneklem denetler.

| Tarih | Dosya | İddia | Sonuç | Kaynak |
|---|---|---|---|---|
| 2026-11-03 | app/seed.py `aikijo-happo-giri` | "kuzeyden başlayıp saat yönünde 8 yöne men uchi", "en iyi ısınma" | ❌ Kaynakla desteklenmiyor. Jo ile 8 yönlü kesiş için orta/güçlü kaynak bulunamadı. Wikipedia (zayıf) jo karşılığını happo-no-tsuki (dürtüş) olarak veriyor. Bokken happo giri için aktarılan yaygın sıra saat yönünde değil. "En iyi" ifadesi abartı. Düzeltme taslağı açılmalı. | https://en.wikipedia.org/wiki/Happo-giri, https://aikidoaus.com.au/library/aiki-ken-curriculum/ |
| 2026-11-03 | app/seed.py JODO (12 kata slug'ı ve sırası) | Seitei Jōdō 12 kata, 1 Tsukizue … 12 Ran ai | ✅ Ad ve sıra doğru. Kata açıklamaları denetlenmedi. | https://clakendo.org/wp-content/uploads/2024/03/Examen-Teorico-de-JODO-de-CLAK.pdf, https://old2.kendo.or.jp/examination/docs/JODO-KYOSHI_written-test_point_201511.pdf |
| 2026-11-03 | app/seed.py AIKIJO teknik (20 suburi) ve BOKKEN 7 suburi | Saito yöntemi 20 jo suburi, ilk üçü choku/kaeshi/ushiro tsuki; 7 aiki-ken suburi | ✅ Sayılar ve ilk sıralar doğru. Hareket tarifleri denetlenmedi. | https://takemusu-iwama-aikido.org/?p=260, https://aikido-shuren-dojo.com/?p=87, https://aikidoaus.com.au/library/aiki-ken-curriculum/ |
