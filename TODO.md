# Joryu — Yapılacaklar ve Eksikler

Son güncelleme: 2026-07-10. Durum işaretleri: 🔴 lansman engeli,
🟡 lansman sonrası ilk ay, 🟢 büyüme/iyileştirme.

## 1. Lansman engelleri (bunlar bitmeden gerçek kullanıcı alma) 🔴

- [x] **Şifre sıfırlama.** /forgot + /reset akışı: imzalı, 1 saat geçerli,
      tek kullanımlık token (parola parmak izine bağlı — tablo yok).
      Hesap var/yok bilgisi sızdırılmaz.
- [x] **E-posta altyapısı.** Resend entegre (`app/mail.py`, BackgroundTasks
      ile async). KALAN: joatolyesi.com domain'i Resend panelinde doğrulanmalı
      (DNS: SPF + DKIM kayıtları) — doğrulanana dek mailler 403 alır.
- [x] **Waitlist davetleri.** `scripts/send_invites.py` hazır: önce dry-run,
      `--yes` ile gönderir; invited_at ile çift gönderim engelli, kesintide
      kaldığı yerden devam eder. Lansman günü çalıştırılacak:
      `docker compose exec app python scripts/send_invites.py --yes`
- [x] **Yumuşak e-posta doğrulama.** Kayıtta doğrulama maili (7 gün geçerli
      token); giriş engellenmez, doğrulanana dek banner + "tekrar gönder".
      Migration 0004 (users.email_verified_at, waitlist.invited_at).
- [ ] **Prod deploy.** VPS + Caddy/Traefik (otomatik HTTPS), compose prod
      ayarları (`ENV=production` → secure cookie), joatolyesi.com DNS.
      Lemon Squeezy webhook URL'i prod domain'e tanımlanmalı, gerçek
      checkout URL'leri + webhook secret .env'e girilmeli.
- [x] **Postgres yedekleme.** `scripts/backup.sh` yazıldı (günlük cron,
      son 14 yedek); offsite kopya hâlâ manuel (ayda bir scp).
