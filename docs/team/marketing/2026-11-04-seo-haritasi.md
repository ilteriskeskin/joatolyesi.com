# SEO anahtar kelime haritası (B-05) — taslak

- Tarih: 2026-11-04 · Sprint: `team/sprint-2026-11-04` · İş: B-05
- Hazırlayan: growth-marketer · Durum: **taslak**. Kod değişmedi, hiçbir yere gönderilmedi.
- Kapsam: `app/guide_content.py` (9 branş rehberi), `app/seed.py` (kata kataloğu; görevde `scripts/` denmişti, ama `scripts/` altında kata seed dosyası yok, `scripts/seed_blog.py` yalnız blogu seed ediyor; kata seed'i `app/seed.py`'de), `scripts/seed_blog.py` (8 blog yazısı), canlı sitemap (salt okuma).
- `[fact-check]` = teknik dövüş sanatı ya da teknik SEO iddiası. `fact-checker` onayı gelmeden title/meta/H1 olarak koda girmemeli. Liste §5'te.

## 0. Yöntem ve dürüst sınırlar

- **Arama hacmi ölçülmedi.** Elimizde Keyword Planner / GSC verisi yok (GSC'de henüz 4 haftalık referans yok, SPRINT.md). Hacim yerine **"tahmini öncelik: yüksek / orta / düşük"** yazıldı. Gerekçe her satırda ya da grup başlığında.
- **Rakip kontrolü:** bu turda 6 WebSearch yapıldı (31 jo kata, seitei jodo listesi, heian shodan TR, bokken seçimi TR, seitei iai listesi, kenjutsu-kendo farkı TR). Tablolardaki "rakip" sütunu yalnız bu aramalara dayanır; **aranmayan sorgu için "kontrol edilmedi"** yazıldı. Arama aracı ABD merkezli; Türkiye sonuçları farklı olabilir.
- **Tespit edilen genel rakip örüntüsü** (6 aramadan):
  - EN sorgularda (31 jo kata, seitei jodo/iai listesi): dojo siteleri, pbworks/stenudd gibi bireysel siteler, Wikipedia. Güçlü ve eski siteler; EN'de baş başa girmek zor.
  - TR sorgularda (heian shodan, bokken seçimi, kenjutsu-kendo): sonuçların çoğu İngilizce çıktı; arama aracı Türkçe adım adım bir anlatım ya da Türkçe bokken seçim rehberi **bulamadı**. Bu, TR'nin boş alan olabileceğine dair bir işaret, kanıt değil. İlteriş'in Google.com.tr'de gizli sekmede aynı 6 sorguyu elle bakması önerilir.
- **Yapısal not (önemli):** Site tek URL'de iki dil sunuyor (dil `?lang=`, çerez ya da `Accept-Language`'den seçiliyor, `app/render.py::resolve_lang`). `base.html` canonical'ı `?lang`'sız yola veriyor. Yani **EN sorgular için ayrı bir URL yok**; EN hedefleri pratikte yalnız başlık/meta'daki EN ibareler ve içerikteki EN özetle desteklenebilir. `[fact-check]` Google'ın hreflang + canonical davranışı SEO bilgisi olan biri/Search Central dokümanıyla doğrulanmalı (§4-3).
- Japonca yazım: sitedeki mevcut tutarlılığa uyuldu (makronsuz: `jodo`, `iaido`, `kendo`). Başlıklarda makron kullanılmadı, arama sorguları da genellikle makronsuz yazılıyor (tahmin).
- Başlık sonuna `| Joryu` eklendi (7 karakter). Tüm title ≤60, meta ≤155 karakter; uzunluklar yazıldıktan sonra betikle sayıldı (§6).

---

## 1. Sayfa türü tabloları

### 1.1 Hub sayfaları

| URL | TR hedef sorgu | EN hedef sorgu | Niyet | Rakip durumu | Title | Meta description | H1 |
|---|---|---|---|---|---|---|---|
| `/` | joryu, jo bokken kata uygulaması | jo bokken kata practice app | Marka / keşif | Kontrol edilmedi (marka sorgusu; rakip beklenmez) | Joryu: Jo, Bokken ve Kata Pratik Takibi | Jo, bokken ve kata için ücretsiz pratik yoldaşı: günlük takip, kata ve teknik kütüphanesi, herkese açık pratisyen profili. | (mevcut) |
| `/guide` | dövüş sanatları kata rehberi, japon silah sanatları rehberi | martial arts kata guide jo bokken iaido | Bilgi / keşif | Kontrol edilmedi | Kata ve Teknik Rehberi: 9 Branş \| Joryu | Aiki-jo, jodo, iaido, kendo, aikido, karate ve taekwondo için kata listeleri ve sıfırdan başlangıç programları. Ücretsiz. | Branş rehberleri |
| `/kata` | kata listesi, kata kütüphanesi | kata library jo iaido kendo | Bilgi / gezinme | Kontrol edilmedi | Kata Kütüphanesi: Jo, Iaido, Kendo, Aikido \| Joryu | Branşa göre filtrelenen kata ve teknik kütüphanesi: aiki-jo, jodo, bokken, iaido, kendo, aikido, karate, taekwondo. | Kata kütüphanesi |
| `/blog` | jo bokken kata yazıları, dövüş sanatı blog | jo bokken kata blog | Bilgi | Kontrol edilmedi | Blog: Jo, Bokken ve Kata Yazıları \| Joryu | Pratisyenlerden jo, bokken, iaido, kendo ve karate üzerine yazılar: başlangıç ipuçları, kavramlar, çalışma yöntemleri. | Blog |

