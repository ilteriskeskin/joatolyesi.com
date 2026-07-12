# Joryu — Lansman Öncesi Manuel Test Checklist'i

Bu doküman, `WAITLIST_ONLY=false` yapıp uygulamayı gerçek kullanıcılara
açmadan önce **senin elinle** tek tek denemen gereken her akışı listeler.
Otomatik testler (33 pytest) kodun bozulmadığını garanti eder ama "gerçekten
kullanışlı mı, güzel mi görünüyor mu" sorusunu yalnızca sen cevaplayabilirsin.

Nasıl çalıştırılır: LAUNCH.md'deki adımlarla lokal ortamı ayağa kaldır
(`docker compose up -d --build`, `WAITLIST_ONLY=false`) ve aşağıdaki
listeyi yukarıdan aşağı, gerçekten tıklayarak geç. Telefon ve masaüstünde
ayrı ayrı dene — bazı maddeler özellikle telefon için işaretli.

---

## A. Hesap ve giriş

- [ ] Kayıt ol (`/register`): geçerli e-posta + 8+ karakter şifre + kullanıcı
      adı + branş seç → hesap oluşuyor mu, otomatik giriş yapıyor mu
- [ ] Kayıt: kısa şifre, geçersiz kullanıcı adı, alınmış kullanıcı adı
      hata mesajları doğru dilde ve anlaşılır mı
- [ ] Çıkış yap, tekrar giriş yap (`/login`) — doğru/yanlış şifre ile dene
- [ ] **Şifremi unuttum** (`/forgot`): mail gerçekten geliyor mu (Resend
      doğrulanmış olmalı), linke tıklayınca yeni şifre belirlenebiliyor mu
- [ ] Şifre sıfırlama linkini **ikinci kez** kullanmayı dene — reddedilmeli
- [ ] Profilde **şifre değiştir** — değiştirdikten sonra eski cihazda/
      tarayıcıda oturumun düştüğünü doğrula (başka bir tarayıcıda dene)
- [ ] **E-posta doğrulama**: kayıt sonrası mail geldi mi, üstteki "doğrula"
      şeridi görünüyor mu, linke tıklayınca şerit kayboluyor mu
- [ ] "Tekrar gönder" butonunu dene
- [ ] Profilde **hesabı sil** — şifre onayı istiyor mu, gerçekten siliniyor mu

## B. Pratik takibi (uygulamanın kalbi)

- [ ] Dashboard'da bugünün tarihiyle pratik kaydet — seri 1'e çıkıyor mu
- [ ] Dünün tarihiyle bir kayıt daha ekle — seri 2'ye çıkıyor mu
- [ ] Isı haritası (aktivite ızgarası) doğru günleri renklendiriyor mu
- [ ] **Haftalık özet kartı**: gün/dakika/odak branş doğru hesaplanıyor mu,
      geçen haftayla kıyas mantıklı mı
- [ ] Bir gün atla (kayıt yapma), ertesi gün tekrar kaydet — seri donma
      hakkıyla köprüleniyor mu ("Bu ayki donma hakkın: 1/2" görünmeli)
- [ ] Ayda 2'den fazla boşluk bırakıp serinin gerçekten sıfırlandığını gör
- [ ] **En uzun seri**: güncel seri rekordan düşükse "Kişisel rekorun"
      notu görünüyor mu

## C. Kuşaklar ve rozetler

- [ ] Sıfır pratikle beyaz kuşak görünüyor mu (herkes buradan başlar)
- [ ] Birkaç gün pratik ekleyip bir sonraki kuşağa (sarı, 30 gün) geçişi
      gözlemle — ilerlemesi mantıklı mı
- [ ] Kilitli kuşaklar üzerine gelince tooltip doğru mesajı gösteriyor mu
      ("Toplam X pratik gününde açılır")