- [x] **CSRF koruması.** Double-submit cookie: tüm POST formlarında gizli
      csrf_token + `csrf_protect` dependency (webhook ve token'lı admin muaf).
- [x] **Hukuki sayfalar.** /privacy (gizlilik + KVKK aydınlatma) ve /terms,
      TR/EN, footer'lardan linkli. Waitlist modunda da erişilebilir.
- [ ] **Kata videoları.** Katalog hazır ama videolar boş. En azından
      aiki-jo + bokken setleri (senin çekimlerin) lansmanla gelmeli;
      `/admin/katas?token=...` ekranından ekleniyor.

## 2. Lansman sonrası ilk ay 🟡

- [x] **Test altyapısı.** pytest kuruldu (20 test): token/kuşak/i18n saf
      testleri + auth, CSRF, reset, oturum düşürme, doğrulama, hesap silme,
      streak, waitlist uçtan uca akışları. Çalıştırma: tests/conftest.py
      başındaki komutla test Postgres'i aç, `pytest`. Eksik: Pro kapıları
      ve webhook uçtan uca testi.
- [x] **Hata izleme.** Sentry entegre — SENTRY_DSN boşsa devre dışı.
      KALAN: sentry.io'da proje aç, DSN'i prod .env'e ekle.
- [ ] **Program günlerine video ekleme.** Admin ekranı şimdilik sadece
      kata videoları; program günleri için aynı ekran genişletilmeli.
- [ ] **İkinci program.** Tek program var (30 gün jo suburi). Bokken
      (nana suburi) programı doğal ikinci ürün; kendo/iaido sonra.
- [ ] **Kullanıcı saat dilimi.** Streak UTC+1 gün toleransıyla çalışıyor;
      doğrusu kayıtta/profilde timezone saklamak.
- [x] **Session iptali + parola değiştirme.** Oturum token'ı parola parmak
      izi taşıyor: şifre değişince (reset dahil) diğer cihazlardaki oturumlar
      otomatik düşer. Profil sayfasında "Şifre değiştir" bölümü var.
      NOT: deploy edildiğinde mevcut tüm oturumlar bir kez düşer (format değişti).
- [x] **Hesap silme.** Profil sayfasında şifre onaylı "Hesabı sil" (danger
      zone); tüm veriler cascade ile silinir, KVKK metninde belirtildi.
- [ ] **Admin ekranlarını birleştir.** /admin/waitlist (CSV) + /admin/katas
      tek panel altında; token yerine admin hesabı düşünülebilir.
- [ ] **Performans.** Google Fonts + unpkg CDN render-blocking; font ve
      htmx/alpine self-host edilirse Lighthouse mobil hedefi (90+) garantiye
      alınır. (GA zaten async.)
- [ ] **PWA offline sayfası.** SW statikleri cache'liyor ama sayfa offline
      açılırsa çıplak hata veriyor; basit bir offline.html iyi olur.

## 3. Ürünü gerçekten kullandıracak özellikler (önerilerim) 🟢

Sıralama: etki/emek oranına göre. İlk üçü bence kritik.

- [x] **1. Günlük hatırlatma (e-posta + PWA push).** Yapıldı:
      `scripts/send_reminders.py` — o gün pratik kaydetmemiş kullanıcılara
      hem e-posta (opt-in: reminders_enabled) hem push bildirimi (opt-in:
      dashboard'daki "Bildirimleri aç" butonu) gönderir. VAPID web push
      (migration 0009: push_subscriptions), `app/push.py` + `scripts/
      generate_vapid_keys.py`. Geçersiz abonelikler (404/410) otomatik
      silinir. KALAN: sunucuda VAPID anahtarı üretip .env'e eklemek.
- [x] **2. Paylaşılabilir profil kartı (OG görseli).** Yapıldı:
      `/u/<kullanıcı>/card.png` — Pillow ile sunucuda çizilen 1200×630 PNG
      (isim, branş, seri, toplam gün, kuşak bandı, 12 haftalık ısı haritası).
      Profil sayfasında og:image + twitter:card meta'ları; link WhatsApp/
      Twitter'a yapıştırılınca kart görünür. Sadece herkese açık profiller.
- [x] **3. YouTube → uygulama köprüsü (teknik taraf).** Kata listesi ve
      ücretsiz kata sayfaları artık login'siz açılıyor (Pro içerik girişsizde
      login'e yönlenir); girişsiz ziyaretçiye kayıt CTA'sı gösterilir.
      KALAN: video açıklamalarına linkleri koymak (senin işin, lansmanla).
- [x] **4. Seri dondurma hakkı.** Yapıldı: ayda 2 tek-günlük boşluk otomatik
      köprülenir (`app/stats.py::_streak_with_freezes`), tablo gerekmez —
      hesap tamamen deterministik. Dashboard'da "Bu ayki donma hakkın: X/2"
      göstergesi + tooltip.
- [x] **5. Kilometre taşı rozetleri → kuşak sistemi.** Yapıldı:
      `app/badges.py` — seriye bağlı 7 kuşak (beyaz 7g → siyah 365g, tüm
      zamanların en uzun serisine bakar, SVG + hover/tooltip) + seans
      rozetleri (1/25/100/300). Dashboard'da tümü (kilitliler silüet),
      herkese açık profilde sadece kazanılanlar. Anlık hesaplanır, tablo yok.
      Kalan: siyah kuşak sonrası **dan dereceleri** (1-10. dan; landing'de
      vaat edildi) + kuşakların paylaşım kartına işlenmesi (madde 2 ile).
- [x] **6. Takip + basit akış.** Yapıldı: herkese açık profillerde
      "Takip et" butonu (toggle), takipçi sayısı; dashboard'da "Takip
      ettiklerin" kartı son 15 pratiği gösterir. Yorum/beğeni bilinçli yok.
      Migration 0005 (follows).
- [x] **7. Kata çalışma modu.** Kata sayfasında "Bugün bunu çalıştım" +
      dakika alanı: tek tuşla pratik kaydı. **Tekrar sayacı eklendi:**
      practice_logs.kata_slug (migration 0009) ile "bunu N kez çalıştın"
      göstergesi — kişisel süreklilik motivasyonu.
- [x] **8. Haftalık özet (v1 — dashboard kartı).** "Bu hafta: X gün, Y dk,
      odak branş" + geçen haftayla kıyas. E-posta versiyonu sonra.
- [x] **9. PWA kısayolu.** Manifest shortcuts: "Pratik kaydet" (/app) ve
      "Kata" (/kata).
- [x] **11. Branş rehberi (/guide).** 10 branş için kata + teknik/vuruş
      sınıflandırması; TR detaylı, EN özet; embusen/happo/seviye SVG
      diyagramları. Giriş istemez ama WAITLIST_ONLY=true iken kapalıdır
      (lansmanla açılır). Kata'sı olmayan branşlarda (aikido, kenjutsu
      kısmen) yalnız teknikler. Her branşa **"İpuçları"** bölümü eklendi
      (ekipman bakımı, yaygın hatalar, güvenlik — genel/doğrulanabilir
      bilgi, teknik-özgü iddia değil). İçerik `app/guide_content.py` —
      düzeltme/ekleme oradan.
- [x] **15. Kata kütüphanesi: Kata / Vuruşlar ayrımı.** `katas.kind`
      kolonu (migration 0008) ile /kata sayfası branş seçilince iki ayrı
      sekmede gösteriyor: Kata (form/poomsae) ve Vuruşlar/Teknikler
      (suburi/kihon/duruş/tekme). 200 girişe çıkarıldı — tüm branşların
      kata VE tekniklerini kapsıyor (aikido hariç: gerçekten kata'sı yok,
      boş sekmede dürüst mesaj + teknik sekmesine yönlendirme). Video
      YouTube linki kabul ediyor (senin çekimin ya da başkasının videosu
      olabilir — `/admin/katas` normalize ediyor); video yoksa yazılı
      açıklama zaten var. `app/seed.py` artık katalogdan çıkarılan eski
      satırları otomatik temizliyor (upsert-only'nin bıraktığı öksüz
      kayıtlar sorunu çözüldü).
- [x] **13. Topluluk blogu.** Yapıldı: yazma girişli (/blog/yeni), okuma
      ve keşfet (/blog) herkese açık; başlık+metin araması, branş filtresi,
      düzenleme/silme (sadece sahibi), yazar → profil linki, og meta
      (sanitize edilmiş özetten). **Markdown editörü**: araç çubuğu
      (kalın/italik/başlık/liste/alıntı/link, Ctrl+B/I kısayolları),
      gövde `markdown` + `nh3` ile render + XSS temizliği. Migration 0006.
      Başlangıç içeriği: `scripts/seed_blog.py` (3 örnek kullanıcı, "Jo
      Nedir?" ve "Dachi Pozisyonları" yazıları — idempotent, tekrar
      çalıştırılabilir).
- [x] **14. Haftanın enleri.** `/practitioners` sayfasında branş başına bu
      hafta en çok dakika yapan (herkese açık profil) — `weekly_leaders()`,
      tablo gerekmez, haftalık pencere pazartesi başlangıçlı hesaplanır.
- [x] **12. Rehber EN derinleştirme.** Kalan tek TR-only adım listesi
      (Taikyoku Shodan) İngilizce'ye çevrildi; rehberde EN açığı kalmadı.
      (Araştırma listesinden gelecek yeni içerikler iki dilde eklenmeli.)
- [x] **16. Waitlist referans linki.** Her kayıt kendi davet linkini
      (`?ref=<kod>`) ve sıra numarasını görüyor; kimin kimi getirdiği
      `referred_by` ile CSV'de izlenebiliyor (migration 0009). Klasik
      waitlist büyütme mekaniği — detay: WAITLIST_GROWTH.md.
      KALAN (istenirse): "3 davet = X sıra yukarı" gibi somut bir ödül.
- [x] **17. En uzun seri gösterimi.** `compute_longest_streak` zaten
      vardı ama hiçbir yerde gösterilmiyordu; artık dashboard'da (güncel
      seriden düşükse "Kişisel rekorun: X gün") ve herkese açık profilde
      ayrı bir stat olarak görünüyor.
