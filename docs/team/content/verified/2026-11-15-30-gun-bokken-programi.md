---
type: guide
target: app/seed.py (Program "30-day-bokken-suburi": program satırı + 30 ProgramDay), app/guide_content.py#PROGRAMS["bokken"] (ikincil)
discipline: bokken
status: verified
---

# 30 Günlük Bokken Suburi Programı — onaylı metin (kısmi onay)

Kaynak taslak: `docs/team/content/drafts/2026-11-15-30-gun-bokken-programi.md`.
Gün planı, tekrar sayıları ve süreler Joryu'nun pedagojik tasarımıdır (B-33 tavsiyesi,
teknik iddia değil). Sayaç ve kilit yok. Partnerli kumitachi yok. Japonca terimler
makronsuz (jodan, yokomen, hanmi).

Numaralandırma: Saito/Iwama çizgisinin 7 ken suburi'si (ichi … shichi/nana).
Kaynaklar bazı hareketlerde ayrışıyor; ayrışan yer metinde açıkça söylenir.

> Not: Program yalnız ilgili program satırı yokken seed ediliyorsa canlı veritabanı
> kendiliğinden güncellenmez (jo programındaki not geçerli; backend kararı).

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

## 2. WEEKS

Modulo şeması yerine 30 elemanlı `BOKKEN_DAY_FOCUS` listesi (bölüm 3) önerilir; developer kararı.

```python
BOKKEN_WEEKS = [
    ("Foundation — ichi no suburi", "Temel — ichi no suburi"),                  # gün 1-7
    ("Stepping back — ni & san no suburi", "Geri adım — ni ve san no suburi"),  # gün 8-14
    ("Advancing cuts — yon & go no suburi", "İlerleyen kesişler — yon ve go no suburi"),  # gün 15-21
    ("Cut and thrust — roku & shichi no suburi", "Kesiş ve tsuki — roku ve shichi no suburi"),  # gün 22-28
    # Gün 29-30: "Joining: full series" / "Birleştirme: tüm seri"
]
```

## 3. Gün planı (30 gün)

| Gün | Odak TR | Focus EN |
|---|---|---|
| 1 | Duruş (migi hanmi) + ichi no suburi, yavaş | Stance (migi hanmi) + ichi no suburi, slow |
| 2 | Ichi no suburi: 3 set x 10+ | Ichi no suburi: 3 sets of 10+ |
| 3 | Ichi no suburi: kesiş ve ayak uyumu | Ichi no suburi: cut and foot together |
| 4 | Ichi no suburi: hanmi duruşu, kesişte merkez hattı | Ichi no suburi: hanmi stance, cutting on the centre line |
| 5 | Ichi no suburi: ayna karşısında, kılıç hattı | Ichi no suburi: in front of a mirror, sword line |
| 6 | Ichi no suburi: uzun set, son set en yavaş | Ichi no suburi: long set, last set slowest |
| 7 | Tekrar günü (hafta 1) | Review day (week 1) |
| 8 | Ichi no suburi ısınma, sonra ni no suburi tanışma | Ichi warm-up, then meet ni no suburi |
| 9 | Ni no suburi: geri adım ve kılıcı kaldırma | Ni no suburi: step back and raise |
| 10 | Ichi + ni no suburi, dönüşümlü | Ichi + ni no suburi, alternating |
| 11 | Ichi ısınma, sonra san no suburi tanışma | Ichi warm-up, then meet san no suburi |
| 12 | San no suburi: geri adımla aşağı indirme, sonra kesiş | San no suburi: step back and lower, then cut |
| 13 | Ni + san no suburi, dönüşümlü | Ni + san no suburi, alternating |
| 14 | Tekrar günü (hafta 2: ichi, ni, san) | Review day (week 2: ichi, ni, san) |
| 15 | Ichi-ni-san ısınma, sonra yon no suburi tanışma | 1-3 warm-up, then meet yon no suburi |
| 16 | Yon no suburi: ardışık kesişler, sağ-sol | Yon no suburi: continuous cuts, right-left |
| 17 | Go no suburi tanışma (hocana danış) | Meet go no suburi (ask your teacher) |
| 18 | Go no suburi: sağ-sol yönde çapraz kesiş | Go no suburi: diagonal cuts, both sides |
| 19 | Yon + go no suburi, dönüşümlü | Yon + go no suburi, alternating |
| 20 | Ichi'den yon'a kadar yavaş geçiş | Slow run from ichi to yon |
| 21 | Tekrar günü (hafta 3: yon, go) | Review day (week 3: yon, go) |
| 22 | Yon-go ısınma, sonra roku no suburi tanışma | Yon-go warm-up, then meet roku no suburi |
| 23 | Roku no suburi: kesişten tsuki'ye geçiş | Roku no suburi: from cut to thrust |
| 24 | Shichi no suburi tanışma | Meet shichi (nana) no suburi |
| 25 | Shichi no suburi: kesiş, adım, tsuki | Shichi no suburi: cut, step, thrust |
| 26 | Roku + shichi no suburi, dönüşümlü | Roku + shichi no suburi, alternating |
| 27 | Ichi'den shichi'ye tüm seri, yarı hız | Full series 1-7 at half speed |
| 28 | Tekrar günü (hafta 4: roku, shichi) | Review day (week 4: roku, shichi) |
| 29 | Tüm seri, ayna karşısında; en zayıf suburi'ye ekstra tur | Full series in front of a mirror; extra round on the weakest |
| 30 | Tüm seri, sakin tempoda; ilerlemeni kaydet | Full series, calm tempo; log your progress |