Not: `/` ve `/blog` meta metinlerindeki "Pratisyenlerden" ifadesi mevcut içeriğe (kullanıcı yazıları) dayanıyor; demo hesaplardan seed edilen yazılar için B-04'te belirtilen şeffaflık kuralı geçerli (§5-5).

### 1.2 Branş rehberleri (`/guide/<branş>`)

Genel gerekçe: Rehber sayfaları "X nedir / X nasıl çalışılır / X kata listesi" niyetini karşılıyor; en güçlü kozumuz **tek başına çalışan için başlangıç programı kutusu** (guide_content.py `PROGRAMS`). Bu, rakiplerde (dojo siteleri) pek görülmeyen bir fayda; ancak aramada ölçülmedi, tahmin.

| URL | TR hedef sorgu | EN hedef sorgu | Niyet | Rakip durumu | Title | Meta description | H1 | Tahmini öncelik |
|---|---|---|---|---|---|---|---|---|
| `/guide/aikijo` | aiki jo nedir, aiki jo suburi, jo kata | aiki jo kata, aiki jo suburi, 31 jo kata | Bilgi + öğrenme | EN: dojo/bireysel siteler güçlü (31 jo kata aramasında pbworks, stenudd, aikidoaus çıktı). TR: kontrol edilmedi | Aiki-jo Rehberi: Suburi, 13 ve 31 Jo Kata \| Joryu | Aiki-jo nedir? 20 suburi, 13'lü ve 31'li kata ve tek başına çalışanlar için haftalık başlangıç programı. | Aiki-jo: suburi ve kata rehberi | Yüksek (site bu branşta en dolu içerik, blogda 3 yazı bağlı) |
| `/guide/bokken` | bokken nedir, bokken suburi, bokken nasıl kullanılır | bokken suburi, how to practice with bokken | Bilgi + öğrenme | TR rehber bulunamadı (bokken seçimi araması TR'de mağaza/forum yönlendirdi, çoğu EN). Kontrol edilmedi: suburi | Bokken Rehberi: Suburi ve Kamae Başlangıcı \| Joryu | Bokken ile başlarken: ichi no suburi, kamae çeşitleri ve ilk 12 hafta için basit bir çalışma programı. | Bokken: suburi ve kamae rehberi | Yüksek (TR boşluk işareti) |
| `/guide/aikido` | aikido teknikleri, ikkyo nikyo sankyo, aikido ukemi | aikido techniques list, ikkyo nikyo sankyo | Bilgi | Kontrol edilmedi. Geniş, rekabetçi bir konu (tahmin) | Aikido Teknikleri Listesi: Ukemi ve Kyu Teknikleri \| Joryu | Aikido temel teknikleri: ukemi, ikkyo'dan gokyo'ya kontroller, nage waza. Kısa özet ve terim sözlüğü. | Aikido: temel teknikler | Orta (rekabet yoğun tahmini, ayrışma zor) |
| `/guide/jodo` | seitei jodo, jodo kata listesi, jodo kihon | seitei jodo 12 kata list, jodo kihon | Bilgi | EN: Wikipedia, karlgeis.com, kampaibudokai, jodokaiaustralia çıktı (bilgi sayfaları dağınık). TR: kontrol edilmedi, rakip beklenmiyor (tahmin) | Seitei Jodo: 12 Kihon ve 12 Kata Listesi \| Joryu | ZNKR Seitei Jodo müfredatı: 12 kihon ve 12 kata isim sırasıyla, tek başına çalışma önerisi. | Seitei Jodo: kihon ve kata listesi | Yüksek (TR boşluk + niyet net) `[fact-check]` |
| `/guide/kenjutsu` | kenjutsu nedir, kenjutsu kata | kenjutsu kata, what is kenjutsu | Bilgi | EN: Wikipedia, kendo-guide, mağaza blogları. TR: arama Türkçe özet sunabiliyor ama kaynaklar blog/ansiklopedi | Kenjutsu Nedir? Kata ve Başlangıç Yolu \| Joryu | Kenjutsu okul bazlı klasik kılıç sanatıdır. Okulsuz çalışanlar için Iaido ve Kendo katalarıyla bağlantılı bir yol. | Kenjutsu: nedir, nereden başlanır | Orta |
| `/guide/kendo` | kendo nedir, kendo kata, nihon kendo kata | nihon kendo kata, kendo basics suburi | Bilgi | Ankara Kendo gibi Türkçe kulüp dokümanları var (arama sonucunda göründü). Kontrol edilmedi: kata | Kendo: Nihon Kendo Kata ve Temel Vuruşlar \| Joryu | Kendo temelleri (men, kote, do, tsuki, suburi) ve Nihon Kendo Kata'nın 7 tachi + 3 kodachi formu. Kısa özetler. | Kendo: temel vuruşlar ve kata | Orta `[fact-check]` |
| `/guide/iaido` | iaido nedir, seitei iai kata listesi, iaido nukitsuke | seitei iai 12 forms, iaido kata list | Bilgi | EN: Wikipedia, kampaibudokai, ZNKR PDF aynaları çıktı; tam isim listesi tek kaynakta bulunamadı (zayıf kaynak karmaşası). TR: kontrol edilmedi | Seitei Iai: 12 Kata Listesi ve Temel Kavramlar \| Joryu | ZNKR Seitei Iai'nin 12 formu: Mae'den Nukiuchi'ye isim sırası, nukitsuke, chiburi ve noto kavramları. | Seitei Iai: 12 kata listesi | Yüksek (TR boşluk + sorgu net) `[fact-check]` |
| `/guide/karate` | shotokan kata listesi, heian shodan, karate kata sırası | shotokan kata list, heian shodan | Bilgi | TR: arama Türkçe adım adım anlatım **bulamadı**; EN'de çok sayıda dojo sayfası var, ağır rekabet (tahmin). | Shotokan Kata Listesi: Taikyoku'dan Heian'a \| Joryu | Shotokan'ın ilk katalarını öğren: Taikyoku Shodan, Heian Shodan–Godan, tek çizgilik Tekki. Hareket sayısı ve yeni teknikler. | Karate: Shotokan kata rehberi | Orta (EN ağır; TR boş olabilir) `[fact-check]` |
| `/guide/taekwondo` | taegeuk poomsae sırası, taekwondo poomsae listesi | taegeuk poomsae list, taekwondo forms | Bilgi | Kontrol edilmedi | Taekwondo Poomsae: Taegeuk 1-8 ve Siyah Kuşak \| Joryu | Taegeuk 1-8, Koryo ve devamı: poomsae isimleri, temsil ettikleri öğeler ve her formda eklenen teknikler. | Taekwondo: Taegeuk poomsae rehberi | Orta |

### 1.3 Kata detay sayfaları (`/kata/<slug>`)

Sitemap'te 100+ kata sayfası var. **Hepsi için ayrı satır yazmak yerine** üç katman: (a) öncelikli tekil sayfalar, (b) otomatik üretilebilir kalıplar (B-06 şablonuna girecek), (c) kapsam dışı.

**Mevcut durum (kod):** `kata_detail.html` title'ı `{{ kata_title }} — {branş} — Joryu`, H1 `{{ kata_title }}`; kata/rehber/blog şablonlarında `meta_description` bloğu **yok**, her sayfa `base.html`'deki genel açıklamayı alıyor (grep ile doğrulandı). Yani meta tarafında en büyük kazanım basit bir şablon değişikliği.

#### (a) Öncelikli tekil sayfalar

Seçim ölçütü: arama niyeti net, ayrı sorgu olarak aranan (yüksek) ve sayfamız için rekabeti düşük olabilecek adlar. Hepsi tahmini.

| URL | TR hedef sorgu | EN hedef sorgu | Niyet | Rakip durumu | Title | Meta description | H1 | Öncelik |
|---|---|---|---|---|---|---|---|---|
| `/kata/sanjuichi-no-jo` | 31 jo kata, aiki jo 31 kata | 31 jo kata | Öğrenme | EN güçlü: pbworks, stenudd, aikidoaus, aikidojournal (6 aramanın en kalabalık sonucu). TR: kontrol edilmedi | 31 No Jo Kata: Aiki-jo Solo Formu \| Joryu | Aiki-jo'nun 31 sayılık solo katası: ne işe yarar, nasıl bölünerek çalışılır, hangi suburilerle ısınılır. | 31 no jo kata | Yüksek (ana sorgu, ama EN'de zor) |
| `/kata/jusan-no-jo` | 13 jo kata | 13 jo kata aikido | Öğrenme | Kontrol edilmedi (EN'de 31'e göre benzer yapı bekleniyor, tahmin) | 13 No Jo Kata: Kompakt Aiki-jo Formu \| Joryu | Aiki-jo'nun 13 sayılık solo katası: ritim odaklı kısa form. Sayıyı sesli say, suburilerle birlikte çalış. | 13 no jo kata | Yüksek `[fact-check]` (sıralama: §3-4) |
| `/kata/aikijo-happo-giri` | happo giri, jo happo giri | happo giri jo | Öğrenme | Kontrol edilmedi | Happo Giri: 8 Yöne Kesiş Çalışması \| Joryu | Happo giri sekiz yöne sırayla kesiş çalışmasıdır: ayak çalışması ve denge için basit bir tekrar planı. | Happo giri | Orta |
| `/kata/jodo-tsukizue` | seitei jodo tsuki zue | seitei jodo tsuki zue | Öğrenme | EN: dağınık listeler (karlgeis, kampaibudokai). Tek kata sayfaları nadir (tahmin) | Seitei Jodo 1. Kata: Tsuki Zue \| Joryu | Seitei Jodo'nun ilk katası Tsuki Zue: tachi ve jo rollerinin özeti, tek başına çalışırken dikkat edilecekler. | Seitei Jodo: Tsuki Zue | Orta `[fact-check]` (kata numarası) |
| `/kata/jodo-kasumi` | jodo kasumi | jodo kasumi kata | Öğrenme | Kontrol edilmedi | Seitei Jodo Kasumi: Sis Katası \| Joryu | Kasumi "sis" katasıdır: jo görüşü perdeler, rakip niyeti okuyamaz. Seitei Jodo içindeki yeri ve çalışma notu. | Seitei Jodo: Kasumi | Orta |
| `/kata/jodo-ran-ai` | jodo ran ai | jodo ran ai | Öğrenme | Kontrol edilmedi | Seitei Jodo Ran-ai: Final Katası \| Joryu | Ran-ai, Seitei Jodo'nun uzun final katasıdır; 12 kihonun neredeyse tamamını tek senaryoda toplar. | Seitei Jodo: Ran-ai | Düşük-orta `[fact-check]` |
| `/kata/jodo-kihon-honte-uchi` | jodo kihon honte uchi | jodo kihon honte uchi | Öğrenme | Kontrol edilmedi | Jodo Kihon: Honte Uchi \| Joryu | Honte uchi, Seitei Jodo kihon setinin ilk tekniğidir. Kısa tanım, tek başına çalışma önerisi. | Jodo kihon: Honte uchi | Orta `[fact-check]` |
| `/kata/kendo-kata-1` | nihon kendo kata 1 tachi, ipponme | nihon kendo kata ipponme | Öğrenme | Kontrol edilmedi | Nihon Kendo Kata 1. Tachi: Ipponme \| Joryu | Nihon Kendo Kata'nın birinci formu: uchidachi/shidachi rolleri ve temel kesiş yapısının kısa özeti. | Nihon Kendo Kata 1 | Orta `[fact-check]` |
| `/kata/kendo-kirikaeshi` | kirikaeshi nasıl yapılır | kirikaeshi kendo | Öğrenme / uygulama | Kontrol edilmedi | Kirikaeshi: Kendo'nun Temel Alıştırması \| Joryu | Kirikaeshi, ardışık sol-sağ men kesişiyle ritim, mesafe ve nefes çalışmasıdır. Tek başına hazırlık ipuçları. | Kirikaeshi | Orta `[fact-check]` |
| `/kata/iaido-mae` | iaido mae, seitei iai mae | iaido mae seitei iai form 1 | Öğrenme | EN: Wikipedia + ZNKR aynaları; Seitei listelerinde isim geçiyor | Seitei Iai 1. Form: Mae \| Joryu | Mae, Seitei Iai'nin ilk formu: seiza'dan öne yatay nukitsuke ve dikey kirioroshi. | Seitei Iai: Mae | Yüksek (set'in giriş formu) `[fact-check]` |
| `/kata/iaido-ukenagashi` | iaido ukenagashi | iaido ukenagashi seitei | Öğrenme | Kontrol edilmedi | Seitei Iai Ukenagashi: Akıtarak Savuşturma \| Joryu | Ukenagashi: kesişi kılıçla akıtıp tek hareketle karşı kesiş. Ritim ve mesafe ipuçları. | Seitei Iai: Ukenagashi | Orta |
| `/kata/iaido-nukitsuke` | nukitsuke nedir | nukitsuke iaido draw | Kavram | Kontrol edilmedi (blogda ilgili yazı var) | Nukitsuke: Iaido'da Çekiş ve Kesiş \| Joryu | Nukitsuke, kılıcın kınından çekilirken yapılan ilk kesiştir. Hız yanılsaması ve temel hata notları. | Nukitsuke | Orta |
| `/kata/aikido-ikkyo` | ikkyo nasıl yapılır | ikkyo aikido technique | Öğrenme | Kontrol edilmedi. Kalabalık sorgu (tahmin) | Ikkyo: Aikido'nun İlk Kontrolü \| Joryu | Ikkyo, aikidonun temel kontrol tekniğidir. Kısa tanım, dikkat noktaları; uygulama için hocana danış. | Ikkyo | Düşük-orta (rekabet) |
| `/kata/karate-heian-shodan` | heian shodan, heian shodan kata | heian shodan | Öğrenme | TR adım adım anlatım bulunamadı; EN'de çok sayıda dojo/YouTube sayfası, ağır rekabet | Heian Shodan: Shotokan'ın İlk Katası \| Joryu | Heian Shodan: 21 hareket, yeni teknikler (shuto uke, age uke, kokutsu dachi) ve I biçimli embusen özeti. | Heian Shodan | Yüksek (TR) / düşük (EN) `[fact-check]` |
| `/kata/karate-taikyoku-shodan` | taikyoku shodan | taikyoku shodan | Öğrenme | Kontrol edilmedi | Taikyoku Shodan: İlk Shotokan Katası \| Joryu | Taikyoku Shodan: gedan barai + oi tsuki ile H biçimli embusen. Dönüşleri öğrenmenin en temiz yolu. | Taikyoku Shodan | Orta `[fact-check]` |
| `/kata/tkd-taegeuk-1` | taegeuk il jang, 1. poomsae | taegeuk il jang | Öğrenme | Kontrol edilmedi | Taegeuk Il Jang: 1. Poomsae \| Joryu | Taegeuk Il Jang (Keon, gök): temel duruşlar ve ilk poomsae. Hareket planı ve çalışma notları. | Taegeuk Il Jang | Orta `[fact-check]` |

Not: Karate ve taekwondo kata sayfaları **canlıda 200 dönüyor** (`/kata/karate-heian-shodan`, `/kata/tkd-taegeuk-1` kontrol edildi) ama **sitemap'te yok**; sebep büyük olasılıkla `SELECTABLE_DISCIPLINES` filtresi (`app/constants.py:19`, kullanımı `landing.py` civarı). Bkz. §4-4.

#### (b) Otomatik kalıplar (B-06 şablonuna)

Sayfaya özel başlık yazmak yerine alanlardan üretilebilen kalıplar. Branş adı için `t["discipline_<d>"]` zaten var.

| Grup (slug deseni) | Title kalıbı (≤60) | Meta kalıbı (≤155) | H1 kalıbı | Notlar |
|---|---|---|---|---|
| `jodo-*` (12 kata, ör. `jodo-suigetsu`, `jodo-hissage`, `jodo-shamen`, `jodo-sakan`, `jodo-monomi`, `jodo-tachi-otoshi`, `jodo-rai-uchi`, `jodo-seigan`, `jodo-midare-dome`) | `Seitei Jodo {n}. Kata: {ad} \| Joryu` | `{description_tr, 150'ye kısalt}` (mevcut kata açıklamaları ör. "Suigetsu (solar plexus) noktasına tek dürtüş" bu iş için yeterli) | `Seitei Jodo: {ad}` | `{n}` kata sırası için `[fact-check]`; sırayı DB'den çıkaracak bir alan yoksa numarasız yaz: `Seitei Jodo {ad} Katası` |
| `jodo-kihon-*` (12 kihon) | `Jodo Kihon: {ad} \| Joryu` | description_tr | `Jodo kihon: {ad}` | Ana sorgu "jodo kihon" + teknik adı |
| `iaido-*` (12 seitei form + temel kavram sayfaları) | `Seitei Iai {n}. Form: {ad} \| Joryu` (form sayfaları) / `Iaido {ad}: Kavram \| Joryu` (nukitsuke, chiburi, noto) | description_tr | `Seitei Iai: {ad}` | Form sırası `[fact-check]` |
| `kendo-kata-1..7`, `kendo-kodachi-1..3` | `Nihon Kendo Kata {n}. Tachi \| Joryu` / `Nihon Kendo Kata Kodachi {n} \| Joryu` | description_tr | `Nihon Kendo Kata {n}` | ZNKR yayını esas `[fact-check]` |
| `kendo-*` temel vuruşlar | `Kendo {ad}: Temel Vuruş \| Joryu` | description_tr | `Kendo {ad}` | men, kote, do, tsuki, suburi, fumikomi, okuri ashi |
| `aiki-ken-suburi-*`, `bokken-*` | `Aiki-ken {n}. Suburi \| Joryu` / `Bokken {ad} \| Joryu` | description_tr | `Aiki-ken suburi {n}` | Blog "Yedi suburi" yazısına iç link |
| `aikido-*` | `{Ad}: Aikido Tekniği \| Joryu` | description_tr + "hocana danış" notu | `{Ad}` | Güvenlik: sağlık tavsiyesi yazılmaz (CONTENT_STANDARDS) |
| `karate-*`, `tkd-*` | `{Ad}: {Shotokan Kata \| Poomsae} \| Joryu` | description_tr | `{Ad}` | Sitemap'e eklenince anlam kazanır |
| Aiki-jo suburi teknikleri (`choku-tsuki`, `kaeshi-tsuki`, `ushiro-tsuki`, `tsuki-gedan-gaeshi`, `tsuki-jodan-gaeshi`, `shomen-uchikomi`, `renzoku-uchikomi`, `katate-*`, `hasso-gaeshi-*`, `menuchi-*`, `nagare-gaeshi-*` vb.) | `Aiki-jo {ad}: Suburi Tekniği \| Joryu` | description_tr | `{Ad}` | Slug'lar genel (`choku-tsuki` branşsız) → title'daki "Aiki-jo" şart, aksi halde belirsiz |

Tahmini öncelik (b grubu): **düşük-orta**. Tek tek sayfalar uzun kuyruklu ve adlandırma tutarlılığıyla toplam trafik getirebilir; gelir tahmini yok, 4 haftalık GSC verisi gerekli.

#### (c) Kapsam dışı / dikkat

- Bazı slug'lar diğerleriyle çakışacak kadar genel (`choku-tsuki`, `ushiro-tsuki`, `kaeshi-tsuki`, `shomen-uchikomi`). Başka branşlarda da aynı terim var; title'a branş şart (yukarıda).
- Kata sayfalarında adım adım döküm yok (özet düzeyi), CONTENT_STANDARDS ile uyumlu. "X nasıl yapılır / adım adım" niyetli sorgulara bu sayfalar tam cevap vermiyor; bu yüzden **"nasıl yapılır" ifadesi title'a konmadı**. Hocana danış çerçevesi korunsun.

### 1.4 Blog yazıları (`/blog/<slug>`)

Mevcut canlı URL'ler (blog listesinden). Slug'lar başlıktan + rastgele uuid son ekle üretilmiş (`app/routers/blog.py::_slugify`); **slug'ı değiştirme** (indekslenmiş URL, iç link kırılır). Başlık etiketi ile H1 ayrı olabilir.

| URL | TR hedef sorgu | EN hedef sorgu | Niyet | Rakip durumu | Title | Meta description | H1 (mevcut korunur) | Öncelik |
|---|---|---|---|---|---|---|---|---|
| `/blog/jo-nedir-dort-seftali-agacindan-dojoya-ff6314` | jo nedir, jo sopası, jo uzunluğu | what is a jo staff, jo staff length | Bilgi | Kontrol edilmedi | Jo Nedir? Uzunluk, Ağaç ve İlk Jo Seçimi \| Joryu | Jo, yaklaşık 128 cm'lik Japon sopasıdır. Kısa tarihi, jodo ile aiki-jo farkı ve ilk jo'yu seçerken dikkat edilecekler. | Jo Nedir? Dört Şeftali Ağacından Dojoya | Yüksek (temel sorgu; ölçü bilgisi `[fact-check]`) |
| `/blog/aiki-jo-nun-20-suburi-si-aikidoyu-sopayla-anlamak-4356de` | aiki jo 20 suburi, saito jo suburi | aiki jo 20 suburi | Bilgi | Kontrol edilmedi | Aiki-jo'nun 20 Suburi'si: Sopayla Aikido \| Joryu | Saito'nun derlediği 20 suburi: tsuki, uchikomi, katate, hasso gaeshi grupları ve tek başına çalışma düzeni. | Aiki-jo'nun 20 Suburi'si: Aikidoyu Sopayla Anlamak | Orta `[fact-check]` |
| `/blog/jodo-ve-jojutsu-ayni-silah-iki-farkli-yol-6347fe` | jodo ile jojutsu farkı | jodo vs jojutsu | Karşılaştırma | EN'de Wikipedia/dojo karşılaştırmaları (tahmin); kontrol edilmedi | Jodo ve Jojutsu Farkı: Aynı Silah, İki Yol \| Joryu | Jodo ve jojutsu aynı kökten gelir ama farklı hedefleri vardır. Seitei Jodo ve Shinto Muso-ryu arasındaki fark. | Jodo ve Jojutsu: Aynı Silah, İki Farklı Yol | Orta `[fact-check]` |
| `/blog/kenjutsu-nedir-kendo-dan-farki-ne-4c99c1` | kenjutsu nedir, kenjutsu kendo farkı | kenjutsu vs kendo | Karşılaştırma | EN: Wikipedia, kendo-guide, mağaza blogları. TR: sonuçlar blog/ansiklopedi; kendo kulüp dokümanı var | Kenjutsu Nedir? Kendo'dan Farkı Ne? \| Joryu | Kenjutsu klasik okul geleneği, kendo ise shinai ve zırhlı modern spordur. Farklar, kesişen noktalar ve nereden başlanır. | Kenjutsu Nedir, Kendo'dan Farkı Ne? | Yüksek (sorgu net, TR aranabilir) |
| `/blog/aiki-ken-e-baslarken-yedi-suburi-neden-bu-kadar-onemli-10ff68` | aiki ken suburi, aikido bokken suburi | aiki ken suburi | Bilgi | Kontrol edilmedi | Aiki-ken'e Başlarken: 7 Suburi Rehberi \| Joryu | Aikido bokken çalışmasının temeli yedi suburi: ne işe yarar, hangi sırayla öğrenilir, ayna ve tekrar önerileri. | Aiki-ken'e Başlarken: Yedi Suburi Neden Bu Kadar Önemli? | Yüksek (Hedef sorgu: "aiki ken suburi" growth-marketer rol dosyasında da öncelikli) `[fact-check]` |
| `/blog/iaido-da-nukitsuke-hiz-yanilsamasi-43267e` | nukitsuke nedir, iaido çekiş | nukitsuke iaido | Kavram | Kontrol edilmedi | Nukitsuke: Iaido'da Hız Yanılsaması \| Joryu | Iaido'da hızlı çekişin ardındaki yanılsama: mesafe, zamanlama ve çekişte sık yapılan hatalar. | Iaido'da Nukitsuke: Hız Yanılsaması | Orta |
| `/blog/poomsae-calisirken-gozden-kacan-uc-detay-a3042e` | poomsae nasıl çalışılır, poomsae ipuçları | poomsae practice tips | Bilgi | Kontrol edilmedi | Poomsae Çalışırken Gözden Kaçan 3 Detay \| Joryu | Taekwondo poomsae çalışırken sık atlanan üç detay: duruş genişliği, bakış ve nefes. Kısa kontrol listesi. | Poomsae Çalışırken Gözden Kaçan Üç Detay | Düşük-orta (site ağırlıklı jo/bokken, tahmin) |
| `/blog/dachi-karatenin-temeli-ayaklarda-kurulur-76bd8b` | karate duruşları, dachi çeşitleri, zenkutsu dachi | karate stances dachi | Bilgi | Kontrol edilmedi. Geniş konu (tahmin) | Karate Duruşları (Dachi): Temel Ayakta Kurulur \| Joryu | Zenkutsu, kiba, kokutsu: karate duruşlarının (dachi) mantığı, yaygın hatalar ve ev çalışması önerileri. | Dachi: Karatenin Temeli Ayaklarda Kurulur | Düşük-orta |

Uyarı: Blog yazılarının metinleri bu turda **okunmadı**; meta description'lar başlıklara ve `scripts/seed_blog.py` başlıklarına dayanıyor (Jo yazısı için gövdeden ilk 40 satır okundu: 128 cm, shiro kashi, 24-26 mm geçiyor). Yayına girmeden önce her meta cümlenin gövdeyle uyumu kontrol edilmeli, aksi halde "gövdede olmayan şeyi vaat eden meta" riski var. Bu yazılar `seed_blog.py` ile demo hesaplardan (kenshin-yolda vb.) giriyor; B-04 şeffaflık notu geçerli.

---

## 2. En iyi 5 içerik boşluğu (B-13 aday yazıları)

Ölçüt: (1) niyeti net, (2) TR'de arama aracının net bir rehber **bulamadığı** ya da sonuçları dağınık gördüğü, (3) sitemizde zaten veri/taban olan, (4) CONTENT_STANDARDS'a uygun yazılabilir (adım adım döküm gerektirmeden, resmi kaynakla). Hepsi **tahmini** önceliktir; hacim ölçülmedi.

| # | Aday yazı (TR başlık) | Hedef sorgu TR / EN | Neden | Doğruluk riski ve kaynak |
|---|---|---|---|---|
| 1 | **Seitei Jodo 12 kata ve 12 kihon: liste ve sıra** | seitei jodo kata listesi / seitei jodo 12 kata list | 6 aramada EN'de bilgi dağınık (karlgeis, Wikipedia, jodokaiaustralia) ve kaynaklar kata sırasını farklı yazıyor; TR'de derli toplu bir liste görmedik. Sitede 12 kihon + 12 kata sayfası zaten var: yazı onlara iç link veren bir **hub** olur. Sadece isim/sıra, adım adım döküm yok. | Orta. Kaynaklar sıra konusunda çelişti (bir kaynakta Kasumi 7., diğerinde farklı sıra): **ZNKR resmi Seitei Jodo kitapçığı** ile doğrulanmalı. Çelişiyorsa iki sırayı da yazıp belirt (CONTENT_STANDARDS kuralı). `[fact-check]` |
| 2 | **Seitei Iai 12 kata: isimler ve gruplar (seiza / tatehiza / tachi)** | seitei iai kata listesi / seitei iai 12 forms list | Aramada **tam bir listeyi tek kaynakta bulamadık**; bir kaynak yalnız ilk beşi, bir başkası yalnız 9, 10 ve 12'yi verdi. Boşluk net. Sitede iaido kata sayfaları (mae, ushiro, ukenagashi…) hazır. Resmi kaynak (AJKF/ZNKR İngilizce kılavuzu, 5. baskı 2014) mevcut. | Orta. Şu anki site liste sırası ile arama sonuçları arasında bir tutarsızlık görmedik, ama bu turda aramalardan tam liste çıkmadı; **doğrulama ZNKR kılavuzundan yapılmalı**. `[fact-check]` |
| 3 | **Bokken nasıl seçilir? Boy, ağaç, ağırlık, tsuba** | bokken nasıl seçilir / how to choose a bokken | TR sorgusu aramada **İngilizce mağaza sayfalarına** gitti; Türkçe bir rehber bulunamadı. Blogda jo seçimi yazısı var (ölçü, ağaç, çap), bokken'in karşılığı yok. Kolay yazılır, düşük doğruluk riski. Bağlanacak yer: `/guide/bokken`. | Düşük-orta. Ölçüler kaynaklı yazılacak, **marka/affiliate linki yok** (BRIEF kapsam dışı). Aramada geçen "98-102 cm genel boy" gibi rakamlar mağaza kaynaklı: alınmadan önce güçlü kaynakla (kendo/aikido federasyonu, dojo) doğrulanmalı. `[fact-check]` |
| 4 | **13'lü mü, 31'li mi? Aiki-jo kata öğrenme sırası** | 13 jo mu 31 jo mu, aiki jo kata sırası / 13 jo kata vs 31 jo kata order | Niyet çok net ve kendi içeriğimizde **çelişki** var, bu yüzden hem fırsat hem risk. Rehber ve program 13'lüyü 31'den önce koyuyor; arama sonucu ise bir kaynakta 13'lünün 31'den sonra öğretildiğini yazıyor. Çelişkiyi açıkça anlatan bir yazı hem bizim güvenilirliğimizi korur hem de başka yerde bulunmayan bir cevap olur. | **Yüksek.** Önce `fact-checker` bu çelişkiyi çözmeli (Saito yayınları ve Iwama müfredatı kaynak). **Çözülmeden yazı yazılmasın**, rehberdeki mevcut sıra da bu denetimden sonra düzeltilmeli. `[fact-check]` |
| 5 | **Shotokan kata sırası: Taikyoku'dan Heian'a, hangi hareket yeni?** | shotokan kata sırası, heian shodan nedir / shotokan kata order | Aramada Heian Shodan için **Türkçe adım adım anlatım bulunamadı**; EN'de çok sayıda dojo sayfası var, yani niyet gerçek ama sadece TR'de fırsat olabilir. Sitede karate kataları ve hareket sayısı özetleri var. Tek hamlede 5 Heian + Taikyoku için iç link merkezi olur. Adım adım dizilim **yazılmaz**, "her katada hangi yeni teknik eklenir" yazılır. | Orta. Hareket sayıları (20, 21, 26, 20, 27, 23) rehberdeki ilk sürümden alınmış, kaynak hâlâ doğrulanmalı (JKA/Shotokan resmi yayını). "Hangi kuşakta" eşlemesi federasyona göre değişir: yazılmaz ya da belirtilir. `[fact-check]` |

Yedek adaylar (sıralama dışı): *Nihon Kendo Kata 7 tachi listesi*; *evde / balkonda jo ve bokken güvenli çalışma (tavan yüksekliği, tandoku dosa)*; *Taegeuk 1-8: hangi formda ne eklenir*.

---

## 3. Doğruluk işaretleri (çelişki ve riskler)

1. Seitei Jodo kata sırası kaynaklarda **tutarlı değil** (arama: iki kaynak aynı 12 ismi farklı sırada verdi). Sayfalarda `{n}. Kata` numarası ZNKR resmi sıra doğrulanana dek **konulmasın**.
2. Seitei Iai: arama sonuçlarının hiçbiri tam listeyi vermedi; site listesiyle karşılaştırma ZNKR kılavuzundan yapılmalı.
3. **Aiki-jo 13'lü / 31'li öğrenme sırası** çelişiyor (§2-4). Mevcut rehber metni ve program (`guide_content.py`, "13'lü kataya başla") denetlenmeli.
4. Heian/Taikyoku hareket sayıları (20/21/26/20/27/23) title ve meta'ya giriyor; meta'da 21'i yazdım, güçlü kaynak doğrulaması bekliyor.
5. Aramadaki Wikipedia aynaları ve dojo siteleri zayıf kaynak (CONTENT_STANDARDS kaynak hiyerarşisi 3-4); bu raporda hiçbir kata içeriği onlara dayandırılmadı, yalnız "rakip kim" bilgisi için kullanıldı.

---

## 4. Developer için uygulanabilir öneri listesi (B-06'nın devamı)

Öncelik sırasına göre. Hiçbiri bağımlılık eklemez.

1. **Sayfaya özel `meta_description` bloğu.** `kata_detail.html`, `guide_discipline.html`, `blog_post.html`'de blok yok → hepsi `default_meta_description` alıyor (grep ile doğrulandı). Kata için `description_tr/en` (kısalt ≤155), rehber için branş `intro` ilk cümleleri (≤155) ya da §1.2'deki metin, blog için gövdenin ilk paragrafı. Ek sorgu gerekmez, veriler zaten sayfada.
2. **Title kalıpları (§1.3b).** Mevcut `{kata} — {branş} — Joryu` yerine sorgu kelimesi öne: `Seitei Jodo Kasumi...`. Genel slug'larda (`choku-tsuki`, `ushiro-tsuki`) branş adı zorunlu. 60 karakter üstünü kırp. Brand son ekini `| Joryu` yap (7 karakter, tutarlı).
3. **hreflang / canonical tutarsızlığı kontrolü.** `base.html` satır 15-18: canonical `?lang`'sız yol; `hreflang="tr"` ve `"en"` ise `?lang=tr` / `?lang=en` URL'lerini gösteriyor (aynı yol, farklı sorgu). Bu iki URL canonical olarak kendilerini değil, sorgusuz yolu gösterdiği için hreflang işlevsiz olabilir. `[fact-check]` Google Search Central "localized versions" dokümanıyla doğrulanmalı; çözüm ya dil başına ayrı URL (`/en/...`) ya da hreflang'ın kaldırılması olabilir, bu bir mimari karar, B-06 kapsamı dışında kalabilir. İlteriş'e sorulacak.
4. **Sitemap tamamlama.**
   - Blog yazıları sitemap'te **yok** (150 URL'den yalnız `/blog` listesi var).
   - Karate ve taekwondo kata sayfaları canlıda 200 ama sitemap'te yok (`landing.py` civarı `SELECTABLE_DISCIPLINES`'a göre üretilmiş, `app/constants.py:19`). Bu bilinçli mi? (Muhtemelen "kayıt sırasında seçilebilir branş" listesi sitemap'e yanlışlıkla taşınmış.) Karar İlteriş'te.
   - `<lastmod>` eklenebilir (Post.updated_at / created_at).
5. **İç link.**
   - Kata detay → branş rehberi (breadcrumb) + önceki/sonraki kata (aynı branş, sıraya göre).
   - Rehber → ilgili blog yazıları (blog `discipline` alanı var).
   - Blog → `Post.discipline` rehberi + ilgili 2-3 kata (aynı branş).
   - Bunlar sayfa başına en fazla 1 ek sorgu bütçesi içinde yapılabilir (SPRINT.md B-06 sınırı).
6. **H1.** Kata H1'i yalnız `kata_title`; genel adlarda (Seigan, Kasumi, Hissage) branş ibaresi H1'e de girsin (§1.3b). Rehber H1 şu an yalnız branş adı; "rehberi" ekle.
7. **JSON-LD:** Article (blog), BreadcrumbList (kata/rehber/blog), B-06 zaten kapsıyor. `HowTo` ekleme: bu turda doğrulanmadı ama Google'ın HowTo zengin sonucunu kısıtladığı biliniyor `[fact-check]`, kazanç beklenmiyor. Sayfaların gövdesinde adım adım döküm de olmadığı için uygun değil.
8. **Blog slug.** Uuid son eki (`_slugify`) yeni bir yazıda her seferinde farklı üretiyor; yazı taşınırsa/yeniden seed edilirse URL değişir. Slug'ı kayıtta sabit tut (zaten DB'de), seed'de aynı başlık varsa atlanıyor (kontrol edildi: `Post.title ==`), bir değişiklik gerekmiyor, sadece **slug'a dokunulmaması** notu.
9. **Önce ölçüm:** Deploy sonrası GSC'de "Sayfalar" raporuna `/kata/`, `/guide/`, `/blog/` için ayrı filtre kaydet (4 hafta referans, SPRINT.md başarı ölçütü). Bu rapordaki "öncelik" sütunları o veriyle yeniden sıralanmalı.

