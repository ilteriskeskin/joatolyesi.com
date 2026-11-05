# Backlog

PO önceliklendirir. Puan = (Etki × Güven) / Emek, her biri 1-5. Yeni fikir
eklenebilir; tamamlanan iş `[x]` ile işaretlenip rapora bağlanır.

## Yön (PO kararı, 2026-11-05) — 2 haftalık büyüme hamlesi

Teşhis: 10 gerçek kullanıcı, haftalık aktif ~0; Instagram videoları 138k izlenmeye kadar çıkıyor ama siteye ~5 oturum geliyor. Darboğaz ürün cilası değil, **teklif + dağıtım**. Bundan sonra her sprint işi bir büyüme hipotezine ve bir metriğe bağlanır. Hijyen/bakım işleri yalnız bir büyüme işini engelliyorsa seçilir.

Sıra:
1. **B-20** 30 günlük jo programı ücretsiz + Instagram açılış sayfası (sprint 2026-11-05b).
2. **B-21** Instagram kampanyası (growth-marketer taslak → İlteriş paylaşır, 14 gün).
3. **B-22** Program e-posta dizisi: kayıt/enroll sonrası gün 1, 3, 7 hatırlatma ("dün kaldığın gün"). Resend çalışıyor.
4. **B-23** Hoca/dojo pilotu: hoca öğrencilerine haftalık ödev verir, kimin çalıştığını görür. Önce İlteriş'in kendi dojosunda 1 pilot.
5. B-07, B-08, B-13 (organik kanal) bunlardan sonra.

Hipotez (B-20/21): Instagram'dan gelen ziyaretçiye somut, ücretsiz bir 30 günlük hedef sunulursa kayıt ve 7. gün geri dönüş artar.
Ölçüt (14 gün): GA4 `sign_up` (utm_source=instagram), `program_enroll`, `program_day_complete` day≥7. Eşikler kampanya taslağında.

## Ölçüm (önce bunlar — ölçemediğini büyütemezsin)

- [x] **B-01 GA4 dönüşüm olayları.** `sign_up`, `practice_logged`, `share_card`, `pwa_install` olaylarını gtag ile gönder (yeni tracker yok, mevcut GA4). Sorumlu: developer. Puan 5×5/1. _✓ Sprint 2026-11-03 (dalda, deploy bekliyor)._
- [x] **B-02 `scripts/weekly_metrics.py`.** DB'den haftalık aktif pratisyen, yeni kayıt, 7. gün geri dönüş, kayıttan ilk seansa dönüşüm hesaplar. Demo hesapları hariç tutar. İlteriş sunucuda tek komutla çalıştırıp çıktıyı METRICS.md'ye yapıştırır. Sorumlu: developer. Puan 5×5/2. _✓ Sprint 2026-11-03 (dalda, deploy bekliyor)._

## Dürüstlük / güven

- [x] **B-03 Demo hesaplar — KARAR: (b).** _✓ Sprint 2026-11-04 (dalda, deploy bekliyor). Kalan içerik işi B-16'da._ _(Karar 2026-11-03'te başka bir Claude oturumu üzerinden iletildi; İlteriş teyit etsin.)_ `scripts/seed_blog.py` + `backfill_practice.py`, gerçek kişi gibi görünen 7 örnek profil (uydurma seri, kuşak, takip ve blog yazısı) oluşturuyor ve bunlar sitede "örnek" olarak etiketlenmiyor. Ziyaretçiyi yanıltır ve keşfedilirse güveni zedeler. Seçenekler: (a) profillerde ve yazılarda görünür "örnek profil" etiketi, (b) yazıları "Joryu Ekibi" yazarına taşıyıp profilleri gizlemek. Ekip önerisi: (b). Sorumlu: PO raporda sorar, developer uygular.

## Büyüme

