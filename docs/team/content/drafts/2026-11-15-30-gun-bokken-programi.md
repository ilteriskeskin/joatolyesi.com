---
type: guide
target: app/seed.py (Program "30-day-bokken-suburi": program satırı + 30 ProgramDay), app/guide_content.py#PROGRAMS["bokken"] (ikincil)
discipline: bokken
status: draft
---

# 30 Günlük Bokken Suburi Programı (Aikiken suburi 1-7)

Not: Gün planı, tekrar sayıları ve süreler bizim pedagojik tasarımımızdır (kaynak gerektirmez). Yalnız bölüm 4'teki hareket açıklamaları teknik iddiadır ve kaynaklıdır. Tüm tekrar/sıra önerileri tavsiyedir; sayaç ve kilit yoktur (B-33). Partnerli kumitachi programda yoktur. Japonca terimler makronsuz yazıldı (jodan, yokomen).

Numaralandırma: Saito/Iwama çizgisinin 7 ken suburi'si (ichi, ni, san, yon, go, roku, shichi/nana). Kaynaklar adlandırmada ve bazı hareketlerde ayrışıyor; ayrışan yerler bölüm 4'te açıkça belirtildi.

## 1. Program açıklaması

```python
description_tr=(
    "Bir ay boyunca her gün yapılandırılmış bokken suburi çalışması. "
    "Önce ichi no suburi, sonra sırayla 2-7. Dört haftalık tema, ardından iki "
    "birleştirme günü. Günde yaklaşık 10-20 dakika; tekrar sayıları tavsiyedir."
),
description_en=(
    "One month of daily, structured bokken suburi practice (aiki-ken suburi 1-7). "
    "Start with ichi no suburi, then add the rest in order. Four weekly themes "
    "plus two joining days. About 10-20 minutes a day; rep counts are suggestions."
),
```

## 2. WEEKS (tema + gün odakları)

Jo programındaki `focuses[(day_num - 1) % len]` modulo şeması bokken için uygun değil (yeni suburi, hafta içinde belirli günde başlamalı). Öneri: `focuses` yerine 30 elemanlı `BOKKEN_DAY_FOCUS` listesi (bölüm 3) kullanılsın. Developer kararı; içerik aşağıdadır.

```python
BOKKEN_WEEKS = [
    ("Foundation — ichi no suburi", "Temel — ichi no suburi"),                  # gün 1-7
    ("Stepping back — ni & san no suburi", "Geri adım — ni ve san no suburi"),  # gün 8-14
    ("Advancing cuts — yon & go no suburi", "İlerleyen kesişler — yon ve go no suburi"),  # gün 15-21
    ("Cut and thrust — roku & shichi no suburi", "Kesiş ve tsuki — roku ve shichi no suburi"),  # gün 22-28
    # Gün 29-30: "Whole series" / "Tüm seri" (hafta 5 teması, 2 gün)
]
```

## 3. Gün planı (30 gün)

Her normal gün: 5 dk ısınma (bilek, omuz, kalça), ana çalışma, son 2 dk sakin nefes/duruş. Tavsiye: her suburi için en az 10 tekrar; yeni suburi günlerinde önce ichi no suburi'den birkaç tekrarla ısın.