---

## 5. `fact-checker` listesi

1. §1.2 `/guide/jodo`: "12 kihon ve 12 kata", ZNKR; `/guide/iaido`: "12 form, Mae'den Nukiuchi'ye"; `/guide/kendo`: "7 tachi + 3 kodachi".
2. §1.2 `/guide/karate`: Tekki'nin tek çizgilik (embusen) olduğu; Heian Shodan 21 hareket, Taikyoku Shodan H biçimli embusen (title/meta'ya giriyor).
3. §1.3a: Kata numaraları (Tsuki Zue 1. kata, Mae 1. form); 13 no jo "başlangıç".
4. §1.4 jo ölçüsü (128 cm, 24-26 mm, beyaz meşe) ve Saito 20 suburi gruplama meta'ları.
5. §3 çelişki maddeleri 1-3.
6. Teknik SEO (§0 hreflang/canonical, §4-3, §4-7): SEO bilgisi olan biri / Google Search Central doğrulaması.

## 6. Karakter denetimi

Hub, rehber, öncelikli kata ve blog tablolarındaki 38 title ve meta çifti betikle sayıldı: en uzun title 58 karakter, en uzun meta 124 karakter; hiçbiri sınırı aşmıyor. §1.3b'deki kalıplar sayılmadı, kalıbı dolduran gerçek başlıklar B-06'da üretildikten sonra kırpma (≤60) uygulanmalı.

---

## 7. Bu iş için sınırlar

- Arama hacmi, tıklama oranı, sıralama konumu **ölçülmedi**; hiçbiri uydurulmadı.
- Rakip bilgisi 6 aramaya dayanıyor, ABD sonuçları, Türkiye farklı olabilir.
- Kodda, DB'de, GSC'de hiçbir değişiklik yapılmadı, hiçbir yere paylaşım/mesaj gönderilmedi.
