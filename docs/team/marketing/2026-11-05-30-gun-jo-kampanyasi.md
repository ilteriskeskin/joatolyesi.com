# Instagram: "30 Günlük Jo Suburi Programı" kampanyası (B-21) — taslak

- Tarih: 2026-11-05 · Hazırlayan: growth-marketer · Durum: **taslak**. Hiçbir yere paylaşılmadı, paylaşımı İlteriş yapacak.
- Temel alınan: `2026-11-03-instagram-hunisi.md` (UTM kuralları §2, teşhis §1, ölçüm §7). Burada tekrar yazılmadı, yalnız bu kampanyaya özel kısımlar var.
- Program içeriği (app/seed.py: `WEEKS`, `_build_program_days`): 4 haftalık tema (Tsuki temelleri, Uchikomi vuruş haftası, Katate & hasso gaeshi, Nagare gaeshi). Her 7. gün tekrar günü. Normal gün: 5 dk ısınma + ana çalışma (3 set x 20 tekrar, son set daha yavaş) + seansı kaydet. Program açıklaması "günde yaklaşık 10-20 dk" diyor (fact-check 2026-11-05 sonrası).
- **Konumlandırma (PO kararı, 2026-11-05):** Program bir *ev çalışması planı*; hareketleri öğretmiyor. Hedef kitle, suburi'yi bir hocadan öğrenmiş ya da öğrenmekte olan ve dojo dışında düzenli çalışmak isteyenler. "Sıfırdan jo öğren", "dojo gerekmez", "hocasız" gibi ifadeler **kullanılmaz**.
- Rakam yok: kullanıcı sayısı, izlenme, "binlerce kişi" gibi iddia kullanılmadı. `<N>` gibi yerlere İlteriş **gerçek** değerini yazar.
- `[fact-check]`: bu belgede **hiç teknik dövüş sanatı iddiası yok**. Metinler yalnız programın yapısını (gün sayısı, süre, set/tekrar, hafta teması) anlatıyor, bunlar ürünün kendi içeriği. Tek not: programın hafta açıklamaları (program metni 2026-11-05'te fact-checker'dan geçti ve düzeltildi: content/verified/2026-11-05-30-gun-jo-programi.md). Kampanya metni bunlara teknik ayrıntı eklemiyor, ama sayfada ne yazıyorsa onun denetimi ayrı iş.

## 0. Başlamadan önce: iki bağımlılık (önemli)

1. **B-20 canlıya çıkmadan kampanya başlamamalı.** Mevcut kodda `/programs/...` yalnız `pro_enabled=True` iken register ediliyor (`app/main.py`) ve ayrıca `require_user` + `require_pro` ister: ziyaretçi `/login`'e, giriş yapan ama Pro olmayan `/billing`'e yönleniyor. Yani bugün bu URL ziyaretçiye açılış sayfası değil. B-20 (ziyaretçiye açık sayfa, ücretsiz) deploy edilince İlteriş şu 3 şeyi **telefondan, çıkış yapmış tarayıcıda** kontrol etsin: (a) sayfa açılıyor, (b) "ücretsiz" yazıyor, (c) kayıt CTA'sından sonra `next` ile programa dönüyor.
2. **UTM, giriş/kayıt yönlendirmesinde düşebilir.** `/register` ya da `/login` yönlendirmesi `utm_*` parametrelerini taşımazsa GA4 kaynağı kayıt anında "(direct)" görebilir. `sign_up` olayı için B-20 testine ekle: UTM'li linkten gel, kayıt ol, GA4 Gerçek zamanlı'da `sign_up` oturumunun kaynağına bak. Tutmuyorsa GA4 "ilk kullanıcı kaynağı" yine de yakalayabilir ama doğrulanmadı.

"Ücretsiz" sözü yalnız Pro kapalı olduğu sürece geçerli. Pro açılırsa tüm metinler (bio dahil) güncellenmeli.

---

## 1. Bio metni ve link

Karakter sayıları Python `len` ile, satır sonları dahil (≤150). Emoji yok.