| Gün | Odak TR | Focus EN |
|---|---|---|
| 1 | Duruş (ken no kamae) + ichi no suburi, yavaş | Stance (ken no kamae) + ichi no suburi, slow |
| 2 | Ichi no suburi: 3 set x 10+ | Ichi no suburi: 3 sets of 10+ |
| 3 | Ichi no suburi: kesiş ve ayak uyumu | Ichi no suburi: cut and foot together |
| 4 | Ichi no suburi: sağ ayak kayması, sol ayak yerinde | Ichi no suburi: right foot slides, left stays |
| 5 | Ichi no suburi: ayna karşısında, kılıç hattı | Ichi no suburi: in front of a mirror, sword line |
| 6 | Ichi no suburi: uzun set, son set en yavaş | Ichi no suburi: long set, last set slowest |
| 7 | Tekrar günü (hafta 1) | Review day (week 1) |
| 8 | Ichi no suburi ısınma, sonra ni no suburi tanışma | Ichi warm-up, then meet ni no suburi |
| 9 | Ni no suburi: geri adım ve kılıcı kaldırma | Ni no suburi: step back and raise |
| 10 | Ichi + ni no suburi, dönüşümlü | Ichi + ni no suburi, alternating |
| 11 | Ichi ısınma, sonra san no suburi tanışma | Ichi warm-up, then meet san no suburi |
| 12 | San no suburi: kılıcı gizleme ve kesiş | San no suburi: hidden blade and cut |
| 13 | Ni + san no suburi, dönüşümlü | Ni + san no suburi, alternating |
| 14 | Tekrar günü (hafta 2: ichi, ni, san) | Review day (week 2: ichi, ni, san) |
| 15 | Ichi-ni-san ısınma, sonra yon no suburi tanışma | 1-3 warm-up, then meet yon no suburi |
| 16 | Yon no suburi: ardışık kesişler, sağ-sol | Yon no suburi: continuous cuts, right-left |
| 17 | Go no suburi tanışma (hocana danış, bkz. not) | Meet go no suburi (ask your teacher, see note) |
| 18 | Go no suburi: sağ-sol yönde çapraz kesiş | Go no suburi: diagonal cuts, both sides |
| 19 | Yon + go no suburi, dönüşümlü | Yon + go no suburi, alternating |
| 20 | Ichi'den yon'a kadar yavaş geçiş | Slow run from ichi to yon |
| 21 | Tekrar günü (hafta 3: yon, go) | Review day (week 3: yon, go) |
| 22 | Yon-go ısınma, sonra roku no suburi tanışma | Yon-go warm-up, then meet roku no suburi |
| 23 | Roku no suburi: kesiş ve tsuki arası geçiş | Roku no suburi: from cut to thrust |
| 24 | Shichi no suburi tanışma | Meet shichi (nana) no suburi |
| 25 | Shichi no suburi: kesiş, adım, tsuki | Shichi no suburi: cut, step, thrust |
| 26 | Roku + shichi no suburi, dönüşümlü | Roku + shichi no suburi, alternating |
| 27 | Ichi'den shichi'ye tüm seri, yarı hız | Full series 1-7 at half speed |
| 28 | Tekrar günü (hafta 4: roku, shichi) | Review day (week 4: roku, shichi) |
| 29 | Tüm seri, ayna karşısında; en zayıf suburi'ye ekstra tur | Full series in front of a mirror; extra round on the weakest |
| 30 | Tüm seri, sakin tempoda; ilerlemeni kaydet | Full series, calm tempo; log your progress |

### Gün metni şablonları (jo programındaki biçime paralel)

```python
# Tekrar günü (day_num in 7, 14, 21, 28)
content_tr = (f"Hafta teması: {theme_tr}. Bugün tekrar günü. 5 dakika ısın (bilek, omuz, kalça). "
  "Sonra bu haftanın suburi'lerini 10 dakika yavaş ve bilinçli tekrar et. "
  "Yarı hız, tam dikkat. 5 dakika serbest hareketle bitir.")
content_en = (f"Week theme: {theme_en}. Review day. Warm up 5 minutes (wrists, shoulders, hips). "
  "Then 10 minutes of slow, deliberate repetition of this week's suburi. "
  "Half speed, full attention. Finish with 5 minutes of free movement.")

# Normal gün
content_tr = (f"Hafta teması: {theme_tr}. 5 dakika ısın (bilek, omuz, kalça). "
  f"Ana çalışma: {focus_tr}. Her suburi için en az 10 tekrar önerilir; "
  "ihtiyacın kadar set yap, son set ilkinden yavaş olsun: hızdan önce isabet. "
  "Bu hareketi henüz hocandan öğrenmediysen önce ona danış. Bitirince seansını kaydet.")
content_en = (f"Week theme: {theme_en}. Warm up 5 minutes (wrists, shoulders, hips). "
  f"Main work: {focus_en}. At least 10 repetitions per suburi is suggested; "
  "do as many sets as you need, last set slower than the first: precision over speed. "
  "If you haven't learned this movement from a teacher yet, ask yours first. Log your session when done.")
```

Gün 29-30 için not: normal şablon kullanılabilir; "hafta teması" yerine "Birleştirme: tüm seri" / "Joining: full series".

## 4. Suburi hareket açıklamaları (kaynaklı)

