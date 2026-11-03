# Instagram → site hunisi (B-04) — taslak

- Tarih: 2026-11-03 · Sprint: `team/sprint-2026-11-03` · İş 3
- Hazırlayan: growth-marketer · Durum: **taslak**. Hiçbir yere paylaşılmadı. Paylaşımı İlteriş yapacak.
- `[fact-check]` işaretli her cümle teknik dövüş sanatı iddiası içeriyor. `fact-checker` onayı gelmeden **kullanılmamalı**. Liste en altta (§9).
- Rakamlar: başlangıç değerleri yalnız `docs/team/METRICS.md`'den alındı. Bilinmeyen her değer "bilinmiyor" olarak yazıldı.

---

## 1. Teşhis: Instagram trafiği GA4'te neden düşük görünüyor olabilir?

Başlangıç verisi (METRICS.md, 2026-11-02, son 28 gün): instagram ~5 oturum (4+1), direct 14, google/organic 17. BRIEF.md'ye göre bazı videolar 138k izlenmeye ulaştı. **İzlenme ile tıklama arasındaki oran bilinmiyor.** Instagram Insights'taki "bağlantı tıklaması" (link tap) sayısı ekipte yok.

Aşağıdakilerin hiçbiri doğrulanmadı. Hepsi kontrol edilmesi gereken olasılıklar:

| # | Olasılık | Nasıl doğrulanır | Doğrulanırsa ne yapılır |
|---|---|---|---|
| 1a | **Bio'da site linki yok, ya da başka bir yere gidiyor** (eski waitlist linki `?src=ig`, Linktree, YouTube…) | Instagram uygulamasında @joryu.art profilini **çıkış yapmış bir tarayıcıdan** ve telefondan aç, bio linkine dokun, adres çubuğundaki son URL'yi not et. | §2'deki bio linkiyle değiştir (§6, adım 1). |
| 1b | **Bio linki var ama ziyaretçi landing'de kalıyor** (landing'de hemen çıkma oranı %66-75, METRICS.md) | GA4 → Raporlar → Etkileşim → Açılış sayfası, filtre: Oturum kaynağı = instagram. Instagram oturumlarının hangi sayfaya düştüğüne bak. | Bio linkini videoda görülene daha yakın bir sayfaya (ör. `/kata?d=aikijo`) yönlendirmeyi A/B gibi dene (§7). |
| 2 | **Instagram uygulama içi tarayıcı referrer'ı kaybediyor, trafik "direct"e yazılıyor.** Bu, sektörde sık bildirilen bir durum ama bizim sitemiz için doğrulanmadı. | (a) Kendi telefonundan bio linkine dokun. GA4 → Raporlar → **Gerçek zamanlı**'da oturumun kaynağı "instagram" mı yoksa "(direct)" mi görünüyor, bak. (b) Aynı testi UTM'li linkle tekrarla. UTM'li link "instagram / social" görünüyorsa sorun bu ve UTM çözüyor demektir. | Bütün Instagram linklerinde UTM kullan (§2). UTM, referrer'dan bağımsız olarak kaynağı taşır. |
| 3 | **Reels'ta CTA yok ya da tıklanabilir bir yol yok.** Reels açıklamasına yazılan URL'ler genellikle tıklanabilir değil (platform davranışı, güncel durumu İlteriş kendi hesabında kontrol etmeli). | Son 10 reels'ın açıklama/ekran metnine bak: kaçında "linki bio'da" ya da benzeri bir yönlendirme var? Insights → profil ziyareti ve dış bağlantı dokunuşları. | §5'teki CTA'ları kullan. Her reels'ı aynı gün bağlantı çıkartmalı (link sticker) bir story ile destekle. |
| 4 | **İzlenmelerin büyük kısmı hedef kitle dışı** (keşfet akışında genel izleyici; pratisyen değil) | Insights → reels → izleyicilerin takipçi / takipçi olmayan oranı ve ülke dağılımı. Kesin bir ölçüm yolu yok; dolaylı sinyal. | Pratisyene yönelik içerikte (kata, suburi) CTA'yı güçlendir. Genel izleyici videosunda CTA'yı yumuşak tut. |
| 5 | **Giriş yapmış kullanıcı `/` → `/app`'e yönleniyor ve UTM düşüyor.** `app/routers/landing.py::index` giriş yapmış kullanıcıyı sorgu parametresi olmadan `/app`'e 303 ile yönlendiriyor, bu yüzden GA'nın gördüğü ilk sayfa UTM'siz `/app` oluyor. | Kod incelemesiyle doğrulandı. Etkisi yalnız **mevcut** kullanıcılarla sınırlı; yeni ziyaretçiyi etkilemez. | Bu sprintte bir şey yapılmıyor. Not olarak backlog'a girebilir (redirect'te `utm_*` parametrelerini korumak). |

