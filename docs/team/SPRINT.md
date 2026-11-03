# Aktif Sprint — 2026-11-03

Dal: `team/sprint-2026-11-03` · İlk sprint (önceki rapor yok, devreden iş yok).
Çalıştırma: otomatik, gözetimsiz. Push/deploy/prod erişimi yok, dışarıya gönderi yok, `.env` okunmaz.

## Hedef (tek cümle)

Kayıt → ilk pratik → geri dönüş hunisini ve Instagram trafiğini **ölçülebilir** hale getirmek; bir sonraki sprintin kararı tahminle değil rakamla verilsin.

## Teşhis (2026-11-02 başlangıç verisi, `METRICS.md`)

- GA4 son 28 gün: 40 aktif kullanıcı, 38 yeni, ort. etkileşim 20 sn, geri gelen kullanıcı ≈ 0. Trafiğin bir kısmı muhtemelen bot/veri merkezi (Ashburn, Altoona, San Jose, Dublin).
- Kaynak: google/organic 17, direct 14, instagram ~5. Instagram'daki büyük izlenmeler (138k'ya ulaşan videolar) siteye yansımıyor.
- **Kuzey yıldızı metrik (haftalık aktif pratisyen) bilinmiyor.** Yeni kayıt sayısı bilinmiyor. GA4'te özel olay yok; DB'den metrik üreten bir script yok. Bu yüzden hiçbir dönüşüm/elde tutma hipotezi şu an test edilemez.
- Önceki sprint hipotezi: yok (ilk sprint).
- Sonuç: Bu sprint yeni özellik değil, **ölçüm + en ucuz dağıtım kaldıracı**. Elde tutma işleri (B-09) ölçüm geldikten sonra.

## Önceliklendirme (Etki × Güven / Emek)

| İş | Puan | Karar |
|---|---|---|
| B-01 GA4 dönüşüm olayları | 5×5/1 = 25 | **Seçildi** |
| B-04 Instagram → site hunisi (taslak) | 5×4/1 = 20 | **Seçildi** |
| B-02 `scripts/weekly_metrics.py` | 5×5/2 = 12.5 | **Seçildi** |
| B-05 SEO anahtar kelime haritası | 4×4/2 = 8 | Sonraki sprint |
| B-06 Teknik SEO | 4×4/2 = 8 | Sonraki sprint |
| B-09 İlk seans akışı | 4×3/3 = 4 | Ölçüm sonrası |
| B-03 Demo hesaplar | — | Karar İlteriş'te → raporda sorulacak |
| B-10 Resend domain doğrulaması | 5×3/1 | İlteriş'in 10 dk kontrolü → raporda |

Tahmini toplam emek: ~2,5-3,5 saat agent işi.

---

## İş 1 — B-01: GA4 dönüşüm olayları

**Sorumlu:** `developer` → `qa-reviewer`

**Neden:** Huniyi (kayıt, ilk seans, paylaşım, PWA yükleme) GA4'te görmeden hiçbir büyüme deneyini değerlendiremeyiz. Kaynak bazlı (instagram/google) kayıt dönüşümü ancak bu olaylarla görünür.

**Kapsam:** Mevcut GA4 (G-54NX2S2Z01, `app/templates/base.html` ve `app/templates/index.html` içindeki gtag) üzerine 4 olay. Yeni tracker, yeni paket, yeni servis yok.

| Olay | Ne zaman | Parametreler (PII yok) |
|---|---|---|
| `sign_up` | Kayıt başarılı olduktan sonraki ilk sayfa yüklemesinde, **bir kez** | `method: "email"`, `discipline` |
| `practice_logged` | `/app/practice` POST başarılı olduğunda (HTMX yanıtı) ve kata sayfasındaki "Bugün bunu çalıştım" kaydında | `discipline`, `minutes`, `source: "dashboard"\|"kata"` |
| `share_card` | `app/static/js/share.js` paylaş veya indir tıklaması | `method: "native"\|"download"\|"x"\|"whatsapp"`, `context: "profile"\|"dashboard"` |
| `pwa_install` | `app/static/js/install-prompt.js` içinde `appinstalled` olayı (ve/veya prompt kabul sonucu `accepted`) | — |