**Seçenek A (önerilen):**

```
Dojo dışı 30 günlük jo suburi planı, ücretsiz ↓
Daily jo & bokken practice.
Aiki-jo · aiki-ken · solo pratik
```
(**115** karakter)

**Seçenek B:**

```
Jo ile 30 gün: bahçede, evde, dojo kapalıyken.
Ücretsiz program + günlük pratik kaydı ↓
Free 30-day jo program
```
(**110** karakter)

- **Bio linki:** `https://joatolyesi.com/programs/30-day-jo-suburi?utm_source=instagram&utm_medium=social&utm_campaign=bio`
- Bu link 11-03 taslağındaki bio linkinin (`/?...campaign=bio`) **yerine** geçer. Kampanya bitince (14 gün) ana sayfa linkine ya da `/kata?d=aikijo` deneyine dönülebilir.
- Bio linkini kopyala-yapıştır yap, elle yazma.

---

## 2. 14 günlük takvim

D1 = B-20 canlıya çıktıktan ve §0 kontrolleri geçtikten sonraki ilk gün. Her gün bir story (link çıkartmalı); tek sayı günleri ek olarak reels. Hepsi tek kişi, 15-45 sn, bahçe/ev.

**Story link çıkartması (her gün, N yerine gün numarası):**
`https://joatolyesi.com/programs/30-day-jo-suburi?utm_source=instagram&utm_medium=social&utm_campaign=story-30-gun-jo-dN`
(`utm_campaign` değeri: `story-30-gun-jo-d1` … `story-30-gun-jo-d14`; ≤20 karakter kuralına uyuyor.) Reels açıklamasına URL **yazma**: tıklanamaz. Reels'ın CTA'sı "link bio'da", aynı günkü story'nin çıkartması asıl tıklanan linktir.

Genel kural: ekran metni 8 kelimeyi geçmesin; ilk 2 sn'de metin ekranda olsun, ses açık olmasa da anlaşılsın.

