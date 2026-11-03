# Backlog

PO önceliklendirir. Puan = (Etki × Güven) / Emek, her biri 1-5. Yeni fikir
eklenebilir; tamamlanan iş `[x]` ile işaretlenip rapora bağlanır.

## Sıradaki sprint (İlteriş kararı, 2026-11-04)

**B-03 (b)** + **B-09 ilk seans akışı**. Gerekçe: bio linki değiştirildi, Instagram trafiği geliyor; kayıt olanın ilk gün seans kaydetmesi şu an en kritik sızıntı. PO bu ikisini seçsin.

## Ölçüm (önce bunlar — ölçemediğini büyütemezsin)

- [x] **B-01 GA4 dönüşüm olayları.** `sign_up`, `practice_logged`, `share_card`, `pwa_install` olaylarını gtag ile gönder (yeni tracker yok, mevcut GA4). Sorumlu: developer. Puan 5×5/1. _✓ Sprint 2026-11-03 (dalda, deploy bekliyor)._
- [x] **B-02 `scripts/weekly_metrics.py`.** DB'den haftalık aktif pratisyen, yeni kayıt, 7. gün geri dönüş, kayıttan ilk seansa dönüşüm hesaplar. Demo hesapları hariç tutar. İlteriş sunucuda tek komutla çalıştırıp çıktıyı METRICS.md'ye yapıştırır. Sorumlu: developer. Puan 5×5/2. _✓ Sprint 2026-11-03 (dalda, deploy bekliyor)._

## Dürüstlük / güven

- [ ] **B-03 Demo hesaplar — KARAR: (b), SONRAKİ SPRİNTİN İLK İŞİ.** _(Karar 2026-11-03'te başka bir Claude oturumu üzerinden iletildi; İlteriş teyit etsin.)_ `scripts/seed_blog.py` + `backfill_practice.py`, gerçek kişi gibi görünen 7 örnek profil (uydurma seri, kuşak, takip ve blog yazısı) oluşturuyor ve bunlar sitede "örnek" olarak etiketlenmiyor. Ziyaretçiyi yanıltır ve keşfedilirse güveni zedeler. Seçenekler: (a) profillerde ve yazılarda görünür "örnek profil" etiketi, (b) yazıları "Joryu Ekibi" yazarına taşıyıp profilleri gizlemek. Ekip önerisi: (b). Sorumlu: PO raporda sorar, developer uygular.

## Büyüme

- [x] **B-04 Instagram → site hunisi.** @joryu.art büyük izlenmeler alıyor ama GA'da Instagram'dan yalnız ~5 oturum geliyor. Bio link (`?src=ig`) + reels CTA'sı + linkin açıldığı sayfanın içerikle eşleşmesi (ör. bir jo videosu → `/kata` aiki-jo). Sorumlu: growth-marketer (taslak) → İlteriş (paylaşım). Puan 5×4/1. _✓ Taslak: docs/team/marketing/2026-11-03-instagram-hunisi.md._
- [ ] **B-05 SEO anahtar kelime haritası.** Mevcut kata/teknik/rehber sayfaları için hedef sorgu (TR+EN), rakip durumu, title/meta/H1 önerisi. Sorumlu: growth-marketer. Puan 4×4/2.
- [ ] **B-06 Teknik SEO.** Kata detay sayfalarında title/meta/canonical/hreflang, JSON-LD (Article/BreadcrumbList), iç linkleme (blog → kata, rehber → kata). Sorumlu: developer. Puan 4×4/2.
- [ ] **B-07 Landing hemen çıkma oranı (%66-75).** Hero'yu ziyaretçinin geldiği niyete göre bölmek, kayıt olmadan denenebilen bir "bugünün antrenmanı" demosu. Sorumlu: growth-marketer (copy) + developer. Puan 3×3/2.
- [ ] **B-08 Reddit/forum fayda gönderileri.** r/aikido, r/kendo, r/iaido için kurallara uygun, değer odaklı 3 gönderi taslağı. Sorumlu: growth-marketer → İlteriş. Puan 3×3/1.

## Elde tutma (geri gelen kullanıcı ≈ 0)

- [ ] **B-09 İlk seans akışı.** Kayıttan sonra 60 saniyede ilk pratik kaydı: varsayılan branş programı, "bugün 10 dk şunu çalış" kartı. Sorumlu: PO (tasarım) + developer. Puan 4×3/3.
- [x] **B-10 Hatırlatmalar gerçekten gidiyor mu?** _✓ 2026-11-03: Resend domain doğrulanmış, mailler geliyor (başka bir Claude oturumu üzerinden iletildi; İlteriş teyit etsin)._ TODO.md'ye göre Resend domain doğrulaması (SPF/DKIM) bekliyor olabilir. Doğrulanmadıysa hatırlatma ve haftalık özet mailleri hiç gitmiyor. Sorumlu: İlteriş (10 dk kontrol). Puan 5×3/1.

## İçerik (her biri: content-writer → fact-checker → developer)

- [ ] **B-11 TODO §3b araştırma listesi:** 13 no jo kata adımları, 31 no jo bölüm dökümü, aiki-ken 2-7 suburi tanımları. Yalnız güçlü kaynakla.
- [ ] **B-12 Mevcut içerik denetimi:** guide_content.py ve blog yazılarındaki iddiaların örneklem denetimi (fact-checker, her sprint 3 iddia).
- [ ] **B-13 SEO odaklı rehber yazıları:** B-05 haritasındaki en iyi 5 sorgu için birer sayfa.

## Arama

- [ ] **B-14 Site içi arama.** `/kata?q=` üzerinden kata + teknik + rehber + blog araması; Postgres full-text (unaccent / `simple` config). Yeni servis ya da bağımlılık yok. Sorumlu: developer → qa-reviewer.

## İçerik düzeltmeleri

- [ ] **B-15 Aiki-jo happo giri girişi.** İlteriş 2026-11-04'te teyit etti: kendi jo çizgisinde happo giri yok. Fact-checker da jo için kaynak bulamadı (bokken happo giri doğrulandı). Kaynaksız iki ifade ("kuzeyden saat yönünde", "en iyi ısınma") kaldırıldı. Kalan iş: `aikijo-happo-giri` girişini (seed + guide_content aiki-jo kata listesi) tamamen kaldırmak ya da bokken girişine yönlendirmek. Seed upsert silme yapmıyor; DB satırı ve ona bağlı pratik kayıtları için güvenli bir yol gerekiyor (gizleme bayrağı ya da migration). Ayrıca 13 no jo EN özetindeki "happo-style turns" ifadesini denetle. Sorumlu: fact-checker → developer.
