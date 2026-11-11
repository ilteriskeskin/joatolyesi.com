---
type: tip
target: app/tips_content.py#TIPS
status: verified (DÜZELTİLDİ — öneriler koda henüz uygulanmadı)
backlog: B-31 ("Günün ipucu" dashboard kartı) hazırlığı
---

# Günün ipucu — TIPS listesi denetimi (2026-11-11)

Denetlenen: `app/tips_content.py`, `TIPS` listesinin tamamı (189 satır, **21 madde**).
Kod değiştirilmedi. Aşağıdaki öneriler koda girmeden önce uygulanmalıdır.

## Özet

| Karar | Sayı | Maddeler |
|---|---|---|
| ONAY | 13 | 2, 4, 5, 6, 7, 8, 9, 11, 12, 13, 17, 19, 21 |
| DÜZELT | 8 | 1, 3, 10, 14, 15, 16, 18, 20 |
| KALDIR | 0 | — |

Önemli bulgular:
1. **#3 yanlış çeviri:** Niju Kun'daki madde "kendini kontrol et" demiyor, "önce kendini bil, sonra başkalarını" diyor (先づ自己を知れ而して他を知れ).
2. **#10 anlam kayması:** Dokkōdō'nun ilk maddesi "her şeyi olduğu gibi kabul et" demiyor. İki adı belli çeviri (Ikeda 1965, Tokitsu 2004) bunu "kuşaktan kuşağa gelen dünya yoluna aykırı davranma" olarak veriyor. Kullanılan ifade Wikipedia'daki serbest çeviriden geliyor.
3. **#15, #16, #18:** Kano ve Ueshiba maddelerine kaynakta olmayan yorumlar eklenmiş. Bunlar "güçle değil zamanlamayla kazan", "partnerin en iyi öğretmenin" ve "bir kerelik ilham değil, sadakat" ifadeleri. #16'da TR "en iyi öğretmenin", EN "one of your best teachers" diyor, yani iki dil de birbirini tutmuyor.

Dosya başındaki doğruluk kuralı açısından **uydurma ya da kaynaksız madde bulunmadı**. Sorun, kaynağı olan maddelere eklenen yorumlarda ve tek bir yanlış çeviride.

Docstring notu (koda dokunulmadı): "Niju Kun 1938" tarihi, Genwa Nakasone'nin *Karate-dō Taikan* (1938) yayımıdır. Bu doğrudur ama yazılış tarihi tartışmalıdır. Dokkōdō bazı nüshalarda 19 madde olarak geçer ("21 maddelik" ifadesi yaygın versiyon için doğrudur).

## Madde madde

Numara = listedeki sıra (1 tabanlı). Kaynak kısaltmaları en altta.

### Gichin Funakoshi — Niju Kun