| Gün | Biçim | Kanca (ilk 2 sn) | Ekran metni | Açıklama / story CTA (TR) | Story URL |
|---|---|---|---|---|---|
| D1 | Reels + story | Jo'yu kameraya doğru uzat, doğrudan konuş: "30 gün. Her gün jo." | "30 gün · dojo dışı çalışma · ücretsiz" | "Hocandan öğrendiğin suburi'yi dojo dışında düzenli çalışmak için 30 günlük plan. Günde yaklaşık 10-20 dakika, ücretsiz. Link bio'da." | `...campaign=story-30-gun-jo-d1` |
| D2 | Story | Telefon ekran kaydı: program sayfası kaydırılıyor | "Program böyle görünüyor" | "Dört hafta, her haftanın bir teması var. Sayfaya buradan bak." (sticker) | `...story-30-gun-jo-d2` |
| D3 | Reels + story | Ekranda "Gün 1" yazısı, jo yerden kalkıyor | "Gün 1: 5 dk ısınma, 3 set" | "Programın ilk günü böyle başlıyor: ısınma, sonra 3 set x 20 tekrar. Hepsi sitede, link bio'da." | `...story-30-gun-jo-d3` |
| D4 | Story | Kameraya: "Jo'yu en son ne zaman eline aldın?" + soru çıkartması | "En son ne zaman?" | "Cevabını yaz. 30 günlük programın linki burada." | `...story-30-gun-jo-d4` |
| D5 | Reels + story | Yavaş çekim bir tekrar, ekranda: "Son set ilkinden yavaş." | "Üçüncü set daha yavaş. Bilerek." | "Programda son set ilkinden yavaştır: hızdan önce isabet. Link bio'da." | `...story-30-gun-jo-d5` |
| D6 | Story | Kendi serini/ilerlemeni göster (telefon ekranı, gerçek) | "Gün <N>" | "Ben de çalışıyorum, her günü kaydediyorum. Sen de başla." (sticker) | `...story-30-gun-jo-d6` |
| D7 | Reels + story | Hafif tempoda tekrar: "Yeni bir şey yok. Sadece yavaş tekrar." | "7. gün: tekrar günü" | "Her yedinci gün tekrar günü: yarı hız, tam dikkat. Bütün plan sitede, link bio'da." | `...story-30-gun-jo-d7` |
| D8 | Story | İkinci hafta temasını göster: ekranda "Hafta 2: vuruş haftası" | "Hafta 2: uchikomi" | "İkinci hafta vuruşlara geçiyor. İlk haftayı kaçırdıysan hâlâ 1. günden başlayabilirsin." (sticker) | `...story-30-gun-jo-d8` |
| D9 | Reels + story | Ekranda "Hafta 2" yazısı, bir uchikomi tekrarı | "Hafta 2 başlıyor" | "Programın ikinci haftası: uchikomi. Günde yaklaşık 10-20 dakika. Link bio'da." | `...story-30-gun-jo-d9` |
| D10 | Story | Soru çıkartması: "30 gün sence en zor nerede kopar?" | "Nerede kopar?" | "Cevapla, sonra programın kayıt/seri takibini gör." (sticker) | `...story-30-gun-jo-d10` |
| D11 | Reels + story | Boş bahçe/oda planı, sonra jo: "Dojo günü değil mi? Çalışma yine de var." | "Dojo arası günler için" | "Dojo'da öğrendiğini evde, bahçede pekiştirmek için 10-20 dakikalık plan. Ücretsiz, link bio'da." | `...story-30-gun-jo-d11` |
| D12 | Story | Ekranda "Hafta 3: katate & hasso gaeshi" | "Hafta 3'e hazırlık" | "Üçüncü hafta geliyor. Şimdi başlarsan hafta hafta yetişirsin." (sticker) | `...story-30-gun-jo-d12` |
| D13 | Reels + story | **Yalnız gerçekten yapıyorsa:** "İki haftadır programdayım." + telefonda gerçek gün sayın | "Gün <N>: ne değişti?" | "İki hafta notum: <İlteriş kendi gözlemini tek cümleyle yazar>. Programı sen de başlat, link bio'da." | `...story-30-gun-jo-d13` |
| D14 | Story | Kameraya: "Bu hafta başlayan olursa 4. haftaya birlikte varırız." | "Hafta 4: nagare gaeshi" | "Son hafta nagare gaeshi ile bitiyor. Başlamak için link burada." (sticker) | `...story-30-gun-jo-d14` |

Notlar:
- D6 ve D13 İlteriş'in **gerçek** ilerlemesine bağlı. Programı gerçekten yapmıyorsa bu iki günü "program sayfası" ekran kaydıyla değiştir; "ben de yapıyorum" deme.
- D13 gözlemi için kalıp: sayı ya da sağlık/teknik sonuç iddiası olmasın ("daha kolay oldu", "kaçırdığım günü fark ettim" gibi kişisel ifade yeter). Teknik bir sonuç söyleyeceksen `[fact-check]` gerekir.
- Reels açıklamalarında hashtag/etiket seçimi İlteriş'in; metin bunu zorunlu kılmıyor.

---

## 3. Mevcut videolara 3 sabit yorum (pin)

Instagram'da bir gönderide en fazla 3 yorum sabitlenir. Yorumlardaki bağlantılar tıklanamaz, bu yüzden URL **yazılmıyor**; yönlendirme bio'ya ve DM'e.

Hangi videolara: en çok izlenen jo videolarının 3'ünde (ya da en çok izlenen, jo içeren 1 videoda 3 yorum), İlteriş kendi hesabından yazıp sabitler. Yorumlar birbirini tekrar etmesin diye 3 farklı videoya dağıtmak daha doğal.

1. **Program tanıtımı:** `Dojo dışında bu tür suburi'yi düzenli çalışmak için 30 günlük bir plan hazırladım: günde 10-20 dk, ücretsiz. Link bio'da. Ya da "link" yaz, DM atayım.`
2. **Soru:** `Jo'yu günde kaç dakika çalışıyorsunuz? Ben 30 günlük bir program hazırladım, ücretsiz. Link bio'da.`
3. **Başlangıç:** `Suburi'yi dojoda öğrenmiş ama evde düzenli çalışamayanlar için 30 günlük plan var: hafta hafta tema, her gün kayıt. Link bio'da, "link" yazarsan DM atarım.`