---

## 2. Link şeması

**Neden UTM:** Kullanıcı kaydında `?src=` saklanmıyor. `src` yalnızca waitlist formunda kullanılıyor (`WAITLIST_GROWTH.md`, `app/routers/landing.py`). Site artık waitlist modunda değil (`waitlist_only` varsayılanı `False`, prod'da `/kata/sanjuichi-no-jo` 2026-11-03'te açık bir kata sayfası döndü). Bu yüzden asıl ölçüm yolu **UTM + İş 1'deki `sign_up` olayı**. GA4, `utm_*` parametrelerini sayfa URL'sinden kendisi okur. Kod gerekmiyor.

**Sabit kurallar:**

- `utm_source=instagram`: her zaman küçük harf, hep aynı.
- `utm_medium=social`
- `utm_campaign=` yalnız şu üç kalıptan biri:
  - `bio`: profil bio linki
  - `story-<konu>`: story bağlantı çıkartması (ör. `story-31-jo`)
  - `reel-<konu>`: reels'ı destekleyen story'deki ya da yorum/DM'de verilen link (ör. `reel-happo-giri`)
- `<konu>`: küçük harf, tire ile, Türkçe karakter yok, ≤20 karakter. Mümkünse sayfanın slug'ı ya da branş adı.
- `utm_content` kullanılmıyor (2 haftalık testte gereksiz kırılım).