**Uygulama notları:**
- `register` (`app/routers/auth.py`) redirect ile bitiyor; sunucu tarafında gtag çağrılamaz. Önerilen yol: kısa ömürlü bir işaret (ör. tek seferlik cookie ya da `?welcome=1`), `base.html` bunu görünce `sign_up` gönderir ve işareti temizler. Yenilemede tekrar göndermemeli.
- `practice_logged` için HTMX yanıtına `HX-Trigger` başlığı eklemek ya da dönen partial'a (`app/templates/_practice_panel.html`) küçük bir inline script koymak; hangisi mevcut yapıyla uyumluysa.
- Her çağrı `typeof gtag === "function"` korumalı olsun; GA yüklenmezse (adblock) JS hatası vermesin.
- **Admin sayfalarında GA kapalı kalmalı** (commit b0c68f0'daki token sızıntısı düzeltmesi bozulmasın).
- Olay parametrelerinde e-posta, kullanıcı adı, kullanıcı id'si, not metni **olmayacak**.
- Kod tekrarını azaltmak için küçük bir yardımcı (ör. `app/static/js/analytics.js` içinde `track(name, params)`) kabul edilebilir.

**Kabul kriterleri:**
1. 4 olayın her biri yukarıdaki tetikleyicide tam bir kez çağrılıyor (kod incelemesi + mümkünse yerel tarayıcıda `dataLayer` kontrolü).
2. `sign_up` sayfa yenilemesinde tekrar gönderilmiyor.
3. Hiçbir olay parametresinde PII yok.
4. `/admin*` şablonlarında gtag hâlâ yok.
5. GA yüklenmediğinde konsolda hata yok.
6. Mevcut `pytest` testleri geçiyor; register sonrası işaretin bir kez render edildiğini doğrulayan en az 1 yeni test (`tests/test_flows.py`). Test Postgres'i ayağa kalkamıyorsa bunu açıkça raporla, testi yine de yaz.
7. `docs/team/METRICS.md`'ye kısa bir "GA4 olayları" bölümü: olay adları + İlteriş'in GA4'te `sign_up` ve `practice_logged`'ı "Key event" olarak işaretlemesi gerektiği notu.

**Ölçülecek metrik:** GA4 → `sign_up` / oturum (kaynak bazında: google/organic, instagram, direct), `practice_logged` / `sign_up`. İlk veri deploy'dan ≥1 hafta sonra.

**Emek:** ~1-1,5 saat. **Sunucu etkisi:** yok (yalnız istemci JS + 1 küçük cookie/param).

---

## İş 2 — B-02: `scripts/weekly_metrics.py`

**Sorumlu:** `developer` → `qa-reviewer`

**Neden:** Kuzey yıldızı metrik (haftalık aktif pratisyen) GA4'te ölçülemez; gerçek kaynak DB. İlteriş'in haftada 30 dk'sını korumak için tek komut, yapıştırılabilir çıktı.

**Çalıştırma hedefi:** `docker compose exec app python scripts/weekly_metrics.py [--week-start YYYY-MM-DD]` (varsayılan: son tamamlanan Pazartesi-Pazar haftası). Mevcut `scripts/send_weekly_digest.py` / `app/db.py::async_session` kalıbını izle.

**Hesaplanacaklar (hafta penceresi Pazartesi başlangıçlı, `weekly_leaders()` ile aynı tanım):**
1. **Haftalık aktif pratisyen:** hafta içinde `practice_logs.practiced_on` ≥1 olan farklı kullanıcı sayısı.
2. **Yeni kayıt:** `users.created_at` hafta içinde.
3. **Kayıttan ilk seansa dönüşüm:** o hafta kayıt olanlardan ≥1 practice_log'u olanların oranı (ve 24 saat içinde olanların oranı, ayrı).
4. **7. gün geri dönüş:** hafta başından 7-13 gün önce kayıt olan kohorttan, kayıt gününden sonraki 7.-13. günler arasında ≥1 pratik kaydı olanların oranı. Kohort boşsa "n=0" yaz, oran uydurma.
5. Toplam kullanıcı ve toplam pratik kaydı (bağlam için).

**Hariç tutma (zorunlu):**
- Demo hesaplar: `scripts/seed_blog.py` ile oluşturulan, e-postası `@demo.joatolyesi.com` ile biten hesaplar. Hariç tutma kuralı tek bir sabitte/fonksiyonda dursun.
- Sahip hesabı (`scripts/backfill_practice.py::OWNER_EMAIL`): geçmişi backfill ile doldurulduğu için metrikleri şişirir. Ana sayıdan hariç tut, çıktıda "sahip hesabı dahil edilmedi" notu düş. E-postayı koda yeniden yazma; mevcut sabiti import et ya da ortak bir sabite taşı.
- Hariç tutulan hesap sayısı çıktıda görünsün (şeffaflık).

**Çıktı:** stdout'a, `docs/team/METRICS.md` haftalık tablosuna doğrudan yapıştırılabilir bir Markdown satırı + altında okunur bir özet bloğu. GA sütunları script tarafından doldurulamaz; `—` bırak.

**Kısıtlar:**
- Salt okuma: hiçbir INSERT/UPDATE/DELETE yok.
- Yalnız SQL agregasyonları (COUNT/DISTINCT); tüm satırları Python belleğine çekme. Yeni bağımlılık yok. 512 MB prod'da birkaç saniyede biten tek seferlik komut.
- Kişisel veri (e-posta, kullanıcı adı) yazdırma.

**Kabul kriterleri:**
1. Script yukarıdaki 5 metriği hesaplıyor, demo + sahip hesaplarını hariç tutuyor ve hariç tutulan sayıyı yazıyor.
2. Hesaplama mantığı test edilebilir bir fonksiyonda; `tests/` altında en az 1 test: demo hesabı ve gerçek hesap oluştur, demo'nun sayılmadığını ve haftalık aktif sayısının doğru olduğunu doğrula. Test Postgres'i ayağa kalkamıyorsa açıkça raporla.
3. Yazma sorgusu yok (diff incelemesinde doğrulanır).
4. Çıktı satırının sütun sırası `METRICS.md` tablosuyla birebir aynı.
5. `docs/team/METRICS.md` başındaki açıklamaya çalıştırma komutu eklendi.
6. Script yerelde gerçek prod verisi olmadan çalıştırıldıysa, örnek çıktı rapora "yerel test DB'si, gerçek rakam değil" etiketiyle konur. **METRICS.md tablosuna hiçbir rakam yazılmaz** — onu İlteriş prod'da çalıştırıp yapıştırır.

**Ölçülecek metrik:** Bu işin kendisi metriği üretir; başarı = İlteriş'in ilk çalıştırmada tabloya kuzey yıldızı rakamını yapıştırabilmesi.

**Emek:** ~1-1,5 saat. **Sunucu etkisi:** haftada bir, saniyeler süren birkaç COUNT sorgusu; ihmal edilebilir.

---

## İş 3 — B-04: Instagram → site hunisi (taslak)

**Sorumlu:** `growth-marketer` (taslak) → teknik dövüş sanatı iddiası içeren metinler için `fact-checker`. Paylaşım: İlteriş.

**Neden:** En büyük varlık dağıtım; Instagram izlenmeleri siteye ~5 oturum olarak düşüyor. Bütçe 0, kod gerektirmeyen en ucuz kaldıraç.

**Çıktı dosyası:** `docs/team/marketing/2026-11-03-instagram-hunisi.md`

**İçerik:**
1. **Teşhis:** Instagram trafiği GA4'te neden düşük görünüyor olabilir (bio'da link yok/yanlış, Instagram uygulama içi tarayıcının referrer'ı kaybedip trafiği "direct"e yazması, reels'ta CTA yok). Her olasılık için "nasıl doğrulanır" adımı. Doğrulanmamış şeyi kesin gibi yazma.
2. **Link şeması:** GA4'ün tanıdığı UTM'li linkler (`utm_source=instagram&utm_medium=social&utm_campaign=<bio|reel-...|story>`). Not: kullanıcı kaydında `?src=` saklanmıyor, yalnız waitlist'te var (`WAITLIST_GROWTH.md`); bu yüzden UTM + İş 1'deki `sign_up` olayı asıl ölçüm yolu. Linkler **yalnız var olan sayfalara** gitsin: `/`, `/kata`, `/kata?d=<branş>`, `/kata/<slug>`, `/guide`, `/guide/<branş>`, `/register`. Her URL'nin route olarak var olduğunu kontrol et (`app/routers/kata.py`, `app/routers/guide.py`, slug'lar için `app/seed.py`).
3. **Bio metni:** TR ve EN, 150 karakter sınırına uygun 2 seçenek + bio link.
4. **İçerik ↔ sayfa eşleme tablosu:** İlteriş'in video türleri (jo suburi, bokken, kata) için "bu tür videonun altında şu CTA, şu sayfaya" — en az 5 satır. Sayfa, videoda görülenle eşleşmeli (jo videosu → `/kata?d=aikijo` ya da ilgili kata sayfası).
5. **5 reels/story CTA + açıklama taslağı** (TR, mümkünse EN): kısa, abartısız. "Binlerce kullanıcı", uydurma sayı, sahte sosyal kanıt yok. Tek kişiyle 15-45 sn çekilebilir fikirler.
6. **İlteriş'in tek somut adımları:** en fazla 3 madde, toplam ≤10 dk.
7. **Ölçüm planı:** GA4'te nereye bakılacak (Edinme → Trafik edinme, oturum kaynağı/aracı = instagram/social; `sign_up` kaynak bazında). 2 haftalık başarı eşiği **hipotez olarak** yazılsın, hacim tahmini uydurmadan.
8. Teknik iddia içeren her metin (kata adı, teknik tarifi) `[fact-check]` ile işaretli.