- [x] **B-04 Instagram → site hunisi.** @joryu.art büyük izlenmeler alıyor ama GA'da Instagram'dan yalnız ~5 oturum geliyor. Bio link (`?src=ig`) + reels CTA'sı + linkin açıldığı sayfanın içerikle eşleşmesi (ör. bir jo videosu → `/kata` aiki-jo). Sorumlu: growth-marketer (taslak) → İlteriş (paylaşım). Puan 5×4/1. _✓ Taslak: docs/team/marketing/2026-11-03-instagram-hunisi.md._
- [x] **B-05 SEO anahtar kelime haritası.** _✓ Taslak 2026-11-04: docs/team/marketing/2026-11-04-seo-haritasi.md (title önerileri sonraki developer işinde uygulanacak)._ Mevcut kata/teknik/rehber sayfaları için hedef sorgu (TR+EN), rakip durumu, title/meta/H1 önerisi. Sorumlu: growth-marketer. Puan 4×4/2.
- [x] **B-06 Teknik SEO.** _✓ 2026-11-04 (f6a0cd4, dalda). Kalan: B-05 title önerileri, sitemap'e blog yazıları (B-18)._ Kata detay sayfalarında title/meta/canonical/hreflang, JSON-LD (Article/BreadcrumbList), iç linkleme (blog → kata, rehber → kata). Sorumlu: developer. Puan 4×4/2.
- [ ] **B-07 Landing hemen çıkma oranı (%66-75).** Hero'yu ziyaretçinin geldiği niyete göre bölmek, kayıt olmadan denenebilen bir "bugünün antrenmanı" demosu. Sorumlu: growth-marketer (copy) + developer. Puan 3×3/2.
- [ ] **B-08 Reddit/forum fayda gönderileri.** r/aikido, r/kendo, r/iaido için kurallara uygun, değer odaklı 3 gönderi taslağı. Sorumlu: growth-marketer → İlteriş. Puan 3×3/1.

## Elde tutma (geri gelen kullanıcı ≈ 0)

- [x] **B-09 İlk seans akışı.** _✓ Sprint 2026-11-04 (dalda, deploy bekliyor)._ Kayıttan sonra 60 saniyede ilk pratik kaydı: varsayılan branş programı, "bugün 10 dk şunu çalış" kartı. Sorumlu: PO (tasarım) + developer. Puan 4×3/3.
- [x] **B-10 Hatırlatmalar gerçekten gidiyor mu?** _✓ 2026-11-03: Resend domain doğrulanmış, mailler geliyor (başka bir Claude oturumu üzerinden iletildi; İlteriş teyit etsin)._ TODO.md'ye göre Resend domain doğrulaması (SPF/DKIM) bekliyor olabilir. Doğrulanmadıysa hatırlatma ve haftalık özet mailleri hiç gitmiyor. Sorumlu: İlteriş (10 dk kontrol). Puan 5×3/1.

## İçerik (her biri: content-writer → fact-checker → developer)