- [x] **20. Paylaşım/push düzeltmeleri (kullanıcı geri bildirimi sonrası).**
      (a) Push "hiçbir şey olmuyor" hatası: kök sebep VAPID anahtarlarının
      hiç üretilmemiş olmasıydı (`/push/vapid-public-key` boş dönüyordu,
      JS sessizce hiçbir şey yapmıyordu) — lokal `.env`'e anahtar üretip
      eklendi, ayrıca push.js artık her adımda görünür durum mesajı
      veriyor (izin reddi, yapılandırma eksikliği, tarayıcı desteği yok
      vb. — asla sessiz kalmıyor).
      (b) Paylaş butonları text-pill'den ikon butona (paylaş + indir,
      site genelinde tek görünüm, `_share_controls.html` partial'ı)
      geçirildi — hem profil hem dashboard'da kullanılıyor.
      (c) Kart görselindeki (card.png) kuşak artık düz bant değil, gerçek
      kuşak şekli (bant + düğüm + sarkan uçlar — sitedeki SVG ile aynı
      oran), `app/card.py::_draw_belt`.
      (d) "Takip ettiklerin" akışı dashboard'un altından kaldırılıp
      `/practitioners` (topluluk) sayfasına taşındı — bağlamsal olarak
      oraya ait. Profil sayfasına gerçek **Takipçiler / Takip Edilenler**
      bölümü eklendi (avatar listeleri, tıklanabilir).