**Kabul kriterleri:**
1. Dosya yukarıdaki 8 bölümü içeriyor.
2. Her link var olan bir route'a gidiyor ve UTM şeması tutarlı.
3. Uydurma rakam/kullanıcı/yorum yok; bilinmeyen değerler "bilinmiyor" diye yazılmış.
4. İlteriş'in aksiyonu ≤3 madde, ≤10 dk.
5. `[fact-check]` işaretli metinler fact-checker'dan geçti ya da raporda "doğrulanmadı, kullanma" diye listelendi.
6. Hiçbir yere gönderi/mesaj atılmadı.

**Ölçülecek metrik:** GA4 instagram kaynaklı oturum (başlangıç ~5 / 28 gün) ve instagram kaynaklı `sign_up` (başlangıç: ölçülmüyor).

**Emek:** ~1 saat. **Sunucu etkisi:** yok.

---

## Bağımlılıklar

- İş 1, İş 2, İş 3 **birbirinden bağımsız**, paralel yürütülebilir.
- Dosya çakışma riski: İş 1 ve İş 2 ikisi de `docs/team/METRICS.md`'ye ekleme yapar (farklı bölümler). İkisi de `developer`'daysa sırayla yapılsın ya da METRICS.md düzenlemesi en sonda tek seferde birleştirilsin. Kod dosyaları çakışmıyor (İş 1: şablonlar/JS/`auth.py`/`practice.py`; İş 2: yeni script + test).
- İş 3'ün ölçüm planı İş 1'deki `sign_up` olayına atıf yapar ama yazımı İş 1'in bitmesini beklemez.

