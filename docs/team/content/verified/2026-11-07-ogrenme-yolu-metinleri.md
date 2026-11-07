---
type: tip
target: app/i18n/strings.py (TR ~satır 497-503 ve 760-790; EN ~satır 12-18 ve 280-305)
discipline: aikijo
status: verified
---

# Öğrenme yolu metinleri (B-33 + B-35)

Kapsam: landing hero alt metni, program detay sayfası, 1. gün sayfası ve program bitiş mesajı. Yalnız metin; sayaç, kilit, yeni alan, migration yok.

## Kaynak ve çerçeve notu

- Tüm tavsiyeler (en az 10 tekrar; önce temel vuruşlar, katalara programı bitirince geç) **Joryu/program tavsiyesidir**. Kaynağı: İlteriş kararı, 2026-11-06 (`docs/team/BACKLOG.md`, "Öğrenme yolu" bölümü, revizyon dahil). Olgusal ya da tarihsel bir iddia değildir; bu yüzden dipnot kaynağı yoktur. Metinlerde "uzmanlar", "geleneksel olarak", "bilimsel olarak" gibi dış otorite atfı kullanılmadı.
- Yalnız 30 günlük programa sıfırdan başlayanlar için tavsiye. Tecrübeli kişi katayı zaten çalışabilir; metin bunu açıkça söyler (kilit ve zorunluluk yok).
- "Hocaya gerek yok" vaadi yok. Çerçeve: "hocan yoksa buradan, temelden başla; topluluk yanında". Hocası olana saygı: "hocan varsa onun sözü önce gelir."
- Yeni teknik/tarihsel iddia eklenmedi. Bu metinlerde `[^n]` dipnotu yok.
- Fact-checker için not: güvenlik notundaki "ağrıda dur" ifadesi CONTENT_STANDARDS "Güvenlik" kuralına göre (sağlık tavsiyesi verilmez; ısınma ve hocaya danış serbest) sınırda. İlteriş kararı (BACKLOG) güvenlik notunun (ısın, yavaş başla, ağrıda dur) korunmasını istiyor; ifade "bırak" yerine genel ve tıbbi tavsiye içermeyen "dur" olarak tutuldu, tedavi/teşhis yok. Karar fact-checker/PO'da.
- Japonca terim yazımı: mevcut dosyadaki gibi "Aiki-jo", "kata", "jo" (makronsuz).

## 1. `hero_sub` (MEVCUT, DEĞİŞİR)

Yer tutucu `{days}` korunur. Eklenen: tek kısa cümle, programa davet.

**TR**
```
Dojo günleri arasında tek başına çalışan aikido, iaido, jodo ve kenjutsu pratisyenleri için: jo, bokken ve kata seanslarını kaydet, serini koru, kata ve teknik kütüphanesinde ilerle — {days} gün aralıksız çalışmış bir pratisyenden. Hocan yoksa 30 günlük programla temelden başla.
```

**EN**
```
For aikido, iaido, jodo and kenjutsu practitioners who train alone between dojo days: log your jo, bokken and kata practice, keep your streak, and browse the kata & technique library — built by a practitioner who trained {days} days straight. No teacher? Start from the basics with the 30-day program.
```

Uzunluk: TR +~55 karakter, EN +~65 karakter (eskiye göre yaklaşık %22-25; tek cümle).

## 2. `program_dojo_note` (MEVCUT, DEĞİŞİR)

Program detay sayfasında kayıt butonunun üstünde ve (giriş yapmamış ziyaretçide) kayıt CTA'sının altında gösterilen not. Eski çerçeve ("hocandan öğrenmiş olmalısın") kaldırılır; güvenlik notu korunur.

**TR**
```
Hocan yoksa buradan, temelden başla; topluluk yanında. Hocan varsa onun sözü önce gelir. Videolar hareketi gösterir, bir öğretmenin yerini tutmaz. Isın, yavaş başla, ağrı hissedersen dur.
```

**EN**
```
No teacher? Start here, from the basics; the community is with you. If you have a teacher, their word comes first. The videos show the movement, but they are not a substitute for a teacher. Warm up, start slow, and stop if something hurts.
```

## 3. `program_for_whom` (YENİ)

