# Aktif Sprint — 2026-11-04

Dal: `team/sprint-2026-11-04` (main'den; 2026-11-03 dalı merge edilmiş) · Otomatik, gözetimsiz koşu.
Push/deploy/prod erişimi yok, `.env` okunmaz, kod bu belgede yazılmaz (uygulama developer'da).

## Hedef (tek cümle)

Sitede kamuya açık hiçbir yerde gerçek kişi gibi görünen uydurma profil/seri/takip kalmasın; demo yazılar "Joryu Ekibi" imzasıyla yayında kalsın.

## Kısa teşhis

- İlteriş kararı (BACKLOG): sıradaki sprint B-03 (b) + B-09. **Kullanım tasarrufu için bu sprintte yalnız B-03 (b)**; B-09 sonraki sprintin ilk işi.
- 2026-11-03 raporu: B-01/B-02/B-04 QA'dan geçti, deploy bekliyor. Yeni rakam yok; metrik kararı yine ölçüm sonrası.
- Sızıntı kaynağı: `seed_blog.py` 7 demo kullanıcı (`@demo.joatolyesi.com`, `is_public=True`) + `backfill_practice.py` `DEMO_STREAKS` (8-400 günlük sahte seri, sahte kuşak) + `FOLLOW_CHAIN` (sahte takip). Görünür yerler: `/practitioners` (liste, "haftanın enleri", takip akışı), `/u/<username>` (+ `/card`, `/avatar.png`, takip POST'u, takipçi/takip listeleri), `/blog` ve `/blog/<slug>` yazar satırı + link.
- Demo e-posta soneki iki yerde ayrı yazılı (`seed_blog.py` f-string, `weekly_metrics.py::DEMO_EMAIL_SUFFIX`); tek sabite bağlanmalı.
- Global (kullanıcıdan bağımsız) sayaç yok (`stats.py` sorguları kullanıcı bazlı); sitemap profil içermiyor. Yani gizlenecek yer yukarıdakilerle sınırlı.
- Şema: Alembic var (`alembic/versions`, son `0011_rest_day`; `CMD` her açılışta `alembic upgrade head`). **Bu işte şema değişikliği gerekmiyor.**

## Seçilen yaklaşım (şema değişikliksiz, silmesiz, prod komutsuz)

1. **Tek ortak sabit:** `app/constants.py` içine `DEMO_EMAIL_SUFFIX = "@demo.joatolyesi.com"` ve SQLAlchemy yardımcısı `demo_user_clause()` (`lower(User.email) LIKE '%suffix'`) + Jinja/Python tarafı için `is_demo_user(user)`. `weekly_metrics.py` ve `seed_blog.py` buradan import eder (OWNER_EMAIL ile aynı kalıp). `weekly_metrics.py`'deki yerel tanım kaldırılır, mevcut test import'u bozulmasın diye aynı isim yeniden dışa aktarılır.
2. **Gizleme = sorgu seviyesinde filtre** (mevcut prod satırları için bayrak/komut gerekmez, deploy ile anında etkili, idempotent, hiçbir satır silinmez/değişmez). `User.is_public` kontrolü olan her yere `~demo_user_clause()` eklenir; tek yerde `public_user_clause()` (= `is_public AND username IS NOT NULL AND NOT demo`) olarak toplanır.
3. **"Joryu Ekibi" = gösterim katmanında**, ayrı sistem kullanıcısı yok. Gerekçe: ekip kullanıcısı `is_public` filtrelerine takılır/yeni satır ister, yazı `user_id` taşımak veri yazmayı gerektirir. `blog_list.html` / `blog_post.html` içinde yazar demo ise: etiket `t.blog_team_author` ("Joryu Ekibi" TR/EN, `app/i18n/strings.py`), avatar ve `/u/...` linki yok. Yazı sahibi demo kullanıcı giriş yapamadığı için düzenle/sil zaten erişilemez. Not: sahip hesabı `joryu`'nun aiki-jo yazısı gerçek hesaptır, etkilenmez.
4. **Seed tekrar çalışınca:** `seed_blog.py` demo kullanıcıları `is_public=False` ile oluşturur (FK sahibi olarak gerekli); `backfill_practice.py`'den `DEMO_STREAKS`, `FOLLOW_CHAIN` ve ilgili döngüler **tamamen kaldırılır** (sahip hesabı backfill'i kalır). Böylece script'i yeniden çalıştırmak sahte aktivite üretmez. Prod'daki mevcut sahte `practice_logs`/`follows` satırları silinmez; hiçbir public yüzde görünmezler, metrik script'i zaten demo'yu hariç tutar.

## İş — B-03 (b): Demo profilleri gizle, yazıları "Joryu Ekibi"ne taşı

**Sorumlu:** `developer` → `qa-reviewer`

**Değişecek dosyalar:** `app/constants.py`, `app/stats.py` (`weekly_leaders`), `app/routers/profile.py` (liste, takip akışı, public profil, card, avatar, takip, takipçi/takip listeleri), `app/routers/blog.py` (gerekirse yazar bilgisini şablona hazırlama), `app/templates/blog_list.html`, `app/templates/blog_post.html`, `app/i18n/strings.py`, `scripts/seed_blog.py`, `scripts/backfill_practice.py`, `scripts/weekly_metrics.py`, `tests/` (yeni `tests/test_demo_hidden.py` ya da `test_flows.py`'ye ekleme).

**Kabul kriterleri:**
1. Demo kullanıcı `/practitioners` listesinde (arama dahil) görünmüyor; "haftanın enleri"nde ve takip akışında yok.
2. `/u/<demo-username>`, `/u/<demo>/card`, `/u/<demo>/avatar.png` 404; demo'yu takip etme POST'u reddediliyor; gerçek kullanıcının takipçi/takip listelerinde demo çıkmıyor.
3. Demo yazarlı blog yazısı `/blog` ve `/blog/<slug>`'da "Joryu Ekibi" ile gösteriliyor; demo `display_name`/`username` HTML'de geçmiyor; yazar linki ve avatar yok. Sahip hesabı `joryu` yazısı eskisi gibi.
4. **Testler:** en az 1 test demo kullanıcının practitioners + liderlik + public profilde görünmediğini, 1 test blog yazısının "Joryu Ekibi" ile gösterildiğini doğrular; gerçek is_public kullanıcı hâlâ görünür (karşı-test). Mevcut testler geçer (`test_weekly_metrics` dahil). Test Postgres'i yoksa açıkça raporla.
5. `DEMO_EMAIL_SUFFIX` repo genelinde tek tanım (`grep` ile doğrulanır; `seed_blog.py` ve `weekly_metrics.py` import eder).
6. `backfill_practice.py` içinde demo seri/takip üreten kod yok; script yalnız sahip hesabını doldurur. Hiçbir script/migration silme yapmaz.
7. Şema/Alembic değişikliği yok (diff'te `alembic/versions` boş).

**Sunucu etkisi:** ihmal edilebilir (mevcut sorgulara bir LIKE koşulu; 512 MB / 1 vCPU'yu etkilemez). **Emek:** ~1,5-2 saat.
**Ölçülecek metrik:** doğrudan büyüme metriği değil, güven/dürüstlük işi. Doğrulama: deploy sonrası `/practitioners` ve 7 demo `/u/...` URL'sinin 404/gizli olması. Dolaylı: `weekly_metrics.py` "hariç tutulan demo" sayısı 7 kalır, gerçek kullanıcı sayıları değişmez.

## Teşhis: blog gövdelerinde uydurma deneyim iddiası

- `seed_blog.py` yazı gövdeleri çoğunlukla bilgi/talimat dilinde ve ekip sesiyle ("öneririz"). **Birinci tekil şahıs deneyim iddiası yalnız bir yerde:** "Jo Nedir?" yazısında "Benim için cevap basit: jo affedicidir…" (kenshin-yolda). "Joryu Ekibi" imzası altında tek kişi anlatıcı sesi yanıltıcı; tek cümlelik nötrleştirme gerekir.
- Yazarlara bağlı uydurma deneyim iddiaları (bio: "İki yıldır her sabah jo…", "Aiki-ken çalışıyorum") yalnız gizlenen profillerde; gizleme sonrası görünmez. Seed'deki bio metinleri yeni DB'ye yazılmaya devam eder ama görünmez; temizlik gerekmez.
- Karate ve taekwondo yazıları (dachi, poomsae) ürün kapsamı dışı (BRIEF) ve `/blog` listesinde hâlâ yayında. Kapsam kararı İlteriş'te.
- Bu sprintte içerik değiştirilmez (içerik işi: content-writer → fact-checker). Sonraki işe bırakılan liste: (a) "Benim için…" cümlesinin ekip sesine çevrilmesi; (b) prod'daki yazı satırı güncellenmeli (seed yalnız başlık yoksa ekler, mevcut satırı güncellemez) → tek seferlik güvenli UPDATE; (c) B-12 kapsamında ZNKR 1968 / "on iki kata" gibi iddiaların denetimi.

## Raporda İlteriş'e sorulacaklar

1. **Prod'da çalıştırılacak komut yok.** Deploy yeterli (filtre sorgu seviyesinde). Teyit: demo satırları ve sahte seri verileri silinmeden kalsın mı, yoksa ileride tek seferlik temizlik ister misin?
2. Karate/taekwondo blog yazıları yayında kalsın mı, gizlensin mi?
3. "Benim için cevap basit" cümlesi ekip sesine çevrilsin mi (kısa içerik işi, sonraki sprint)?
4. B-03 kararı (b)'yi teyit et (başka oturumdan iletilmişti).
5. Hâlâ bekleyenler: 2026-11-03 dalını merge/deploy, GA4 key event, `weekly_metrics.py` ilk çalıştırma, Instagram bio linki.

## Sonraki sprint

B-09 ilk seans akışı (ilk iş), ardından B-05/B-06 ya da B-15.