Yalnız en az iki bağımsız kaynağın örtüştüğü çekirdek yazıldı. Kaynakların hepsi orta/zayıf düzeydedir (aşağıda not). Hiçbiri "resmi müfredat" değildir.

**1 — Ichi no suburi.** Tek, düz bir shomen kesişi (tepeden aşağı dikey kesiş); yalnız sağ ayak kayar, sol ayak yerinde kalır.[^1][^2]

**2 — Ni no suburi.** Sağ ayakla geri adım atarken kılıç başın üstüne kalkar (jodan benzeri); ardından öne adımla düz bir shomen kesişi yapılır.[^1][^2][^3]

**3 — San no suburi.** Geri adım, kılıç başın üstüne kalkar, sonra kılıç aşağıya, sağ uyluk/yan tarafa (waki gamae) indirilir; öne adımla shomen kesişi. Kılıç boyunun rakipten gizlenmesi vurgulanır.[^1][^3][^4] (Kaynak çelişkisi: bir kaynak bunu gedan olarak anlatıyor.[^5] Bkz. bölüm 5.)

**4 — Yon no suburi.** İlerlerken sağ-sol ayak değiştirerek art arda shomen kesişi.[^1][^2][^6]

**5 — Go no suburi.** İlerlerken sağ ve sola dönüşümlü, yaklaşık 70 derece açılı yokomen tipi (kafanın yanına) kesişler.[^2][^7][^6] (Kaynaklar adlandırma ve ayrıntıda ayrışıyor; bölüm 5.)

**6 — Roku no suburi.** Kesişin ardından tsuki; kesiş-tsuki dizisi iki yönde dönüşümlü.[^2][^7][^8]

**7 — Shichi (nana) no suburi.** Sağ duruşta kesiş, ardından öne adımla sol duruşta tsuki; tekrarlanarak ilerlenir.[^2][^7][^8]

Tekrar sayısı: kaynaklar bir sayı vermiyor. "En az 10 tekrar" Joryu'nun B-33 tavsiyesidir, teknik iddia değil.

## 5. Zayıf / çelişkili maddeler (fact-checker dikkatine)

1. **San no suburi: waki gamae mi, gedan mı?** Takemusu Iwama (Wikipedia ile uyumlu) ve Aikido Warrior waki gamae diyor; Aikido Australia gedan kamae diyor. Taslak waki gamae yazıyor. Mevcut `app/seed.py` "Aiki-ken suburi 3 ... Alt savuşturma (gedan)" yazıyor: kaynaklarla çelişen ya da en azından tek kaynaklı. Kodda ayrı düzeltme gerekir (bu taslağın kapsamı dışı).
2. **Go no suburi.** Takemusu Iwama "renzoku nagare shomen" (sağ-sol yan kesişler) der; Shuren ve Aikido Warrior yaklaşık 70 derece yokomen; Aikido Australia "kılıcın sapını kaldırarak" der. Çekirdek ("dönüşümlü yan/çapraz kesiş") iki kaynakla destekli, ayrıntı [DOĞRULANAMADI]. Mevcut seed'deki "yan savuşturma" ifadesi bu kaynaklarda yok. Gün 17 bu yüzden "hocana danış" notlu.
3. **Roku no suburi.** Wikipedia "düz kesiş sonra öne kayarak tsuki" der; Aikido Australia "kesiş ve tsuki aynı hanmi'de" der; diğerleri iki yönde dönüşümlü. Çekirdek ("kesiş + tsuki") ortak, yön/ayak ayrıntısı [DOĞRULANAMADI]. Mevcut seed'deki "tsuki'de arka topuk kalkmaz" ifadesi kaynaklarda yok.
4. **Yon no suburi.** Aikido Australia kılıç ucunun kaldırıldığını belirtir; diğerleri belirtmez. Taslağa alınmadı.
5. **Suburi 4 ve 5 numaralandırma** Takemusu Iwama listesinde 4-7 "renzoku" olarak farklı adlandırılıyor; yine de 7'li sıra ve 1-3 içerik olarak örtüşüyor.
6. **Resmi kaynak yok.** Aikikai/Iwama resmi müfredat belgesi bulunamadı; tümü dojo siteleri (Standartlar madde 3). Kurala göre en az iki bağımsız orta kaynak yeterli; 4-7 için yalnız çekirdek yazıldı.
7. Hareketin kendisini öğrenme: metin öğretmen yerine geçmez; "hocana danış" uyarısı korunmuştur. Sağlık tavsiyesi yok.
8. Wikipedia yalnız destekleyici olarak kullanıldı; tek başına hiçbir iddiayı taşımıyor.