### Gün metni şablonları

```python
# Tekrar günü (day_num in 7, 14, 21, 28)
content_tr = (f"Hafta teması: {theme_tr}. Bugün tekrar günü. 5 dakika ısın (bilek, omuz, kalça). "
  "Sonra bu haftanın suburi'lerini 10 dakika yavaş ve bilinçli tekrar et. "
  "Yarı hız, tam dikkat. 5 dakika serbest hareketle bitir.")
content_en = (f"Week theme: {theme_en}. Review day. Warm up 5 minutes (wrists, shoulders, hips). "
  "Then 10 minutes of slow, deliberate repetition of this week's suburi. "
  "Half speed, full attention. Finish with 5 minutes of free movement.")

# Normal gün (gün 29-30'da theme = "Birleştirme: tüm seri" / "Joining: full series")
content_tr = (f"Hafta teması: {theme_tr}. 5 dakika ısın (bilek, omuz, kalça). "
  f"Ana çalışma: {focus_tr}. Her suburi için en az 10 tekrar önerilir; "
  "ihtiyacın kadar set yap, son set ilkinden yavaş olsun: hızdan önce isabet. "
  "Bu hareketi henüz hocandan öğrenmediysen önce ona danış. Bitirince seansını kaydet.")
content_en = (f"Week theme: {theme_en}. Warm up 5 minutes (wrists, shoulders, hips). "
  f"Main work: {focus_en}. At least 10 repetitions per suburi is suggested; "
  "do as many sets as you need, last set slower than the first: precision over speed. "
  "If you haven't learned this movement from a teacher yet, ask yours first. Log your session when done.")
```

## 4. Suburi hareket açıklamaları (onaylı çekirdek)

Kaynakların hepsi dojo/ikincil düzeyde (Standartlar 3); her madde en az iki bağımsız kaynakla örtüşüyor. Resmi müfredat değildir; hocanın çizgisi önceliklidir.

1. **Ichi no suburi.** Hanmi duruştan tek, düz shomen kesişi (tepeden aşağı dikey kesiş).
2. **Ni no suburi.** Sağ ayakla geri adım atarken kılıç başın üstüne kalkar; ardından öne adımla düz shomen kesişi.
3. **San no suburi.** Geri adımda kılıç kaldırılıp sağ yana, uyluk hizasına (waki gamae) indirilir; öne adımla shomen kesişi. Bazı dojolar (ör. Aikido Australia) bu suburi'yi gedan'a geri adımla öğretir; hocanın çizgisini izle.
4. **Yon no suburi.** İlerlerken sağ-sol duruş değiştirerek art arda shomen kesişi.
5. **Go no suburi.** İlerlerken sağa ve sola dönüşümlü, başın yanına yönelen çapraz kesişler.
6. **Roku no suburi.** Her kesişin ardından tsuki; sağ ve sol tarafta dönüşümlü tekrarlanır.
7. **Shichi (nana) no suburi.** Sağ duruşta kesiş, ardından öne adımla sol duruşta tsuki; tekrarlanarak ilerlenir.

Tekrar sayısı: kaynaklar sayı vermiyor; "en az 10 tekrar" Joryu'nun B-33 tavsiyesidir.

## EN özet

A 30-day bokken program on the seven aiki-ken suburi (Saito/Iwama numbering): week 1 ichi no suburi; week 2 ni and san (step back, then cut); week 3 yon and go (advancing cuts); week 4 roku and shichi (cut and thrust); days 29-30 join the full series. At least 10 reps per suburi is a suggestion; no counter or lock. Movement notes are limited to what at least two independent dojo sources agree on; san no suburi is taught to waki gamae in most sources and to gedan in some. Solo only, no kumitachi.