Program detay sayfasında, açıklamanın altında kısa "kimin için" satırı (başlık yok, tek paragraf).

**TR**
```
Bu program jo'ya sıfırdan başlayanlar için. Zaten çalışıyorsan, aşağıdaki tavsiyeler seni bağlamaz; katalara istediğin zaman bakabilirsin.
```

**EN**
```
This program is for people starting jo from scratch. If you already train, the advice below doesn't bind you; you can browse the katas any time.
```

## 4. `program_advice_reps` (YENİ)

Tavsiye 1. Program detayında ve 1. günde ortak kullanılır (iki yerde aynı anahtar).

**TR**
```
Her hareketi en az 10 tekrar çalış.
```

**EN**
```
Practice each movement at least 10 times.
```

## 5. `program_advice_basics_first` (YENİ)

Tavsiye 2. Program detayında ve 1. günde ortak.

**TR**
```
Önce temel vuruşlar: katalara programı bitirdikten sonra geç.
```

**EN**
```
Basic strikes first: move on to the katas after you finish the program.
```

## 6. `program_advice_heading` (YENİ, kısa başlık)

İki tavsiyenin üstündeki küçük başlık / etiket (program detayında).

**TR**
```
Joryu tavsiyesi
```

**EN**
```
Joryu's advice
```

## 7. `program_advice_note` (YENİ)

İki tavsiyenin altında, tavsiye (zorunluluk değil) olduğunu belirten tek satır. Program detayında tavsiyelerle birlikte.

**TR**
```
Bunlar tavsiyedir; sayaç ya da kilit yok.
```

**EN**
```
These are recommendations; there is no counter or lock.
```

## 8. `program_day1_advice` (YENİ)

1. gün sayfasında (yalnız `day.day_number == 1`), gün içeriğinin altında / tamamla butonunun üstünde kısa hali. Detay sayfasındaki iki ayrı satırın tek cümlelik birleşimi (3. ve 4. anahtarlar bu sayfada gösterilmez; tek anahtar yeter).

**TR**
```
İpucu: her hareketi en az 10 tekrar çalış; katalara programı bitirince geç.
```

**EN**
```
Tip: practice each movement at least 10 times; save the katas until you finish the program.
```

## 9. `program_finished` (MEVCUT, DEĞİŞİR)

Bitiş mesajı. Eski: "Programı tamamladın. Tebrikler." Yeni: aynı sıcaklık + sonraki adım cümlesi; link ayrı anahtardadır (10).

**TR**
```
Programı tamamladın. Tebrikler. Sırada katalar.
```

**EN**
```
You finished the program. Well done. Next up: the katas.
```

## 10. `program_next_kata_link` (YENİ)

Bitiş mesajının hemen altındaki link metni. Hedef: `/kata?d=aikijo` (aiki-jo kata listesi).

Doğrulama: `app/routers/kata.py` `kata_list` branş seçimini `d` query parametresinden okur (`d == "all"` tümü; `d in available` o branş). Branş değeri `app/constants.py` `DISCIPLINES` içindeki `"aikijo"`. `kata_list.html` zaten `/kata?d={{ d }}` ve `&kind=kata` kullanıyor. Yani doğru yol `/kata?d=aikijo` (`kind` varsayılan `kata`; `?discipline=` parametresi **yok**, kullanılmamalı). Not: `d=aikijo` yalnız katalogda o branşta içerik varsa seçilir (`available`); aksi halde kullanıcının kendi branşına düşer, bu davranış developer/qa için bilgi.

**TR**
```
Aiki-jo katalarına git →
```

**EN**
```
Go to the Aiki-jo katas →
```

## Uygulama notu