("Bu videodaki çalışmayı" ifadesi yalnız videonun gerçekten programın bir temasıyla ilgili olduğu durumda kullanılmalı; değilse 2 ya da 3 numarayı seç.)

---

## 4. Yorum / DM yanıt şablonu ("link?", "link nerede?")

Önce yoruma kısa yanıt (link tıklanamaz), sonra DM ile link. DM'deki linke ayrı kampanya adı veriyoruz: `reel-30-gun-jo`.

**Yoruma yanıt:**
- TR: `Bio'da. Ayrıca DM attım.`
- EN: `It's in the bio. I also sent you a DM.`

**DM (TR):**
```
Selam, ilgin için sağ ol. 30 günlük jo suburi programı burada, ücretsiz:
https://joatolyesi.com/programs/30-day-jo-suburi?utm_source=instagram&utm_medium=social&utm_campaign=reel-30-gun-jo
Kayıt olup 1. günden başlayabilirsin. Takıldığın yer olursa yaz.
```

**DM (EN):**
```
Hi, thanks for asking. The free 30-day jo suburi program is here:
https://joatolyesi.com/programs/30-day-jo-suburi?utm_source=instagram&utm_medium=social&utm_campaign=reel-30-gun-jo
Sign up and start at day 1. Message me if you get stuck.
```

Kural: Yalnız isteyene gönder. Toplu/otomatik DM gönderme, aynı kişiye tekrar gönderme. Yanıtları İlteriş elle yazar.

---

## 5. Ölçüm

**GA4 (olay ve boyut):**

