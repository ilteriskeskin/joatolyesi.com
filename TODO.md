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

- [ ] **1. Günlük hatırlatma (push/e-posta).** Streak ürünün çekirdeği ama
      hatırlatma olmadan streak ölür. PWA push (VAPID, ücretsiz) veya
      günlük e-posta: "Serin 12 günde — bugün 15 dakika yeter." Alışkanlık
      uygulamalarında elde tutmanın 1 numaralı kaldıracı bu.
- [ ] **2. Paylaşılabilir profil kartı (OG görseli).** Profil sayfası için
      otomatik üretilen görsel: isim + branş + seri + ısı haritası.
      Instagram bio/story'de paylaşılınca organik büyüme sağlar — senin
      dağıtım avantajın (138k izlenmeli videolar) ile birebir örtüşüyor.
      "Dövüş sanatçısının GitHub profili" konumlandırmasının vitrini.
- [ ] **3. YouTube → uygulama köprüsü.** Her videonun açıklamasına ilgili
      kata sayfası linki (`joatolyesi.com/kata/...?src=yt`). Kata sayfaları
      giriş istemeden önizlenebilir olmalı (şu an login istiyor — ücretsiz
      içerik herkese açık olsun, SEO da kazanılır). Dönüşüm hunisinin
      en ucuz parçası.
- [ ] **4. Seri dondurma hakkı.** Ayda 1-2 "donma" hakkı (hastalık, seyahat).
      Seriyi kaybetmek bırakmanın en büyük sebebi; affetme mekanizması
      elde tutmayı ciddi artırır (Duolingo etkisi).
- [x] **5. Kilometre taşı rozetleri → kuşak sistemi.** Yapıldı:
      `app/badges.py` — seriye bağlı 7 kuşak (beyaz 7g → siyah 365g, tüm
      zamanların en uzun serisine bakar, SVG + hover/tooltip) + seans
      rozetleri (1/25/100/300). Dashboard'da tümü (kilitliler silüet),
      herkese açık profilde sadece kazanılanlar. Anlık hesaplanır, tablo yok.
      Kalan: siyah kuşak sonrası **dan dereceleri** (1-10. dan; landing'de
      vaat edildi) + kuşakların paylaşım kartına işlenmesi (madde 2 ile).
- [ ] **6. Takip + basit akış.** Toplulukta kişileri takip et; "bugün kim
      ne çalıştı" akışı. Sosyal baskı = düzenlilik. (Yorum/beğeni değil,
      sadece görünürlük — basit tut.)
- [x] **7. Kata çalışma modu (v1).** Kata sayfasında "Bugün bunu çalıştım"
      + dakika alanı: tek tuşla pratik kaydı, not olarak kata adı düşer.
      Kalan: tekrar sayacı.
- [x] **8. Haftalık özet (v1 — dashboard kartı).** "Bu hafta: X gün, Y dk,
      odak branş" + geçen haftayla kıyas. E-posta versiyonu sonra.
- [x] **9. PWA kısayolu.** Manifest shortcuts: "Pratik kaydet" (/app) ve
      "Kata" (/kata).
- [x] **11. Branş rehberi (/guide).** 10 branş için kata + teknik/vuruş
      sınıflandırması; TR detaylı, EN özet; embusen/happo/seviye SVG
      diyagramları. Giriş istemez ama WAITLIST_ONLY=true iken kapalıdır
      (lansmanla açılır). Kata'sı olmayan
      branşlarda (aikido, kenjutsu kısmen) yalnız teknikler. İçerik
      `app/guide_content.py` — düzeltme/ekleme oradan.
- [ ] **12. Rehber EN derinleştirme.** Rehberin adım listeleri şimdilik
      yalnız TR; EN kullanıcılar TR listeyi görüyor.

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