## Raporda İlteriş'e sorulacaklar (bu sprintte uygulanmayacak)

1. **B-03 demo hesaplar:** 7 demo profil uydurma seri/kuşak/takip gösteriyor ve "örnek" etiketi yok. Ekip önerisi (b): yazıları "Joryu Ekibi" yazarına taşı, profilleri gizle. Onay?
2. **B-10:** Resend panelinde joatolyesi.com domain'i doğrulandı mı (SPF/DKIM)? Doğrulanmadıysa hatırlatma ve haftalık özet mailleri hiç gitmiyor.
3. Deploy sonrası GA4'te `sign_up` ve `practice_logged`'ı Key event olarak işaretle.
4. Prod'da `scripts/weekly_metrics.py`'yi çalıştırıp çıktıyı `METRICS.md`'ye yapıştır — **kuzey yıldızı rakamı şu an yok.**
5. Instagram bio linkini taslaktaki UTM'li linkle değiştir.

## Metrik veri durumu (açık not)

Kuzey yıldızı (haftalık aktif pratisyen), yeni kayıt, 7. gün geri dönüş ve kayıttan ilk seansa dönüşüm için **hiç veri yok**. Bu sprintte hiçbir agent bu alanlara rakam yazmaz; rakamlar ancak İlteriş deploy edip script'i prod'da çalıştırınca ve GA4 olayları ≥1 hafta veri toplayınca gelir.