**1. "Karate nezaketle (rei) başlar, nezaketle biter — teknikten önce saygı gelir."** → **DÜZELT**
- Madde doğru (空手道は礼に始まり礼に終る事を忘るな). Ancak "teknikten önce saygı gelir" eki bu maddede yok. Ayrı bir madde olan 技術より心術 (#4) ile karışıyor.
- Önerilen TR: "Karate nezaketle (rei) başlar, nezaketle biter."
- EN: değişmez.
- Kaynak: [NK-Y], [NK-T]

**2. "Karatede ilk saldırı yoktur."** → **ONAY** (空手に先手なし). Kaynak: [NK-Y], [NK-T]

**3. "Başkalarını kontrol etmeye kalkışmadan önce kendini kontrol et."** → **DÜZELT**
- Orijinal: 先づ自己を知れ而して他を知れ (mazu onore o shire, shikashite ta o shire). Fiil *shire* "bil" demektir, "kontrol et" değil. "Control" bazı çevirilerde dolaşan bir hatadır.
- Önerilen TR: "Önce kendini bil, sonra başkalarını."
- Önerilen EN: "First know yourself, then know others."
- Kaynak: [NK-Y] (Japonca metin + çeviri), [NK-T], (destekleyici) takase.com hat sanatı sayfası

**4. "Önce ruh, sonra teknik."** → **ONAY** (技術より心術, gijutsu yori shinjutsu). Bu yaygın çeviri anlama sadık. Kaynak: [NK-Y], [NK-T]

**5. "Kazalar dikkatsizlikten doğar."** → **ONAY** (禍は懈怠に生ず). Kaynak: [NK-Y]

**6. "Karate çalışmasının yalnızca dojoda olduğunu sanma."** → **ONAY** (道場のみの空手と思ふな). Kaynak: [NK-Y]

**7. "Karateyi öğrenmek bir ömür alır — bunun bir sınırı yoktur."** → **ONAY**
- 空手の修業は一生である = "Karate eğitimi ömür boyudur."
- "Sınırı yoktur" kısmı orijinalde yok. Yine de yaygın İngilizce çeviride ("there is no limit") geçiyor ve anlamı bozmuyor.
- İsteğe bağlı sadeleştirme: "Karate çalışması ömür boyu sürer."
- Kaynak: [NK-Y]

**8. "Karate kaynayan su gibidir — sürekli ısıtmazsan soğur."** → **ONAY**
- Orijinal: 空手は湯の如し絶えず熱度を与えざれば元の水に還る. Isıtılmazsa eski (soğuk) suya döner.
- Kaynak: [NK-Y]

**9. "Kazanman gerektiğini değil, kaybetmemen gerektiğini düşün."** → **ONAY** (勝つ考は持つな負けぬ考は必要). Kaynak: [NK-Y]

### Miyamoto Musashi — Dokkōdō / Go Rin no Sho

**10. "Her şeyi olduğu gibi kabul et."** → **DÜZELT**
- Bu ifade Wikipedia'daki adı verilmemiş serbest çeviriden geliyor. Adı belli iki yayımlanmış çeviri 1. maddeyi farklı veriyor: Ikeda (1965) "geleneksel ahlaka aykırı davranmam", Tokitsu (2004) "kuşaktan kuşağa süren dünya yoluna karşı gelme".
- "Her şeyi kabul et" pasif bir kabullenme anlamı taşıyor ve maddenin anlamını kaydırıyor.
- Önerilen TR: "Kuşaktan kuşağa süregelen dünya yoluna aykırı davranma."
- Önerilen EN: "Do not go against the ways of the world handed down through generations."
- Not: Japonca asıl metin (世々の道をそむく事なし) birincil kaynaktan sayfa numarasıyla doğrulanamadı. Aslı Kumamoto Prefectural Museum of Art'ta bulunuyor. Koda girmeden önce Kōdansha Gakujutsu Bunko ya da Chikuma Gakugei Bunko *Gorin no Sho* (Dokkōdō ekli) edisyonundan teyit edilmesi önerilir. Teyit edilemezse madde kaldırılmalı.
- Kaynak: [DK-I], [DK-T], [DK-M]

**11. "Kendini hafife al, dünyayı derinden düşün."** → **ONAY**
- 4. madde (身を浅く思ひ世を深く思ふ). Ikeda ve Tokitsu çevirileri aynı anlamı veriyor.
- Kaynak: [DK-I], [DK-T]

**12. "Yaptığın şeye pişman olma."** → **ONAY**
- 6. madde (我事において後悔をせず). İki çeviri de aynı.
- Kaynak: [DK-I], [DK-T]

**13. "Asla kıskanma."** → **ONAY**
- 7. madde. Tokitsu "iyide de kötüde de", Ikeda ise "başkasının talihini de kendi talihsizliğim yüzünden de" diye genişletiyor. Kısa hali anlama sadık.
- Kaynak: [DK-I], [DK-T]

**14. "Bin gün çalışmak dövmek (temel atmak), on bin gün çalışmak cilalamaktır (ustalaşmaktır)."** → **DÜZELT** (kaynak etiketi ve TR akıcılığı)
- İfade gerçekten metinde var: *Go Rin no Sho*, Su Kitabı (Mizu no Maki), sonsöz. Orijinal: 千日の稽古を鍛とし、万日の稽古を錬とす. "Tanren" (鍛錬) kelimesinin kaynağıdır.
- Mevcut "yaygın çeviriyle" etiketi belirsiz. Ayrıca Victor Harris çevirisinde bu cümle yok (serbest çeviri), bu yüzden "yaygın çeviri" ibaresi yanıltıcı.
- Önerilen source: "Go Rin no Sho (Beş Halka Kitabı), Su Kitabı"
- Önerilen TR: "Bin günlük çalışma temeli döver, on bin günlük çalışma onu arıtır."
- EN: değişmez.
- Kaynak: [GR-K] (orijinal metin), [GR-A] (aikidō dojo açıklaması, destekleyici). Harris çevirisi kontrol edildi, cümle o çeviride yok.

### Jigoro Kano

**15. "Seiryoku zenyo: enerjini en verimli şekilde kullan — güçle değil, doğru zamanlamayla kazan."** → **DÜZELT**
- İlke doğru. Kano bunu "zihin ve bedenin en verimli kullanımı" olarak tanımlıyor ve günlük hayata kadar genelliyor.
- "Güçle değil zamanlamayla kazan" eki Kano'nun tanımında yok. İlkeyi müsabaka tekniğine indirgiyor.
- Önerilen TR: "Seiryoku zenyo: zihnini ve bedenini en verimli şekilde kullan — yalnız tatamide değil, günlük hayatta da."
- Önerilen EN: "Seiryoku zenyo: maximum efficient use of mind and body — on the mat and in daily life."
- Kaynak: [KA-J] (Kōdōkan bülteni), [KA-IJF]

**16. "Jita kyoei: karşılıklı fayda ve ortak gelişim — antrenman partnerin senin en iyi öğretmenin."** → **DÜZELT**
- "Karşılıklı fayda" kısmı doğru.
- "Partnerin en iyi öğretmenin" Kano'ya ait değil ve Kano'nun ağzından sunuluyor.
- TR ("en iyi öğretmenin") ile EN ("one of your best teachers") da birbirini tutmuyor.
- Önerilen TR: "Jita kyoei: karşılıklı yardım ve fayda — kendinle birlikte başkalarının da gelişmesini gözet."
- Önerilen EN: "Jita kyoei: mutual welfare and benefit — progress together with others."
- Kaynak: [KA-IJF], [KA-J]

### Morihei Ueshiba (özet; The Art of Peace)

**17. "Aikido rakibi yenmeyi değil, çatışmayı uyum içinde çözmeyi öğretir."** → **ONAY** (özet olarak)
- Art of Peace #51 ("there are no contests", asıl yenilgi içteki çekişme zihnidir) ve #91 ("the Way of a Warrior is to establish harmony") ile destekleniyor.
- İsteğe bağlı: source alanını "The Art of Peace (John Stevens derlemesi ve çevirisi), öğretinin özeti" yapın. Derleme Ueshiba'nın kendisine değil, Stevens'a aittir.
- Kaynak: [AP]

**18. "Gerçek çalışma günlük tekrardır — bir kerelik ilham değil, her gün dönüp gelen sadakattir."** → **DÜZELT**
- Günlük çalışma teması destekleniyor: #38 günlük çalışma, #41 "Day after day / train your heart out", #93 her gün çalışmaya devam et.
- "Bir kerelik ilham değil … sadakat" karşıtlığı derlemede yok, eklenmiş bir yorum.
- Önerilen TR: "Gün be gün çalış ve tekniğini incelt; kendini hiçbir zaman tamamlanmış bir usta sayma, başkalarıyla birlikte çalışmayı sürdür."
- Önerilen EN: "Train day after day and refine your technique; never think of yourself as a finished master — keep training together with others."
- Kaynak: [AP] #38, #41, #93

### Genel antrenman bilgeliği

**19. "Kısa ve düzenli tekrar, uzun ve düzensiz seanslardan daha kalıcıdır."** → **ONAY**
- Dağıtık pratik etkisiyle uyumlu. Meta-analiz (63 çalışma) aralıklı pratiğin toplu pratikten ortalama olarak daha iyi olduğunu buluyor. Etki basit motor görevlerde daha büyük.
- Kaynak: [SC-D]

**20. "Yorgunken çalışılan teknik, dinlenmişken çalışılandan daha kalıcı hata bırakır — dikkatli ol."** → **DÜZELT**
- Araştırma (Branscheidt ve ark. 2019) kas yorgunluğunun beceri *öğrenmesini* bozduğunu ve etkinin yorgunluk geçtikten sonraki günlerde de sürdüğünü gösteriyor.
- "Kalıcı hata bırakır" ifadesi bulgudan güçlü. Çalışma ince kuvvet kontrolü gerektiren tek bir görevde yapıldı.
- Önerilen TR: "Aşırı yorgunken yapılan çalışma beceri öğrenmeyi bozabilir ve etkisi yorgunluk geçtikten sonra da sürebilir — yorulunca tempoyu düşür ya da ara ver."
- Önerilen EN: "Practising while heavily fatigued can impair skill learning, and the effect may outlast the fatigue — slow down or rest when tired."
- Kaynak: [SC-F]

**21. "Video izlemek çalışmanın yerini tutmaz ama gözünü eğitir — ikisini birlikte kullan."** → **ONAY**
- Gözlemle öğrenme literatürüyle uyumlu: gözlem en çok fiziksel pratikle birleştiğinde katkı sağlıyor ve fiziksel pratiğin yerini nadiren tutuyor.
- Kaynak: [SC-W], [SC-O]

## Kaynaklar (erişim 2026-11-11)

- [NK-Y] Kousaku Yokota (8. dan, ASAI), "Translating the Niju kun". 20 maddenin Japonca metni, romajisi ve çevirisi: https://themartialway.com.au/?p=3629
- [NK-T] Gichin Funakoshi, Genwa Nakasone, *The Twenty Guiding Principles of Karate*, çev. John Teramoto, Kodansha International 2003 (künye: https://ci.nii.ac.jp/ncid/BA65135304). Metin bu denetimde açılmadı, yalnız künye ve madde 4 ifadesi arama sonuçlarıyla teyit edildi.
- [DK-I] Dokkōdō, Giichiro Ikeda çevirisi (1965), terebess.hu Zen arşivinde Wikipedia versiyonuyla yan yana: https://terebess.hu/zen/mesterek/musashi.html
- [DK-T] Kenji Tokitsu, *Miyamoto Musashi: His Life and Writings*, Weatherhill 2004. Dokkōdō çevirisi şu sayfadan aktarıldı: https://japanpowered.com/history/miyamato-musashis-the-way-to-be-followed-alone-dokkodo (ikincil aktarım)
- [DK-M] Kumamoto Prefectural Museum of Art (Kumamoto Kenritsu Bijutsukan), 獨行道 aslının kaydı: https://www.pref.kumamoto.jp/site/museum/9254.html
- [GR-K] 日本古典文学摘集, 五輪書 水の巻 (三八) 後書, orijinal metin: https://www.koten.net/gorin/gen/238/
- [GR-A] Aishinkan Kyoto (aikidō dojo), 鍛錬 açıklaması: https://www.aishinkankyoto.jp/tanren/
- (kontrol) Victor Harris çevirisi *A Book of Five Rings*, Su Kitabı sonu. Cümle bu çeviride yok: https://terebess.hu/zen/mesterek/A-book-of-five-rings.pdf
- [KA-IJF] International Judo Federation, "Jigoro Kano, Who Was He Really?" ve tarih sayfaları: https://www.ijf.org/history/jigoro-kano-who-was-he-really, https://www.ijf.org/history
- [KA-J] Shinichi Oimatsu (Kōdōkan), 1984, *Bulletin for the Scientific Study of Kodokan Judo* makalesi. Kano'nun ilkelerini, judonun zihin ve bedeni geliştirme amacını ve günlük hayata uygulanışını anlatıyor, jita kyōei'yi "mutual prosperity" olarak veriyor. JudoInfo yeniden basımı: https://judoinfo.com/?p=410
- [AP] Morihei Ueshiba, *The Art of Peace*, çev./derl. John Stevens. Maddeler OMLC dökümünden okundu (#38, #41, #51, #91, #93): https://omlc.org/aikido/talk/osensei/artofpeace/index.html
- [SC-D] Donovan & Radosevich (1999), "A meta-analytic review of the distribution of practice effect", *J. Applied Psychology* 84(5): 795–805. PDF: https://www.gwern.net/docs/spaced-repetition/1999-donovan.pdf
- [SC-F] Branscheidt ve ark. (2019), "Fatigue induces long-lasting detrimental changes in motor-skill learning", *eLife* 8:e40578: https://elifesciences.org/articles/40578
- [SC-W] Wulf, Shea & Lewthwaite (2010), "Motor skill learning and performance: a review of influential factors", *Medical Education*: https://pubmed.ncbi.nlm.nih.gov/20078758/
- [SC-O] Ste-Marie ve ark. gözlem müdahaleleri incelemeleri (2012; güncelleme 2020): https://www.scapps.org/jems/index.php/1/article/view/1751

## Denetim — 2026-11-11
- Sonuç: DÜZELTİLDİ (önerilen metinlerle). 13 madde ONAY, 8 madde DÜZELT, 0 madde KALDIR.
- ✅ 1–9 Niju Kun: Japonca metin ve çeviriyle karşılaştırıldı. #3 yanlış çeviri, #1'de eklenmiş yorum var.
- ⚠️ #10 Dokkōdō 1. madde: iki adlandırılmış çeviriye göre düzeltildi. Japonca asıl metin sayfa numarasıyla teyit edilmeli, edilemezse madde kaldırılmalı.
- ✅ #11–13 Dokkōdō: iki çeviride örtüşüyor. #14 orijinal metinde bulundu, kaynak etiketi düzeltildi.
- ⚠️ #15, #16, #18: kaynağın dışına taşan yorumlar çıkarıldı.
- ⚠️ #20: bilimsel bulgudan güçlü ifade yumuşatıldı.
- Kod (`app/tips_content.py`) değiştirilmedi. Öneriler B-31 kapsamında uygulanmalı.