- [x] **19. Avatar + paylaşım.** Yüklemesiz avatar (`app/avatar.py`):
      enso halkası (kuşak rengiyle boyanır) + baş harf monogramı, her
      kullanıcı için deterministik açıda döner. `/u/<kullanıcı>/avatar.png`
      (herkese açık profilde). Profil kartına (`card.png`) gömüldü.
      Paylaşım widget'ı (dashboard + profil): Web Share API (mobilde
      görsel dahil native paylaşım) + masaüstü fallback (X/WhatsApp/
      İndir linkleri). CJK font riski nedeniyle kanji yerine monogram
      tercih edildi (prod Docker imajında yalnız DejaVu var).
- [x] **18. Dil kalitesi denetimi.** strings.py baştan sona tarandı;
      TR/EN anahtar paritesi zaten testle garanti (test_langs_have_same_keys).
      Bulunan 3 gerçek pürüz düzeltildi: TR'de devrik "Branş branş" tekrarı,
      iki dilde de eksik "video" kelimesi (kata_title), EN'de Türkçe'den
      birebir çevrilmiş "Freeze rights" ifadesi.

## 3b. Rehber araştırma listesi (İlteriş doğrulayıp ekleyecek) 📋

Doğruluk kuralı gereği emin olunmayan içerik rehbere YAZILMADI; sayfada
"doğrulanıyor" notu görünüyor. Doğrulanınca `app/guide_content.py`'ye
eklenecekler:

- [ ] **13 no jo kata — adım adım liste.** Iwama saito çizgisindeki
      standart 13 hareketin sırası ve adları.
- [ ] **31 no jo kata — bölüm dökümü.** Hangi hareketler hangi bölümde;
      yaygın öğretimdeki bölüm sınırları.
- [ ] **Aiki-ken 2-7. suburi tanımları.** Her birinin kesin tarifi
      (şu an sadece ichi no suburi detaylı, kalanı videoya yönlendiriyor).
- [ ] **Taegeuk hareket sayıları.** Kaynaklar çelişiyor; Kukkiwon resmi
      sayıları teyit edilirse geri eklenebilir.
- [ ] Genel: her branşın tekniklerini o branştan bir hocaya okutup
      onay almak (özellikle kendo/iaido/karate bölümleri).
- [ ] **10. TR yerel fiyatlandırma.** Billing'de ₺59/ay yazıyor ama Lemon
      Squeezy'de TR fiyatlı ayrı varyant tanımlanmalı.

## 4. Bilinen küçük işler / teknik borç

- [ ] `schemas.py` silindi; form doğrulama el yazması regex'lerle —
      e-posta/username doğrulaması tek modüle toplanabilir.
- [ ] `deps.py` PRO_STATUSES "paused/unpaid" durumlarını Pro saymıyor —
      LS panelindeki dunning ayarlarıyla birlikte gözden geçir.
- [ ] Heatmap 112 hücre, `tabindex` sadece dolu hücrelerde — erişilebilirlik
      taraması yapılmadı (kontrast oranları dahil).
- [ ] `alembic upgrade head` her container açılışında çalışıyor — çoklu
      replica olursa migration lock/tek seferlik job'a taşınmalı.
- [ ] Rate limit in-memory — tek instance için yeterli, ölçeklenirse Redis.
- [ ] Kata kataloğu açıklamaları kısa; adım adım anlatım + görsel dizilim
      (özellikle 31 no jo) içerik olarak eklenebilir.

## 5. Bilinçli olarak yapılmayanlar (kapsam dışı — BRIEF §Phase 1)

Native app (PWA yeter), tek seferlik program satışı (abonelik oturunca),
ekipman affiliate sayfaları, blog/SEO çalışması, çoklu admin/rol sistemi,
yorum-beğeni gibi ağır sosyal özellikler.