**Hazır linkler (hepsi doğrulanmış route'lar, bkz. §9.2):**

| Kullanım | URL |
|---|---|
| Bio (varsayılan) | `https://joatolyesi.com/?utm_source=instagram&utm_medium=social&utm_campaign=bio` |
| Bio (alternatif, §7'deki deney) | `https://joatolyesi.com/kata?d=aikijo&utm_source=instagram&utm_medium=social&utm_campaign=bio` |
| Doğrudan kayıt | `https://joatolyesi.com/register?utm_source=instagram&utm_medium=social&utm_campaign=story-kayit` |
| Aiki-jo kütüphanesi | `https://joatolyesi.com/kata?d=aikijo&utm_source=instagram&utm_medium=social&utm_campaign=story-aikijo` |
| Aiki-jo suburi (teknik sekmesi) | `https://joatolyesi.com/kata?d=aikijo&kind=teknik&utm_source=instagram&utm_medium=social&utm_campaign=reel-jo-suburi` |
| 31 no jo kata | `https://joatolyesi.com/kata/sanjuichi-no-jo?utm_source=instagram&utm_medium=social&utm_campaign=reel-31-jo` |
| 13 no jo kata | `https://joatolyesi.com/kata/jusan-no-jo?utm_source=instagram&utm_medium=social&utm_campaign=reel-13-jo` |
| Jo happo giri | `https://joatolyesi.com/kata/aikijo-happo-giri?utm_source=instagram&utm_medium=social&utm_campaign=reel-happo-giri` |
| Choku tsuki | `https://joatolyesi.com/kata/choku-tsuki?utm_source=instagram&utm_medium=social&utm_campaign=reel-choku-tsuki` |
| Bokken kütüphanesi (teknik) | `https://joatolyesi.com/kata?d=bokken&kind=teknik&utm_source=instagram&utm_medium=social&utm_campaign=reel-bokken-suburi` |
| Aiki-ken suburi 1 | `https://joatolyesi.com/kata/bokken-shomen-suburi?utm_source=instagram&utm_medium=social&utm_campaign=reel-ken-suburi-1` |
| Bokken happo giri | `https://joatolyesi.com/kata/bokken-happo-giri?utm_source=instagram&utm_medium=social&utm_campaign=reel-bokken-happo` |
| Aiki-jo rehberi | `https://joatolyesi.com/guide/aikijo?utm_source=instagram&utm_medium=social&utm_campaign=story-rehber-aikijo` |
| Bokken rehberi | `https://joatolyesi.com/guide/bokken?utm_source=instagram&utm_medium=social&utm_campaign=story-rehber-bokken` |
| Tüm rehberler | `https://joatolyesi.com/guide?utm_source=instagram&utm_medium=social&utm_campaign=story-rehber` |

Not: `/kata?d=` yalnız katalogda içeriği olan seçilebilir branşları kabul ediyor: `aikijo`, `bokken`, `aikido`, `jodo`, `kenjutsu`, `kendo`, `iaido`. Geçersiz bir değer hata vermiyor ama sessizce varsayılan görünüme düşüyor, bu yüzden yazım hatası fark edilmez. Linki kopyalayıp yapıştır, elle yazma.

---

## 3. Bio metni (≤150 karakter)

Karakter sayıları satır sonları ve boşluklar dahil, **metnin tamamı** üzerinden sayıldı (Python `len`). Emoji eklenmedi; İlteriş eklerse sınırı tekrar kontrol etsin.

**Seçenek A (TR + EN, iki dilli):**

```
Jo & bokken, her gün. Dojo kapalıyken bile.
Daily jo & bokken practice.
Ücretsiz pratik takibi + kata kütüphanesi ↓
```
(115 karakter)

**Seçenek B (pratik odaklı, TR + EN):**

```
Aiki-jo · aiki-ken · solo pratik
Kata ve suburi kütüphanesi, günlük seri takibi — ücretsiz.
Free solo practice tracker ↓
```
(120 karakter)

- Bio linki: `https://joatolyesi.com/?utm_source=instagram&utm_medium=social&utm_campaign=bio`
- "Ücretsiz" ifadesi şu anki durumla uyumlu: Pro kapalıyken ödeme duvarı yok (`app/routers/kata.py::kata_detail`). Pro açılırsa bio metni güncellenmeli.
- Metinlerde sayı, kullanıcı sayısı ya da sosyal kanıt yok. Teknik iddia yok, bu yüzden `[fact-check]` gerekmiyor.

---

## 4. İçerik ↔ sayfa eşleme tablosu

Kural: videoda **ne görünüyorsa**, link o sayfaya gider. Genel ana sayfaya yalnız içerikten bağımsız videolar (kurucu hikâyesi, seri) gider.

| Video türü | Ekran/açıklama CTA'sı (TR) | Story link çıkartması → sayfa | `utm_campaign` |
|---|---|---|---|
| Jo suburi (tsuki, uchikomi vb. tekli hareket) | "20 suburinin hepsi kısa notlarla sitede — link storyde." `[fact-check]` **F1: DOĞRULANDI** | `/kata?d=aikijo&kind=teknik` | `reel-jo-suburi` |
| 31 no jo kata | "31'li katanın sayfası ve pratik kaydı — link storyde." | `/kata/sanjuichi-no-jo` | `reel-31-jo` |
| 13 no jo kata | "13'lü kata sayfası — link storyde." | `/kata/jusan-no-jo` | `reel-13-jo` |
| Jo happo giri | "8 yöne kesiş, ısınma rutini olarak — link storyde." `[fact-check]` **F3 (jo): DÜZELTİLMELİ** · F4: kişisel ifade (bkz. Denetim) | `/kata/aikijo-happo-giri` | `reel-happo-giri` |
| Bokken suburi (aiki-ken) | "Aiki-ken suburileri tek sayfada — link storyde." | `/kata?d=bokken&kind=teknik` | `reel-bokken-suburi` |
| Bokken happo giri | "Bokkenle 8 yön — link storyde." `[fact-check]` **F3 (bokken): DOĞRULANDI** | `/kata/bokken-happo-giri` | `reel-bokken-happo` |
| "Aiki-jo nedir / nereden başlanır" anlatısı | "Nereden başlayacağını rehberde yazdık — link storyde." | `/guide/aikijo` | `story-rehber-aikijo` |
| Kurucu hikâyesi / kesintisiz pratik serisi | "Sen de serini başlat — link bio'da." | `/register` | `story-kayit` |
| Jodo (yalnız video gerçekten Seitei Jōdō ise) | "Seitei jodo katalarının listesi — link storyde." `[fact-check]` **F6: DOĞRULANDI** (yazım: "Seitei Jōdō" önerilir) | `/kata?d=jodo` | `reel-jodo` |

---

## 5. Reels/story CTA + açıklama taslakları

Hepsi tek kişiyle, bahçede ya da evde, 15-45 sn'de çekilebilir. Sayı, kullanıcı sayısı, sahte yorum ya da "binlerce pratisyen" gibi iddia yok. `<N>` yazan yere İlteriş **gerçek** gün sayısını kendisi yazar. BRIEF.md'deki "290+" eski bir değer olabilir, doğrulanmadan kullanılmamalı.

### 5.1 — "Tsuki serisi, yavaş çekim" (jo, 20-30 sn)
- **Çekim:** Sabit kamera, yandan. Choku tsuki, kaeshi tsuki, ushiro tsuki; her biri 1 normal, 1 yavaş tekrar.
- **Ekran metni:** "Aiki-jo suburi 1-3" `[fact-check]` **F2: DOĞRULANDI**
- **Açıklama (TR):** Tsuki serisinin ilk üç hareketi. Sırası ve kısa notları sitede, linki storyde. `[fact-check]` **F2: DOĞRULANDI**
- **Açıklama (EN):** First three of the tsuki series. Order and notes on the site, link in story. `[fact-check]` **F2: DOĞRULANDI**
- **Story:** aynı videodan 5 sn kesit + link çıkartması → `/kata?d=aikijo&kind=teknik` (`reel-jo-suburi`)

### 5.2 — "31'li katayı bölüm bölüm" (jo, 30-45 sn)
- **Çekim:** 31 no jo katanın tamamı, normal hızda, tek çekim. İsteğe bağlı ekranda bölüm geçişleri.
- **Ekran metni:** "31 no jo kata"
- **Açıklama (TR):** 31'li kata, baştan sona. Siteden kataya her çalıştığında tek tuşla kayıt düşebilirsin. Linki storyde.
- **Açıklama (EN):** The 31 jo kata, start to finish. Log each run with one tap on the site. Link in story.
- Not: "kataya tek tuşla kayıt" bir ürün özelliği (`POST /kata/{slug}/log`), teknik iddia değil. Bölüm sayısı ya da bölümlerin yerini ekrana yazacaksa `[fact-check]` gerekir.
- **Story:** link çıkartması → `/kata/sanjuichi-no-jo` (`reel-31-jo`)

### 5.3 — "Ders öncesi 2 dakika: happo giri" (jo veya bokken, 15-25 sn)
- **Çekim:** Üstten ya da çaprazdan; 8 yön tek tur.
- **Ekran metni:** "Happo giri — 8 yön" `[fact-check]` **F3: bokken DOĞRULANDI / jo DÜZELTİLMELİ**
- **Açıklama (TR):** Isınma rutinim: 8 yöne tek tur. Sayfası sitede, linki storyde. `[fact-check]` **F3: bokken DOĞRULANDI / jo DÜZELTİLMELİ · F4: kişisel ifade, İlteriş teyit etmeli**
- **Açıklama (EN):** My warm-up: one round to eight directions. Page on the site, link in story. `[fact-check]` **F3: bokken DOĞRULANDI / jo DÜZELTİLMELİ · F4: kişisel ifade, İlteriş teyit etmeli**
- Not: Seed metnindeki "kuzeyden başlayıp saat yönünde" ve "en iyi ısınma" ifadeleri **kullanılmadı**; ilki sıra iddiası, ikincisi abartı.
- **Story:** → `/kata/aikijo-happo-giri` (`reel-happo-giri`) ya da `/kata/bokken-happo-giri` (`reel-bokken-happo`)

### 5.4 — "Dojo kapalı, pratik açık" (kurucu/seri, 15-20 sn)
- **Çekim:** Kısa suburi kesiti + telefonda sitenin seri ekranı (kendi hesabı, gerçek rakamla).
- **Ekran metni:** "Gün <N>"
- **Açıklama (TR):** Dojo haftada iki gün açık; kalan günlerde evde çalışıyorum ve her gününü kaydediyorum. Kendi serini başlatmak istersen link bio'da.
- **Açıklama (EN):** The dojo is open two days a week; I train the rest at home and log every day. Start your own streak, link in bio.
- Not: "haftada iki gün" İlteriş'in kendi dojosu için doğru değilse kendi rakamıyla değiştirmeli. Bu kişisel bir ifade, genel bir iddia değil.
- **Story:** → `/register` (`story-kayit`)

### 5.5 — "Aiki-ken suburi 1" (bokken, 20-30 sn)
- **Çekim:** Önden ve yandan iki açı; ichi no suburi, 3 tekrar.
- **Ekran metni:** "Aiki-ken suburi 1 — Ichi no suburi" `[fact-check]` **F5: DOĞRULANDI**
- **Açıklama (TR):** Yedi aiki-ken suburisinin ilki. Hepsinin listesi sitede, linki storyde. `[fact-check]` **F5: DOĞRULANDI**
- **Açıklama (EN):** The first of the seven aiki-ken suburi. Full list on the site, link in story. `[fact-check]` **F5: DOĞRULANDI**
- **Story:** → `/kata/bokken-shomen-suburi` (`reel-ken-suburi-1`)

**Her reels için ortak kural:** Reels aynı gün aynı videodan bir story + link çıkartması ile desteklenir. Her story'nin `utm_campaign` değeri farklıdır, böylece hangi videonun tıklama getirdiği GA4'te ayrışır.

---

## 6. İlteriş'in somut adımları (3 madde, toplam ~10 dk)

1. **(~4 dk)** @joryu.art bio linkini `https://joatolyesi.com/?utm_source=instagram&utm_medium=social&utm_campaign=bio` ile değiştir, bio metni olarak §3'teki A ya da B'yi yapıştır.
2. **(~3 dk)** Telefondan kendi bio linkine dokun, GA4 → **Gerçek zamanlı**'da oturumun "instagram / social" olarak göründüğünü kontrol et (§1, olasılık 2'nin testi). Görünmüyorsa rapora not düş.
3. **(~3 dk)** Bir sonraki jo videosunu paylaşırken aynı gün §4'teki eşleşen link ile bir story at.

(5.1-5.5 taslaklarının kullanımı, fact-check sonucuna bağlı olduğu için bu listeye dahil edilmedi.)

---

## 7. Ölçüm planı

**Nereye bakılır (GA4):**

- **Edinme → Trafik edinme**: boyut "Oturum kaynağı / aracı", satır `instagram / social`. Oturum sayısı ve ortalama etkileşim süresi.
- Aynı rapora ikincil boyut olarak **Oturum kampanyası**: `bio`, `story-*`, `reel-*` kırılımı.
- **`sign_up` kaynak bazında**: İş 1 deploy edildikten sonra. Raporlar → Etkileşim → Etkinlikler → `sign_up`, ikincil boyut "Oturum kaynağı / aracı". İlteriş'in `sign_up` ve `practice_logged`'ı Key event işaretlemesi (SPRINT "sorulacaklar" #3) bu raporu kolaylaştırır.
- **Instagram Insights** (GA4 dışında): bio link dokunuşu ve story link çıkartması dokunuşu. GA4'teki oturumla karşılaştırılarak "tıklandı ama oturum gelmedi" kaybı görülebilir.
- **Kontrol:** `(direct) / (none)` oturumları. UTM'den sonra düşerse olasılık 2 güçlenir.

**Başlangıç:** instagram ~5 oturum / 28 gün (METRICS.md). Instagram kaynaklı `sign_up`: **ölçülmüyor** (başlangıç yok). Bio link dokunuş sayısı: **bilinmiyor**.

**2 haftalık başarı eşiği (hipotez, tahmin değil):**

> **H1:** Bio linki UTM'li hale gelip her reels bir link çıkartmalı story ile desteklenirse, 14 günde `instagram / social` oturumu, başlangıcın 14 güne düşen payının (~2-3) **belirgin üstüne** çıkar. Eşik olarak **≥10 oturum / 14 gün** öneriliyor. Bu sayı bir hacim tahmini değil, karar için seçilmiş bir çizgi.
>
> **H2:** Bu oturumlardan **≥1 `sign_up`** gelir (İş 1 deploy edilmişse).

**Karar kuralı:**
- H1 tutarsa: link çıkartmalı story'yi standart yap; bir sonraki sprintte §7'deki "bio → `/kata?d=aikijo`" alternatifini 2 hafta dene ve `sign_up` oranını karşılaştır.
- H1 tutmazsa ama Insights'ta dokunuşlar varsa: kayıp tıklama ile oturum arasında. Olasılık 2'yi ve sayfa yüklenme süresini incele.
- H1 tutmazsa ve dokunuş da yoksa: sorun CTA/içerik tarafında (olasılık 3-4). Bir sonraki sprintte CTA metinleri değiştirilir.

---

## 8. Teknik iddia içeren metinler (`[fact-check]` işaretleri)

Bu dosyadaki bütün teknik dövüş sanatı iddiaları aşağıda tek tek listelendi. `fact-checker` denetiminden geçmeyen bir metin **kullanılmamalı**. Fact-check gerektirmeyen alternatif: ilgili cümleden sayı ve sıra bilgisini çıkarıp yalnız kata adını bırakmak (ör. "Tsuki serisi" yerine "Jo suburi").

| # | Yer | İddia | Önerilen kaynak (CONTENT_STANDARDS hiyerarşisi) |
|---|---|---|---|
| F1 | §4 satır 1, §5.5 | Aiki-jo'da **20 suburi** vardır | (1-2) Morihiro Saito, *Takemusu Aikido* / *Traditional Aikido* cilt 2 (jo bölümü); Iwama ryu resmi yayınları |
| F2 | §5.1 | Choku tsuki, kaeshi tsuki ve ushiro tsuki aiki-jo **suburi 1-3**'tür ve "tsuki serisinin ilk üç hareketi"dir | (1-2) Saito, aynı eser, 20 jo suburi listesi |
| F3 | §4 satır 4 ve 6, §5.3 | Happo giri **8 yöne** kesiştir (jo ve bokken için) | (2) Saito'nun aiki-ken / aiki-jo yayınları; (3) iki bağımsız köklü Iwama dojo sitesi |
| F4 | §5.3 | Happo giri bir ısınma rutini olarak kullanılır | Kişisel kullanım olarak çerçevelendi ("ısınma rutinim"). Fact-checker bunu kişisel ifade sayarsa onay gerekmez. Genel bir iddiaya dönüşürse kaynak gerekir. |
| F5 | §5.5 | Aiki-ken'de **yedi suburi** vardır (nana suburi) ve ichi no suburi bunların **ilkidir** | (1-2) Saito, *Takemusu Aikido* / *Traditional Aikido* cilt 1 (aiki-ken bölümü) |
| F6 | §4 son satır | `/kata?d=jodo` sayfası **Seitei Jōdō** katalarını listeler | (1) ZNKR Seitei Jōdō müfredatı (12 kata). Seed'deki 12 slug'ın (`jodo-tsukizue` … `jodo-ran-ai`) ZNKR listesi ve sırasıyla eşleştiği kontrol edilmeli. |

Teknik iddia **içermeyen**, işaretlenmemiş metinler: §3 bio metinleri, §5.2 (sayı/bölüm yazılmadığı sürece), §5.4 (kişisel ifade), kata adının yalnızca başlık olarak geçtiği satırlar ("31 no jo kata", "13 no jo kata" sayfa adlarıdır, seed'den geliyor).

---

## 9. Ek: doğrulama notları

### 9.1 Kaynak dosyalar
- Route'lar: `app/routers/landing.py` (`/`), `app/routers/auth.py` (`/register`), `app/routers/kata.py` (`/kata`, `/kata/{slug}`), `app/routers/guide.py` (`/guide`, `/guide/{discipline}`). Hepsi `app/main.py`'de bağlı.
- `?d=` geçerli değerleri: `app/constants.py::SELECTABLE_DISCIPLINES` ∩ katalogda içerik olan branşlar. `?kind=`: `kata` | `teknik`.
- Slug'lar: `app/seed.py` (`AIKIJO`, `BOKKEN`, `CATALOG`).
- `/guide/{discipline}`: `app/guide_content.py::GUIDE` anahtarları.
- Prod kontrolü: `https://joatolyesi.com/kata/sanjuichi-no-jo` 2026-11-03'te "31 no jo kata" başlıklı kata sayfası döndü (waitlist ya da 404 değil).

### 9.2 Kullanılan ve doğrulanan linkler
`/`, `/register`, `/kata?d=aikijo`, `/kata?d=aikijo&kind=teknik`, `/kata?d=bokken&kind=teknik`, `/kata?d=jodo`, `/kata/sanjuichi-no-jo`, `/kata/jusan-no-jo`, `/kata/aikijo-happo-giri`, `/kata/choku-tsuki`, `/kata/bokken-shomen-suburi`, `/kata/bokken-happo-giri`, `/guide`, `/guide/aikijo`, `/guide/bokken`.

---

## Denetim — 2026-11-03

- Denetleyen: fact-checker · Kapsam: §8'deki F1-F6 (§4 ve §5'teki `[fact-check]` işaretleri). Kaynakların hepsi 2026-11-03'te açılıp okundu. Açılamayan kaynak doğrulanmış sayılmadı.
- **Sonuç: KISMEN ONAYLANDI.** F1, F2, F5, F6 ve F3'ün bokken kısmı doğrulandı. F3'ün jo kısmı **DÜZELTİLMELİ**. F4 kişisel ifade olarak kabul edildi, ama İlteriş'in teyidine bağlı.
- Dosya yerinde bırakıldı, `content/verified/`'e taşınmadı. Gerekçe: Bu dosya koda girecek bir içerik taslağı (guide/kata/blog/tip) değil, pazarlama planı. İçinde düzeltilmesi gereken bir madde de var. `SPRINT.md` bu yola referans veriyor.
- Not: Saito'nun kitapları (*Takemusu Aikido*, *Traditional Aikido*) çevrimiçi açılamadı. Bu yüzden F1, F2, F3 ve F5 standarttaki "birbirinden bağımsız iki orta (3) kaynak" kuralıyla doğrulandı, güçlü kaynakla değil.

| # | Karar | Kaynaklar (açıldı) | Not |
|---|---|---|---|
| F1 Aiki-jo'da 20 suburi | ✅ DOĞRULANDI | Takemusu Iwama Aikido, https://takemusu-iwama-aikido.org/?p=260 (20 suburi, 5 grup) · Minnesota Aiki Shuren Dojo, https://aikido-shuren-dojo.com/?p=87 (20 suburi, gruplar 1-5/6-10/11-13/14-18/19-20) · Aikido Journal, aikidoauckland.co.nz'de yeniden yayımlanan yazı, https://aikidoauckland.co.nz/aikido-weapons-and-how-the-system-is-structured (20 jo, 7 ken suburi) | Sitedeki aiki-jo `teknik` listesinde tam 20 kayıt var (`app/seed.py`). Bu da kaynaklardaki listeyle uyuşuyor. §8'deki F1 satırında "§5.5" yazıyor. Doğrusu yalnız §4 satır 1, çünkü §5.5 aiki-ken. |
| F2 Choku/kaeshi/ushiro tsuki = suburi 1-3, tsuki serisinin ilk üçü | ✅ DOĞRULANDI | takemusu-iwama-aikido.org/?p=260 · aikido-shuren-dojo.com/?p=87 · James Neiman, Aikido Journal, https://aikidojournal.com/?p=17169 (ushiro tsuki, tsuki no bu'nun 3.'sü) · destekleyici: https://omlc.org/aikido/weapons/jo/jo-suburi.html | Tsuki serisi 5 hareketten oluşuyor (suburi 1-5). "İlk üç" ifadesi bu yüzden doğru. |
| F3 Happo giri 8 yöne kesiş, **bokken** | ✅ DOĞRULANDI | Aikido Australia / Takemusu Aiki Association, https://aikidoaus.com.au/library/aiki-ken-curriculum/ ("ken kamae'den 8 yönlü kesiş") · Aikido Journal yazısı, aikidoauckland.co.nz (4 ana + 4 ara yön) · destekleyici: https://en.wikipedia.org/wiki/Happo-giri | Kesiş sırası kaynaktan kaynağa değişiyor: Wikipedia, Saito'nun 1975 kitabında farklı bir sıra olduğunu not ediyor. CTA'larda sıra yazmamak doğru karar. |
| F3 Happo giri 8 yöne kesiş, **jo** | ⚠️ DÜZELTİLMELİ | Bakılanlar: aikidoaus.com.au (jo happo giri yok), aikidoauckland.co.nz (yalnız ken happo giri), omlc.org jo suburi (yok), baymarinaikido.com sözlüğü (yok). Wikipedia Happo-giri (zayıf): jo karşılığı olarak *happo-no-tsuki* adlı bir **dürtüş** çalışmasından söz ediyor. | Jo ile "8 yöne kesiş" iddiasını destekleyen orta ya da güçlü bir kaynak bulunamadı. Zayıf kaynak, jo karşılığının kesiş değil dürtüş olduğunu söylüyor. **Öneri:** §4 satır 4'te ve §5.3'ün jo versiyonunda sayı/yön/kesiş ifadesini çıkar. Örnek: "Jo happo giri, ısınma rutinim — link storyde." Daha güvenlisi: §5.3'ü yalnız bokkenle çek. |
| F4 Happo giri ısınma olarak | ✅ Kişisel ifade olarak kabul edildi (kaynak gerekmez) | — | "Isınma rutinim / My warm-up" çerçevesi kişisel bir ifade. Bunun İlteriş için gerçekten doğru olması gerekiyor. Genel bir iddiaya ("happo giri bir ısınmadır") dönüştürülürse kaynak bulunamadı: Aikido Journal yazısı ısınma olarak happo giriyi değil suburiyi anıyor. §4 satır 4'teki "ısınma rutini olarak" ifadesi kişisel değil, yarı genel duruyor. "ısınma rutinim" diye yazılmalı. |
| F5 Aiki-ken'de 7 suburi, ichi no suburi ilki | ✅ DOĞRULANDI | aikidoaus.com.au aiki-ken curriculum (7 suburi, "Ichi no suburi"den "Shichi no suburi"ye, ichi = shomen uchikomi) · Aikido Journal yazısı, aikidoauckland.co.nz (yedi ken suburi) · destekleyici: aikidojournal.com/?p=17169 (27 bölüm = 20 jo + 7 ken) | Yazım notu: 7. suburi kaynakta "Shichi no suburi", seed'de "Nana no suburi" diye geçiyor (七'nin iki okunuşu). CTA'yı etkilemiyor. |
| F6 `/kata?d=jodo` Seitei Jōdō katalarını listeliyor | ✅ DOĞRULANDI | ZNKR, https://old2.kendo.or.jp/examination/docs/JODO-KYOSHI_written-test_point_201511.pdf (resmi: 1-12. kata, yani 12 kata) · Confederación Latinoamericana de Kendo sınav belgesi, https://clakendo.org/wp-content/uploads/2024/03/Examen-Teorico-de-JODO-de-CLAK.pdf (12 AJKF kata, sırasıyla adlar) · Jodo Kai Australia, https://jodokaiaustralia.com/section666820.html · Karl Geis, https://www.karlgeis.com/seitei-no-kata · kısmi teyit: BKA sınav soruları (kata 3 Hissage, kata 10 Seigan), Kendo Canada sınavı (7. Kasumi, 9. Rai Uchi) | Seed'deki 12 slug (`jodo-tsukizue` … `jodo-ran-ai`) ad ve sıra olarak listeyle birebir eşleşiyor. Liste `sort_order` ile sıralanıyor ve `?d=jodo` varsayılan olarak `kind=kata` gösteriyor. **Kapsam dışı uyarı:** Sayfadaki kata açıklamaları (ör. Hissage "jo gizli tutulur", Rai uchi "chūdan serisinden") bu denetimde doğrulanmadı. CTA yalnız "liste" dediği için sorun yok, ama açıklamalar ayrıca denetlenmeli. Yazım: aynı dosyada "Seitei jodo" ve "Seitei Jōdō" birlikte geçiyor. CTA'da "Seitei Jōdō" kullanılmalı. |

**Kullanılabilir:** §4 satır 1 (jo suburi), satır 5 (aiki-ken suburi), satır 6 (bokken happo giri), satır 9 (jodo, yalnız video Seitei ise) · §5.1 · §5.3 (bokken ile) · §5.5. §5.3'ün açıklamaları F4 teyidine bağlı.
**Kullanılmamalı (düzeltilene kadar):** §4 satır 4'ün metni ("8 yöne kesiş") ve §5.3'ün jo versiyonundaki "8 yön" ifadeleri.

**Seed'de bulunan ek bulgu (bkz. `docs/team/content/audit-log.md`):** `aikijo-happo-giri` açıklamasında "kuzeyden başlayıp saat yönünde 8 yöne men uchi" ve "en iyi ısınma" ifadeleri geçiyor. Bunlar kaynakla desteklenmiyor. Wikipedia'nın aktardığı yaygın sıra (K, G, D, B, …) saat yönünde değil, ve jo karşılığı dürtüş olarak geçiyor.