## Kaynaklar (erişim: 2026-11-15)

[^1]: Takemusu Iwama Aikido, "The 7 Ken Suburi", https://takemusu-iwama-aikido.org/?p=305 — 1: düz shomen, yalnız sağ ayak kayar; 2: geri adım jodan, öne kesiş; 3: waki gamae'ye geri adım, öne kesiş; 4: renzoku shomen, sağ-sol. Saito'nun yedi suburi'yi kumitachi'den seçtiğini de belirtir (https://takemusu-iwama-aikido.org/the-7-ken-suburi/).
[^2]: Aikido Shuren Dojo, "Aiki Ken Suburi", https://aikido-shuren-dojo.com/?p=83 — 1: düz kafa kesişi; 2: sağ ayak geri, kılıç yukarıda, öne kesiş; 4: sağ-sol ilerleme; 5: sağ-sol yan kesiş; 6: 5'e ek olarak her kesişten sonra tsuki; 7: sağ duruşta kesiş, sol duruşta tsuki.
[^3]: Aikido Warrior, "Second Suburi – Ni No Suburi" (Saito Sensei'ye atfedilir), https://theaikidowarrior.com/second-suburi-ni-no-suburi/ — sağ ayak geri (hitoemi), öne adımla shomen kesişi, kesişte merkez yükselmez. Wikipedia (https://en.wikipedia.org/wiki/Aiki-ken, destekleyici) 2'yi jodan'a geri adım diye verir.
[^4]: Aikido Warrior, "Third Suburi – San No Suburi", https://theaikidowarrior.com/third-suburi-san-no-suburi/ — kılıcı yukarı uzat, waki'ye indir, kılıcı yan uyluğa yasla ve rakipten gizle, öne adımla shomen. Ayrıca [^1] ve Wikipedia (3 = waki gamae).
[^5]: Aikido Australia, "Aiki-ken Curriculum", https://aikidoaus.com.au/library/aiki-ken-curriculum/ — 1: chudan'dan kesiş; 2: jodan'a geri adım; 3: gedan'a geri adım (diğer kaynaklarla çelişir); 6-7: kesiş + tsuki. Sayfa Saito/Iwama olduğunu açıkça belirtmiyor.
[^6]: Wikipedia, "Aiki-ken", https://en.wikipedia.org/wiki/Aiki-ken (destekleyici) — 4: ilerlerken art arda düz kesiş; 5: yaklaşık 70 derece kesiş; ayrıca [^1] ve [^2] (4).
[^7]: Aikido Warrior, "Sixth/Seventh Suburi", https://theaikidowarrior.com/sixth-suburi-roku-no-suburi/ ve https://theaikidowarrior.com/seventh-suburi-shichi-no-suburi/ — yaklaşık 70 derece yokomen kesişi; 6: kesiş sonrası tsuki, ters yönde tekrar; 7: sağ ayakla kesiş, sol ayakla öne tsuki. Go (5) için: kaynak sayfasında alternatif yokomen kesişleri (https://theaikidowarrior.com/fifth-suburi-go-no-suburi/).
[^8]: Aikido Australia [^5] (6: aynı hanmi'de kesiş+tsuki; 7: sağ hanmi'de kesiş, adımla sol hanmi'de tsuki) ve Aikido Shuren Dojo [^2] (7); Takemusu Iwama [^1] (6-7: kesiş sonrası tsuki).

## EN özet

A 30-day bokken program built on the seven aiki-ken suburi (Saito/Iwama numbering): week 1 ichi no suburi only; week 2 ni and san (step back, then cut); week 3 yon and go (advancing cuts); week 4 roku and shichi (cut and thrust); days 29-30 join the full series. At least 10 reps per suburi is a suggestion, and there is no counter or lock. Movement descriptions are limited to what at least two independent dojo sources agree on; san, go and roku have conflicting source detail (see section 5). Solo only, no kumitachi.