## Denetim — 2026-11-15
- Sonuç: DÜZELTİLDİ (kısmi onay). Gün planı, süreler, tekrar önerisi pedagojik tasarım, denetim dışı; iç tutarlılık ✅ (normal gün ≈10-15 dk, tekrar günü 20 dk; "10-20 dakika" doğru).
- Numaralandırma (7 suburi, sıra, shichi/nana) ✅ Takemusu Iwama, Shuren, Aikido Australia, Aikido Warrior örtüşüyor.
- [^1] Ichi ✅ düz shomen (Takemusu Iwama, Shuren, Wikipedia). ❌ "yalnız sağ ayak kayar, sol ayak yerinde kalır" çıkarıldı: yalnız Takemusu Iwama söylüyor; Aikido Warrior sağ ayağın hafif geri kaydığını yazıyor, sol ayak için bir şey demiyor. Gün 4 odağı buna dayanıyordu, "hanmi duruşu, kesişte merkez hattı" yapıldı.
- ⚠️ Gün 1 "ken no kamae" yerleşik bir terim olarak hiçbir kaynakta geçmiyor; "migi hanmi" yapıldı (Shuren, Aikido Australia, Aikido Warrior başlangıcı hanmi).
- [^2] Ni ✅ sağ ayak geri (Shuren, Aikido Warrior), kılıç yukarı/jodan (Takemusu Iwama, Aikido Australia, Shuren), öne adımla shomen. "jodan benzeri" parantezi sadeleştirildi.
- [^3] San ✅ waki gamae: Takemusu Iwama, Aikido Warrior (Saito'ya atıflı), Shuren ("sağa indirilir"), Wikipedia. Aikido Australia gedan diyor (Saito'ya atıf yok); çelişki Standartlar gereği metinde açıkça yazıldı. ❌ "kılıç boyunun rakipten gizlenmesi" çıkarıldı: yalnız Aikido Warrior'da var. Gün 12 "kılıcı gizleme" → "geri adımla aşağı indirme, sonra kesiş".
- [^4] Yon ✅ dört kaynakta ilerleyerek sağ-sol shomen. Uç kaldırma (yalnız Aikido Australia) taslakta zaten yoktu.
- [^5] Go ✅ çekirdek: ilerlerken sağ-sol dönüşümlü yan/çapraz kesiş (Takemusu Iwama "sağa ve sola shomen", Shuren "başın yanına sağ-sol", Aikido Warrior yokomen/gyaku yokomen). ❌ "yaklaşık 70 derece" çıkarıldı: Aikido Warrior + Wikipedia (zayıf); iki orta kaynak şartı yok. "Yokomen tipi" adlandırması da çıkarıldı (Takemusu Iwama shomen adı kullanıyor).
- [^6] Roku ✅ kesiş + tsuki, sağ/sol dönüşümlü (Takemusu Iwama migi/hidari, Shuren, Aikido Warrior). Kesiş türü (shomen mi yokomen mi) ve hanmi ayrıntısı kaynaklarda ayrışıyor, metne girmedi.
- [^7] Shichi ✅ sağda kesiş, adımla solda tsuki (Takemusu Iwama, Shuren, Aikido Australia, Aikido Warrior).
- Güvenlik ✅ "hocana danış" her normal günde var; sağlık tavsiyesi yok. Telif ✅ alıntı yok.
- Çıkarılan ayrıntılar (ichi sol ayak, san gizleme, go 70°, roku ayak/yön ayrıntısı) TODO.md §3b'deki "Aiki-ken 2-7. suburi tanımları" maddesi kapsamında kalıyor.
- Kaynaklar (açıldı, 2026-11-15): https://takemusu-iwama-aikido.org/?p=305, https://aikido-shuren-dojo.com/?p=83, https://aikidoaus.com.au/library/aiki-ken-curriculum/, https://theaikidowarrior.com/first-suburi-ichi-no-suburi/, https://theaikidowarrior.com/second-suburi-ni-no-suburi/, https://theaikidowarrior.com/third-suburi-san-no-suburi/, https://theaikidowarrior.com/fifth-suburi-go-no-suburi/, https://theaikidowarrior.com/sixth-suburi-roku-no-suburi/, https://theaikidowarrior.com/seventh-suburi-shichi-no-suburi/, (zayıf) https://en.wikipedia.org/wiki/Aiki-ken