- [ ] **B-11 TODO §3b araştırma listesi:** 13 no jo kata adımları, 31 no jo bölüm dökümü, aiki-ken 2-7 suburi tanımları. Yalnız güçlü kaynakla.
- [ ] **B-12 Mevcut içerik denetimi:** _2026-11-05: jo yazısında 3 iddia denetlendi, üçü düzeltme gerektirdi → content/verified/2026-11-05-jo-yazisi-duzeltme.md (seed'e uygulanması B-19)._ guide_content.py ve blog yazılarındaki iddiaların örneklem denetimi (fact-checker, her sprint 3 iddia).
- [ ] **B-13 SEO odaklı rehber yazıları:** B-05 haritasındaki en iyi 5 sorgu için birer sayfa.

## Arama

- [ ] **B-14 Site içi arama.** `/kata?q=` üzerinden kata + teknik + rehber + blog araması; Postgres full-text (unaccent / `simple` config). Yeni servis ya da bağımlılık yok. Sorumlu: developer → qa-reviewer.

## İçerik düzeltmeleri

- [ ] **B-15 Aiki-jo happo giri girişi.** İlteriş 2026-11-04'te teyit etti: kendi jo çizgisinde happo giri yok. Fact-checker da jo için kaynak bulamadı (bokken happo giri doğrulandı). Kaynaksız iki ifade ("kuzeyden saat yönünde", "en iyi ısınma") kaldırıldı. Kalan iş: `aikijo-happo-giri` girişini (seed + guide_content aiki-jo kata listesi) tamamen kaldırmak ya da bokken girişine yönlendirmek. Seed upsert silme yapmıyor; DB satırı ve ona bağlı pratik kayıtları için güvenli bir yol gerekiyor (gizleme bayrağı ya da migration). Ayrıca 13 no jo EN özetindeki "happo-style turns" ifadesini denetle. Sorumlu: fact-checker → developer.

- [x] **B-16 Blog gövdelerinde demo kişiye ait birinci şahıs ifadeler.** Örn. jo yazısındaki "Benim için cevap basit…" cümlesi artık "Joryu Ekibi" imzasıyla tutarsız. content-writer nötrleştirir → fact-checker → developer. Seed mevcut yazıyı güncellemediği için prod satırı için tek seferlik UPDATE gerekir (İlteriş). _✓ 2026-11-04 jo yazısı (a571ef9); prod SQL İlteriş'te. Karate/taekwondo yazıları kalıyor (İlteriş kararı)._ Kapsam dışı jo iddiaları (128 cm, 20 suburi vb.) audit-log'da sonraki denetim adayı.

- [x] **B-19 Jo yazısı düzeltmelerini uygula.** _✓ 2026-11-05 (229cbe5); prod SQL İlteriş'te._ content/verified/2026-11-05-jo-yazisi-duzeltme.md (satır 45, 54, 58, 202) seed_blog.py'ye; prod için idempotent UPDATE SQL (İlteriş çalıştırır). Sorumlu: developer → qa-reviewer.

## Büyüme hamlesi (2026-11-05)

- [x] **B-20 30 günlük jo programı ücretsiz.** _✓ 2026-11-05 (4abea57, 380ce28); program metni fact-check ile düzeltildi; prod SQL İlteriş'te. Küçük not: 4. haftada ilk gün suburi 20, sonra 19 geliyor (yorumdaki sıranın tersi) — sonraki içerik turunda düzeltilebilir._ Pro kapalıyken program giriş yapan herkese açık; `/programs/30-day-jo-suburi` ziyaretçiye açık açılış sayfası + kayıt CTA'sı (`next` ile geri dönüş); gün → kata linkleri; GA4 `program_enroll`, `program_day_complete`. Sorumlu: developer → qa-reviewer.
- [ ] **B-21 Instagram 30 gün kampanyası.** Bio, 14 günlük takvim, pin yorumlar, DM şablonu, UTM. Sorumlu: growth-marketer → İlteriş.
- [ ] **B-22 Program e-posta dizisi.** Gün 1/3/7 hatırlatma; kaldığı güne link. Sorumlu: developer.
- [ ] **B-23 Hoca/dojo pilotu.** Grup + haftalık ödev + öğrenci ilerleme görünümü. Önce İlteriş'in dojosu. Sorumlu: PO (tasarım) + developer.

## Bakım

- [x] **B-17 Test izolasyonu.** _✓ 2026-11-05 (dalda; seed edilen test kullanıcıları teardown'da siliniyor, aynı DB'de 11 koşu yeşil)._ `tests/test_demo_hidden.py::test_demo_hidden_from_public_surfaces` aynı test DB'sinde ikinci koşuda düşüyor (`weekly_leaders` önceki testlerin verisini görüyor). Sorumlu: developer.
- [x] **B-18 Sitemap'e blog yazıları.** _✓ 2026-11-04 (81facbd, dalda); karate/taekwondo da dahil edildi (132e99a, İlteriş kararı)._ Sitemap blog yazılarını içermiyor; karate/taekwondo kata sayfaları da yok (İlteriş kararı bekliyor). Sorumlu: developer. Puan 4×4/1.