| Ne | Olay / rapor | Not |
|---|---|---|
| Sayfaya gelen | Edinme → Trafik edinme, `instagram / social`, ikincil boyut "Oturum kampanyası" (`bio`, `story-30-gun-jo-dN`, `reel-30-gun-jo`) | Hangi gün/story getirdi |
| Kayıt | `sign_up` (var; `method`, `discipline`), kaynak: `instagram / social` | Key event işaretlenmemişse İlteriş işaretlesin (METRICS.md) |
| Programa başlama | `program_enroll` (**B-20'de eklenecek, henüz kodda yok**) | Deploy sonrası Gerçek zamanlı'da tetiklendiğini doğrula, parametre adlarına (gün/program) bak |
| Devam | `program_day_complete` (**B-20'de eklenecek**), gün ≥ 7 | 7. günü tamamlamak için en az 7 gün gerekir (günler sırayla açılıyor, `programs.py`) |
| Genel pratik | `practice_logged` | Programın dışında da çalışıyor mu |
| Kontrol | `(direct) / (none)` oturum sayısı | UTM'den sonra düşüyor mu (11-03 §7) |

Gerçek kullanıcı sayısı için GA4'e değil DB'ye bak: `scripts/weekly_metrics.py` (demo ve sahip hariç). GA4'teki bot/veri merkezi trafiği (METRICS.md notu) oturum sayılarını şişirebilir; kayıt ve enroll sayıları daha güvenilir.

**Instagram Insights (GA4 dışı, elle not al; ekranlar sürüme göre değişebilir):**
- Reels: erişim/oynatma, kaydetme, paylaşım.
- Profil: profil ziyareti ve **bio linki dokunuşu** (dış bağlantı dokunuşları).
- Story: **bağlantı çıkartması dokunuşu**, görüntüleme, yanıt (soru çıkartması cevapları), sonraki story'ye geçiş/çıkış.
- İki kaynağı yan yana yaz: "Insights'ta N dokunuş → GA4'te M oturum". Aradaki kayıp (uygulama içi tarayıcı vb.) 11-03 teşhisinin 2. olasılığı.

**Başarı eşiği önerisi (14 gün) — hepsi TAHMİN, veriye dayanmıyor:**

Dayanak yalnız bu: başlangıçta instagram ~5 oturum / 28 gün, kayıtlı gerçek kullanıcı 10, Instagram kaynaklı kayıt ölçülmüyordu. Kampanya için bir dönüşüm oranı verisi yok. Aşağıdaki sayılar "karar çizgisi" olarak seçildi, sonuç tahmini değil.

| Metrik (14 gün, `instagram / social`) | Alt çizgi (devam et) | Güçlü (ölçeklendir) |
|---|---|---|
| Programa/sayfaya gelen oturum | ≥ 30 | ≥ 100 |
| `sign_up` | ≥ 4 | ≥ 12 |
| `program_enroll` | ≥ 3 | ≥ 10 |
| `program_day_complete` gün ≥ 7 (kişi) | ≥ 1 | ≥ 3 |

**Karar kuralı:**
- Alt çizgiyi geçerse: aynı yapıyı 14 gün daha sürdür, B-22 e-posta dizisini öne al.
- Oturum var ama `sign_up` yok: sorun sayfa/kayıt akışında (CTA, kayıt adımı sayısı, UTM düşmesi §0.2).
- `sign_up` var ama `program_enroll`/gün 7 yok: sorun teklifin sonrasında (ilk gün deneyimi, hatırlatma yok). B-22'nin kanıtı olur.
- Insights'ta dokunuş yok: sorun içerik/CTA tarafında; kancaları ve CTA'yı değiştir, teklifi değil.
- Eşikleri 14. günde İlteriş ve PO birlikte yeniden değerlendirsin; 14 günlük örnek küçük, tek bir kişi sonucu oynatabilir.

---

## 6. EN versiyon (kısa)

**Bio (EN):** `Free 30-day jo suburi plan for between-class practice ↓ / Aiki-jo · aiki-ken`
**Bio link:** same as §1 (`campaign=bio`).

**Pin comments (EN):**
1. `A 30-day plan to practice suburi between classes: 10-20 min a day, free. Link in bio, or comment "link" and I'll DM you.`
2. `How many minutes a day do you train with the jo? I made a free 30-day program. Link in bio.`
3. `Starting from zero or coming back? There's a 30-day jo program: one theme per week, log every day. Link in bio.`

**14-day plan, one line each** (story URL pattern is identical for all days: `.../programs/30-day-jo-suburi?utm_source=instagram&utm_medium=social&utm_campaign=story-30-gun-jo-dN`):
- D1 reel: "30 days. Every day, the jo." Caption: "30-day jo suburi program is live. For between-class practice, about 10-20 min a day, free. Link in bio."
- D2 story: screen recording of the program page.
- D3 reel: "Day 1: 5 min warm-up, 3 sets." D4 story: question sticker ("When did you last pick up the jo?").
- D5 reel: "Third set is slower. On purpose." D6 story: your real day count.
- D7 reel: "Day 7: review day, nothing new." D8 story: week 2 teaser.
- D9 reel: "Week 2 starts." D10 story: question sticker ("Where do 30 days usually break?").
- D11 reel: "No dojo? The program is still on." D12 story: week 3 teaser.
- D13 reel (only if you are really doing it): "Day <N>: what changed?" D14 story: week 4 teaser, last call.

Thresholds and events: see §5 (same numbers; estimates, not data).

---

## 7. İlteriş'in somut adımları

1. B-20 deploy olunca §0 kontrollerini yap (çıkış yapmış tarayıcıda, telefondan; ~5 dk).
2. Bio metnini (§1 A) ve bio linkini değiştir; telefondan dokunup GA4 Gerçek zamanlı'da `instagram / social` göründüğünü doğrula (~5 dk).
3. D1 reels'ını çek, aynı gün story ve 3 pin yorumunu at; sonraki günlerde §2 takvimine göre devam et (günde ~10-15 dk).
4. 7. ve 14. günde Insights dokunuşlarını ve GA4 sayılarını METRICS.md'ye yaz.