| Anahtar | Şablon | Nerede / koşul |
|---|---|---|
| `hero_sub` | landing (mevcut kullanım yeri değişmez) | Hero alt metni; `{days}` formatı aynen kalır. |
| `program_for_whom` | `app/templates/program_detail.html` | Başlık ve açıklamanın (`<p class="muted">`) hemen altı; hem giriş yapmamış hem giriş yapmış + kayıtsız görünümde. |
| `program_advice_heading`, `program_advice_reps`, `program_advice_basics_first`, `program_advice_note` | `program_detail.html` | `program_for_whom` altında küçük bir kutu/liste: başlık + iki tavsiye + not satırı. Kayıtlı (enrollment) ve bitirmiş kullanıcıda gösterme gerekmez; yalnız giriş yapmamış ziyaretçide ve henüz kayıt olmamış girişli kullanıcıda (`program_dojo_note` ile aynı iki koşul). |
| `program_dojo_note` | `program_detail.html` | Mevcut iki yer aynı kalır (kayıt CTA'sı altı, kayıt formunun üstü). Metin yeni çerçeve. |
| `program_day1_advice` | `app/templates/program_day.html` | Yalnız `day.day_number == 1` ve kilitli/`opens_tomorrow` değilken; `day.content` paragrafının altı, tamamla formunun üstü. Hafif `muted` stil yeterli. |
| `program_finished` | `program_detail.html` | Mevcut `{% if finished %}` bloğu (`form-message--success`) aynı kalır. |
| `program_next_kata_link` | `program_detail.html` | `finished` bloğunun hemen altında `<p class="program-cta"><a class="button" href="/kata?d=aikijo">...</a></p>`. |

Kapsam dışı / dikkat:
- Tavsiyeler hiçbir yerde zorunlu görünmemeli (ek düğme devre dışı bırakma, onay kutusu, sayaç yok).
- EN şablonlarda anahtarlar `t.<anahtar>` olarak aynı; TR ve EN sözlüklerine aynı anahtar seti eklenmeli (dil paritesi testi varsa geçmeli).
- B-21 kampanya taslağı bu turda yok.
- Fact-checker bu taslağı doğrulama için "olgusal iddia yok; tavsiye kaynağı BACKLOG kararı; güvenlik notu ifadesi" kapsamında inceler.

## Denetim — 2026-11-07
- Sonuç: DÜZELTİLDİ
- Olgusal iddia: yeni teknik/tarihsel iddia yok; dipnot yok, dış otorite atfı yok. `hero_sub`taki "{days} gün aralıksız" ifadesi mevcut metinden aynen korunmuş (app/i18n/strings.py TR 498-503, EN 13-18); yer tutucu `{days}` TR ve EN'de tek ve değişmemiş. ✅
- Tavsiye çerçevesi: "en az 10 tekrar" ve "önce temel vuruşlar" detay sayfasında "Joryu tavsiyesi" başlığı + "Bunlar tavsiyedir; sayaç ya da kilit yok." notuyla, 1. günde "İpucu:" önekiyle sunuluyor; `program_for_whom` tecrübeli kişiyi açıkça muaf tutuyor. Kural/zorunluluk/kilit dili yok; BACKLOG revizyonuyla (sayaç ve kilit yok, yalnız sıfırdan başlayana tavsiye) uyumlu. ✅
- "Hocaya gerek yok" vaadi yok. Çerçeve "hocan yoksa buradan, temelden başla; topluluk yanında" + "hocan varsa onun sözü önce gelir" + "öğretmenin yerini tutmaz"; dürüst. ✅
- Güvenlik notu: "Isın, yavaş başla, ağrı hissedersen dur." genel uyarı düzeyinde; teşhis, tedavi, egzersiz reçetesi yok. CONTENT_STANDARDS "Güvenlik" kuralıyla (ısınma ve genel dikkat uyarısı serbest) uyumlu kabul edildi; değiştirilmedi. ✅
- ⚠️ `program_dojo_note` "Her günün videosu" → "Videolar": program_day.html videoyu yalnız `day.video_url` varsa gösteriyor; her günde video olduğu ürün gerçeği olarak garanti değil. TR ve EN birlikte yumuşatıldı.
- ⚠️ `hero_sub` EN "No teacher nearby?" → "No teacher?": TR "Hocan yoksa" ile anlam eşleşmesi için.
- Link: `/kata?d=aikijo` app/routers/kata.py (24-76) ile doğrulandı: `d` parametresi `available` içindeyse seçilir, `kind` varsayılan `kata`; `aikijo` app/constants.py'de tanımlı. ✅ (Katalogda aikijo içeriği yoksa kullanıcının branşına düşme davranışı qa için not.)
- TR/EN anlam eşleşmesi diğer tüm anahtarlarda tutarlı. ✅

