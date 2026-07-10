# Joryu — Business Brief & Phase 0 Spec

## 1. Strateji özeti (bu neden var)

Sahibin haksız avantajı dağıtım: martial arts içerik kanalları
(Instagram @joryu.art — bazı videolar 138k izlenme, YouTube ~1.260 abone,
TikTok). Ürün bu kanalların ucuna takılan bir dönüşüm noktası.

Hedef kitle: tek başına antrenman yapan silah/kata pratisyenleri
(jo, bokken; aikido, iaido, kobudo). Bu nişte global düzeyde ciddi bir
uygulama yok, Türkçe'de hiç yok.

Gelir modeli (sırasıyla devreye girecek):
1. Tek seferlik dijital program satışı ("30-Day Jo Suburi Program", $19–29)
2. Freemium abonelik: takip ücretsiz; programlar + kata kütüphanesi Pro
   ($4.99/ay veya $39/yıl; TR için yerel fiyat ~₺59/ay)
3. Ekipman affiliate linkleri (jo, bokken, hakama — Amazon + niş satıcılar)
4. YouTube reklam geliri (eşik geçilince, bonus)

Doğrulama kapısı: Landing page 2 hafta içinde 100+ e-posta toplarsa
Phase 1 (uygulama MVP) başlar. 20'nin altında kalırsa konumlandırma
değişir, kod yazılmaz.

## 2. Phase 0 kapsamı — Landing page + waitlist

Tek FastAPI uygulaması, tek sayfa + bir POST endpoint.

### Sayfa yapısı (yukarıdan aşağı)
1. **Hero**: tam genişlik video/görsel alanı (sahibin kendi çekimi,
   placeholder olarak koyu atmosferik bir arka plan bırak).
   Başlık + alt başlık + e-posta formu (tek alan + buton).
2. **Problem**: 3 kısa blok — "Dojo haftada 2 gün, sen her gün çalışmak
   istiyorsun" / "Kata sırasını unutuyorsun" / "İlerlediğini göremiyorsun".
3. **Çözüm önizleme**: 3 özellik kartı — Günlük pratik kaydı & seri (streak),
   Kata & suburi video kütüphanesi, 30 günlük yapılandırılmış programlar.
4. **Sosyal kanıt**: "290+ gün kesintisiz jo pratiğinden doğdu" satırı +
   Instagram embed/link.
5. **İkinci CTA**: e-posta formu tekrar.
6. **Footer**: sosyal linkler (@joryu.art), dil değiştirici (EN/TR).

### Metinler

**EN**
- Hero H1: "Train every day. Even when the dojo is closed."
- Hero sub: "Joryu is the practice companion for jo, bokken and kata —
  daily tracking, structured programs, and a video library built by a
  practitioner who trained 290 days straight."
- CTA button: "Join the waitlist"
- Form success: "You're in. First invites go out soon."

**TR**
- Hero H1: "Her gün çalış. Dojo kapalıyken bile."
- Hero sub: "Joryu; jo, bokken ve kata için pratik yoldaşın — günlük takip,
  yapılandırılmış programlar ve 290 gün aralıksız çalışan bir
  pratisyenin video kütüphanesi."
- CTA button: "Bekleme listesine katıl"
- Form success: "Listedesin. İlk davetler yakında."

### Teknik gereksinimler
- `GET /` → landing page (lang: cookie > ?lang= > Accept-Language, default EN)
- `POST /waitlist` → e-posta kaydı (HTMX ile inline success mesajı)
  - Validasyon: format + tekrar kayıt idempotent (aynı e-posta hata vermez)
  - Tablo: waitlist(id, email unique, lang, source, created_at)
  - `source` = ?src= query param (ig, yt, tt ayrımı için — sahibi hangi
    kanalın dönüştürdüğünü görmek istiyor)
- Basit admin: `GET /admin/waitlist?token=...` env'den token, CSV export
- Rate limit: IP başına dakikada 5 POST (slowapi veya basit in-memory)
- Dockerfile + compose.yml (app + postgres), .env.example
- Sayfa < 200KB, Lighthouse mobile 90+ hedef

### Yapılmayacaklar (Phase 0)
Ödeme, kullanıcı hesabı, dashboard, uygulamanın kendisi, blog, SEO
çalışması. Sadece yukarıdaki kapsam.

## 3. Phase 1 — Uygulama MVP (AKTİF FAZ)

Phase 0 tamamlandı; landing + waitlist `/` altında yaşamaya devam eder.

### Kapsam
1. **Hesaplar**: e-posta + şifre kayıt/giriş. bcrypt hash, imzalı session
   cookie. OAuth yok, magic link yok, e-posta doğrulama yok (Phase 2).
2. **Pratik kaydı + streak (ücretsiz)**: tarih, disiplin (jo/bokken/kata/
   diğer), süre (dk), not. Streak = art arda pratik yapılan gün sayısı
   (bugün veya dün kayıt varsa canlı). Dashboard: streak + GitHub tarzı
   aktivite ısı haritası (kayıt eklenince hücre renklenir; hover/dokunuşta
   tarih + branşlar + dakika) + son kayıtlar.
3. **Kata & suburi video kütüphanesi**: EN/TR başlık + açıklama, video URL
   (sahibin çekimleri; şimdilik placeholder). Birkaç içerik ücretsiz,
   kalanı Pro kilidi arkasında.
4. **30 günlük program motoru (Pro)**: program → 30 gün, her gün içerik +
   opsiyonel video. Kayıt (enroll) → günler sırayla açılır, gün tamamlama
   işaretlenir. İlk içerik: "30-Day Jo Suburi Program".
5. **Pro abonelik — Lemon Squeezy**: hosted checkout linkleri (aylık $4.99 /
   yıllık $39), webhook ile subscription durumu senkronu. Kart verisi bize
   uğramaz. `custom[user_id]` ile eşleşme. İptal edilen abonelik dönem
   sonuna dek Pro kalır.
6. **PWA**: manifest + service worker, standalone açılış `/app`.
7. **Profil & topluluk ("dövüş sanatçılarının GitHub'ı")**: kullanıcı adı,
   görünen ad, bio, branş. Profil varsayılan gizli; kullanıcı isterse
   herkese açık yapar. Açık profil: pratik istatistikleri (seri, toplam
   seans/dakika) + GitHub tarzı aktivite ısı haritası. `/practitioners`
   altında kullanıcı arama. Açık profiller giriş yapmadan görüntülenebilir.
8. **Kata kütüphanesi branş filtresi**: varsayılan görünüm kullanıcının
   branşı; sekmelerle diğer branşlara veya tümüne geçilebilir.

Varsayılan dil TR (cookie > ?lang= > Accept-Language > TR).

### Yapılmayacaklar (Phase 1)
Native app, tek seferlik program satışı, affiliate sayfaları, e-posta
gönderimi, sosyal özellikler, çoklu kullanıcı rolleri.

## 4. Kararlar
- Domain: **joatolyesi.com** (karar verildi; canonical/OG etiketleri buna göre)
- Waitlist e-postaları için gönderim: şimdilik yok, sadece topla
- Analytics: **Google Analytics 4** — ölçüm kimliği G-54NX2S2Z01
- Branşlar: aiki-jo, bokken (aiki-ken), aikido, jodo (ZNKR seitei),
  jojutsu (SMR kihon), kenjutsu, kendo (Nihon Kendō Kata), iaido (ZNKR
  seitei), karate (Shotokan), taekwondo (WT Taegeuk) + diğer. Katalog
  standart müfredat listelerinden doğrulanarak seed'lendi.