- [ ] Seans rozetleri (İlk Seans, 25/100/300) doğru tetikleniyor mu
- [ ] Herkese açık profilde **sadece kazanılan** kuşak/rozetler görünüyor mu
      (dashboard'da tümü, profilde sadece kazanılanlar olmalı)

## D. Kata kütüphanesi

- [ ] `/kata` sayfası girişsiz açılıyor mu (login istemiyor olmalı)
- [ ] Bir branş seç — **Kata** ve **Vuruşlar/Teknikler** sekmeleri ayrı
      ayrı doğru içerikleri gösteriyor mu
- [ ] Aikido'yu seç: Kata sekmesi dürüstçe boş mu, "teknik sekmesine bak"
      yönlendirmesi çalışıyor mu
- [ ] Ücretsiz bir kataya gir, video yoksa "video yakında" + açıklama
      metni görünüyor mu; video varsa (admin'den eklediysen) oynatılıyor mu
- [ ] **"Bugün bunu çalıştım"** butonuna bas — pratik kaydı düştü mü,
      seri arttı mı
- [ ] Aynı kataya birkaç kez daha bas — **tekrar sayacı** ("Bunu N kez
      çalıştın") doğru artıyor mu
- [ ] Pro (kilitli) bir kataya girişsiz git — login'e yönleniyor mu;
      girişli ama Pro değilken git — billing sayfasına yönleniyor mu

## E. Rehber (/guide)

- [ ] Girişsiz `/guide` açılıyor mu, 10 branş listeleniyor mu
- [ ] Bir branşa gir: Başlangıç programı, Kata, Teknikler, İpuçları
      bölümleri sırayla görünüyor mu, içindekiler linkleri çalışıyor mu
- [ ] Kata diyagramları (happo/embusen) düzgün render oluyor mu
- [ ] "Video kütüphanesi →" linki doğru branşın `/kata` sayfasına gidiyor mu
- [ ] TR ve EN'de aynı sayfayı aç, iki dilin de anlamlı olduğunu kontrol et

## F. Blog

- [ ] Girişsiz `/blog` açılıyor, yazılar okunuyor mu
- [ ] Arama kutusuna bir kelime yaz — filtreleniyor mu
- [ ] Branş filtresi çipleri çalışıyor mu
- [ ] Girişli yeni yazı yaz: **markdown araç çubuğu** (kalın/italik/başlık/
      liste/alıntı/link) doğru biçimlendiriyor mu
- [ ] Yayınlanan yazıda markdown doğru HTML'e dönüşmüş mü (başlık, liste vb.)
- [ ] Kendi yazını düzenle, sonra sil — ikisi de çalışıyor mu
- [ ] Başka birinin yazısında düzenle/sil butonlarının **görünmediğini**
      doğrula

## G. Topluluk, takip, haftanın enleri

- [ ] Profilini herkese açık yap, kullanıcı adı belirle
- [ ] `/practitioners`'da kendini bul, arama kutusuyla ara
- [ ] Başka bir hesaptan seni takip et — takipçi sayın arttı mı
- [ ] Takip ettiğin kişi pratik kaydedince dashboard'daki **"Takip
      ettiklerin"** akışında görünüyor mu
- [ ] **Haftanın enleri**: bu hafta en çok dakika yapan doğru sırada mı
      (birkaç test hesabıyla farklı dakikalarda kayıt at, kontrol et)

## H. Avatar ve paylaşım (bu turun yeni özelliği)

- [ ] Herkese açık profilinde **avatar** görünüyor mu (enso halkası +
      kuşak rengi + baş harf) — kuşağın değiştikçe halka rengi de
      değişiyor mu
- [ ] `/practitioners` listesinde ve blog yazarı yanında küçük avatar
      görünüyor mu
- [ ] Profilinde **"Paylaş"** butonuna bas:
  - [ ] **Telefonda**: native paylaşım sayfası açılıyor mu (WhatsApp,
        Instagram Story, Mesajlar vb. seçenekleri görmeli), görsel
        (kart) da paylaşıma dahil oluyor mu
  - [ ] **Masaüstünde**: açılır menüde X/WhatsApp/İndir seçenekleri
        çalışıyor mu
- [ ] `/u/<kullanıcı>/card.png` linkini doğrudan tarayıcıda aç — kart
      güzel görünüyor mu (isim, avatar, seri, kuşak bandı, ısı haritası)
- [ ] Bu linki WhatsApp'a veya Twitter'a yapıştır — link önizlemesinde
      kart görselinin çıktığını doğrula (og:image çalışıyor mu)
- [ ] Dashboard'daki paylaşım widget'ı: profil **gizliyken** "profili
      herkese açık yap" önerisi çıkıyor mu; **açıkken** paylaş butonu
      çıkıyor mu
- [ ] Gizli bir profilin avatar/kart linkine doğrudan git — 404 dönüyor
      mu (başkasının gizli verisi sızmamalı)

## I. Bildirimler

- [ ] Dashboard'da **"Bildirimleri aç"** butonuna bas, tarayıcı izin
      sorusunu onayla — buton "Bildirimler açık" durumuna geçiyor mu
- [ ] Reddet ve tekrar dene — düzgün geri dönüyor mu
- [ ] Profilde **e-posta hatırlatmasını** aç
- [ ] O gün pratik kaydetmeden `scripts/send_reminders.py`'yi elle
      çalıştır — hem mail hem push bildirimi geldi mi
- [ ] Bildirime tıkla — uygulamayı doğru sayfada (`/app`) açıyor mu

## J. Waitlist ve referans linki (hâlâ `WAITLIST_ONLY=true` iken de test et)

- [ ] `WAITLIST_ONLY=true` yapıp joatolyesi.com'a git: **sadece** landing
      sayfası ve mail formu görünüyor mu — hiçbir menü/link yok mu
      (login, guide, blog, kata dahil hiçbiri erişilebilir olmamalı)
- [ ] Mail ile kaydol — "Listede X. kişisin" + kendi davet linki çıkıyor mu
- [ ] Aynı maille tekrar dene — "zaten listedesin" mesajı çıkıyor mu
- [ ] Kendi davet linkini (`?ref=...`) başka bir tarayıcıda aç, farklı
      maille kaydol — CSV'de (`/admin/waitlist?token=...`) `referred_by`
      sütununa doğru kod düştü mü
- [ ] `/privacy` ve `/terms` waitlist modunda da açılıyor mu

## K. Programlar ve ödeme (Pro)

- [ ] `/programs`'a gir, 30 günlük programa kaydol
- [ ] Bir günü tamamla — bir sonraki gün açılıyor mu, önceki gün
      tamamlanmadan sonrakine geçilemiyor mu
- [ ] Lemon Squeezy **test mode**'da satın alma yap — `/billing`
      "aktif" gösteriyor mu
- [ ] Pro içerik (kilitli kata, programlar) aboneliğin aktifken açılıyor mu
- [ ] Webhook testi: LS panelinden test webhook'u gönder, abonelik
      durumu güncelleniyor mu

## L. Mobil / PWA

- [ ] Telefonda Chrome/Safari'de siteyi aç, "ana ekrana ekle" ile yükle
- [ ] Ana ekran ikonundan aç — tam ekran (adres çubuğu olmadan) açılıyor mu
- [ ] Ana ekran ikonuna basılı tutunca kısayollar (Pratik kaydet, Kata)
      çıkıyor mu
- [ ] Uçak modunda aç — önbelleğe alınmış statik dosyalar (CSS, ikonlar)
      hatasız yükleniyor mu
- [ ] Tüm sayfaları telefon genişliğinde gez — metin taşması, buton
      üst üste binmesi var mı (özellikle profil header + avatar + paylaşım
      widget'ı yeni eklendi, mobilde dikey diziliyor mu kontrol et)

## M. Dil ve genel gözden geçirme

- [ ] Her sayfada TR ⇄ EN geçişini dene — çeviri eksik/devrik yer var mı
- [ ] `?src=ig` gibi bir kaynak parametresiyle gelip dil değiştirince
      parametrenin korunduğunu doğrula
- [ ] Masaüstünde geniş ekranda (1440px+) landing sayfasını gez — hero,
      cihaz mockup'ları, bölümler orantılı mı
- [ ] 404 sayfası (var olmayan bir kullanıcı adı/kata/blog yazısı) düzgün
      görünüyor mu

## N. Güvenlik ve altyapı (LAUNCH.md ile çakışan maddeler — tekrar kontrol)

- [ ] CSRF: bir formu tarayıcı konsolundan token'sız POST etmeyi dene —
      403 dönmeli
- [ ] Rate limit: `/login`'e art arda 11 kez yanlış şifreyle POST at —
      11.'de reddedilmeli
- [ ] `ENV=production` iken çerezlerin `Secure` bayrağı taşıdığını
      (tarayıcı geliştirici araçlarından) doğrula
- [ ] Sentry'ye kasıtlı bir hata düşür (örn. geçersiz bir route ile 500
      tetikle) — panelde görünüyor mu
- [ ] `scripts/backup.sh`'ı elle çalıştır, dump dosyasının gerçekten
      okunabilir olduğunu `zcat` ile doğrula

---

## Bulduğun sorunları nereye not alacaksın

Küçük bug/typo → doğrudan söyle, aynı oturumda düzeltilir.
Kapsam dışı / "olsa iyi olur" fikirleri → TODO.md §3'e eklenir.
İçerik hatası (rehberdeki bir kata/teknik bilgisi yanlışsa) → TODO.md
§3b "Rehber araştırma listesi"ne düşülür, sen doğrulayınca eklenir.
