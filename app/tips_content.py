"""İpuçları: ünlü dövüş sanatçılarının belgelenmiş öğretilerinden ve genel,
doğrulanabilir antrenman bilgeliğinden günlük bir seçki.

DOĞRULUK KURALI (app/guide_content.py ile aynı): Burada yalnız gerçekten
belgelenmiş, kaynağı gösterilebilen öğretiler yer alır:
- Gichin Funakoshi'nin "Niju Kun" (Karatenin Yirmi İlkesi; ilk yayımı Genwa
  Nakasone'nin Karate-dō Taikan'ında, 1938 — yazılış tarihi tartışmalıdır) — her biri
  "hitotsu" (bir/ilk) ile başlar, yani orijinalinde numaralı/sıralı değildir
  ve tek bir "resmi" İngilizce/Türkçe çevirisi yoktur; burada anlam olarak
  doğrulanmış, yaygın kabul gören çeviriler kullanılır. Madde numarası iddia
  edilmez.
- Miyamoto Musashi'nin "Dokkodo" (Tek Başına Yürüme Yolu, 1645) — yaygın
  versiyonda 21 madde (bazı nüshalarda 19); çeviriler arasında kelime farkı
  olabilir, yalnız iki adlandırılmış çeviriyle örtüşen maddeler kullanılır.
- Jigoro Kano'nun (Judo'nun kurucusu) iki temel ilkesi: Seiryoku Zenyo ve
  Jita Kyoei — kendi yazılarında tanımladığı, yaygın kabul görmüş ilkeler.
- Morihei Ueshiba (Aikido kurucusu) için tam alıntı yerine öğretisinin genel
  özeti verilir (çeviriler arasında kelime farkı olabildiği için).
Uydurma/kaynağı belirsiz "motivasyon sözü" YAZILMAZ. Emin olunmayan bir
öğreti eklenmeden önce TODO.md'ye not düşülür.

`date.toordinal() % len(TIPS)` ile günlük döner (bkz. pick_daily_tip) — tablo gerekmez, deterministik.
"""

from datetime import date

TIPS: list[dict] = [
    {
        "author": "Gichin Funakoshi",
        "role_tr": "Shotokan karatenin kurucusu",
        "role_en": "Founder of Shotokan karate",
        "source": "Niju Kun (Karatenin Yirmi İlkesi)",
        "tr": "Karate nezaketle (rei) başlar, nezaketle biter.",
        "en": "Karate begins with courtesy and ends with courtesy.",
    },
    {
        "author": "Gichin Funakoshi",
        "role_tr": "Shotokan karatenin kurucusu",
        "role_en": "Founder of Shotokan karate",
        "source": "Niju Kun",
        "tr": "Karatede ilk saldırı yoktur.",
        "en": "There is no first attack in karate.",
    },
    {
        "author": "Gichin Funakoshi",
        "role_tr": "Shotokan karatenin kurucusu",
        "role_en": "Founder of Shotokan karate",
        "source": "Niju Kun",
        "tr": "Önce kendini bil, sonra başkalarını.",
        "en": "First know yourself, then know others.",
    },
    {
        "author": "Gichin Funakoshi",
        "role_tr": "Shotokan karatenin kurucusu",
        "role_en": "Founder of Shotokan karate",
        "source": "Niju Kun",
        "tr": "Önce ruh, sonra teknik.",
        "en": "Spirit first, technique second.",
    },
    {
        "author": "Gichin Funakoshi",
        "role_tr": "Shotokan karatenin kurucusu",
        "role_en": "Founder of Shotokan karate",
        "source": "Niju Kun",
        "tr": "Kazalar dikkatsizlikten doğar.",
        "en": "Accidents arise from negligence.",
    },
    {
        "author": "Gichin Funakoshi",
        "role_tr": "Shotokan karatenin kurucusu",
        "role_en": "Founder of Shotokan karate",
        "source": "Niju Kun",
        "tr": "Karate çalışmasının yalnızca dojoda olduğunu sanma.",
        "en": "Do not think that karate training is only in the dojo.",
    },
    {
        "author": "Gichin Funakoshi",
        "role_tr": "Shotokan karatenin kurucusu",
        "role_en": "Founder of Shotokan karate",
        "source": "Niju Kun",
        "tr": "Karateyi öğrenmek bir ömür alır — bunun bir sınırı yoktur.",
        "en": "It will take your entire life to learn karate; there is no limit.",
    },
    {
        "author": "Gichin Funakoshi",
        "role_tr": "Shotokan karatenin kurucusu",
        "role_en": "Founder of Shotokan karate",
        "source": "Niju Kun",
        "tr": "Karate kaynayan su gibidir — sürekli ısıtmazsan soğur.",
        "en": "Karate is like boiling water — if you do not heat it constantly, it will cool.",
    },
    {
        "author": "Gichin Funakoshi",
        "role_tr": "Shotokan karatenin kurucusu",
        "role_en": "Founder of Shotokan karate",
        "source": "Niju Kun",
        "tr": "Kazanman gerektiğini değil, kaybetmemen gerektiğini düşün.",
        "en": "Do not think that you have to win; think rather that you do not have to lose.",
    },
    {
        "author": "Miyamoto Musashi",
        "role_tr": "Kılıç ustası, Go Rin no Sho'nun yazarı",
        "role_en": "Swordsman, author of The Book of Five Rings",
        "source": "Dokkodo",
        "tr": "Kendini hafife al, dünyayı derinden düşün.",
        "en": "Think lightly of yourself and deeply of the world.",
    },
    {
        "author": "Miyamoto Musashi",
        "role_tr": "Kılıç ustası, Go Rin no Sho'nun yazarı",
        "role_en": "Swordsman, author of The Book of Five Rings",
        "source": "Dokkodo",
        "tr": "Yaptığın şeye pişman olma.",
        "en": "Do not regret what you have done.",
    },
    {
        "author": "Miyamoto Musashi",
        "role_tr": "Kılıç ustası, Go Rin no Sho'nun yazarı",
        "role_en": "Swordsman, author of The Book of Five Rings",
        "source": "Dokkodo",
        "tr": "Asla kıskanma.",
        "en": "Never be jealous.",
    },
    {
        "author": "Miyamoto Musashi",
        "role_tr": "Kılıç ustası, Go Rin no Sho'nun yazarı",
        "role_en": "Swordsman, author of The Book of Five Rings",
        "source": "Go Rin no Sho (Beş Halka Kitabı), Su Kitabı",
        "tr": "Bin günlük çalışma temeli döver, on bin günlük çalışma onu arıtır.",
        "en": "A thousand days of training to forge, ten thousand days of training to refine.",
    },
    {
        "author": "Jigoro Kano",
        "role_tr": "Judo'nun kurucusu",
        "role_en": "Founder of Judo",
        "source": "Seiryoku Zenyo ilkesi",
        "tr": "Seiryoku zenyo: zihnini ve bedenini en verimli şekilde kullan — yalnız tatamide değil, günlük hayatta da.",
        "en": "Seiryoku zenyo: maximum efficient use of mind and body — on the mat and in daily life.",
    },
    {
        "author": "Jigoro Kano",
        "role_tr": "Judo'nun kurucusu",
        "role_en": "Founder of Judo",
        "source": "Jita Kyoei ilkesi",
        "tr": "Jita kyoei: karşılıklı yardım ve fayda — kendinle birlikte başkalarının da gelişmesini gözet.",
        "en": "Jita kyoei: mutual welfare and benefit — progress together with others.",
    },
    {
        "author": "Morihei Ueshiba",
        "role_tr": "Aikido'nun kurucusu",
        "role_en": "Founder of Aikido",
        "source": "Öğretisinin genel özeti (The Art of Peace derlemesi)",
        "tr": "Aikido rakibi yenmeyi değil, çatışmayı uyum içinde çözmeyi öğretir.",
        "en": "Aikido teaches resolving conflict through harmony, not defeating an opponent.",
    },
    {
        "author": "Morihei Ueshiba",
        "role_tr": "Aikido'nun kurucusu",
        "role_en": "Founder of Aikido",
        "source": "Öğretisinin genel özeti (The Art of Peace derlemesi)",
        "tr": "Gün be gün çalış ve tekniğini incelt; kendini hiçbir zaman tamamlanmış bir usta sayma, başkalarıyla birlikte çalışmayı sürdür.",
        "en": "Train day after day and refine your technique; never think of yourself as a finished master — keep training together with others.",
    },
    # Genel, kaynağı kişiye bağlı olmayan, doğrulanabilir antrenman bilgeliği
    # (guide_content.py'deki "İpuçları" bölümleriyle aynı üslup).
    {
        "author": None,
        "source": "Genel antrenman bilgeliği",
        "tr": "Kısa ve düzenli tekrar, uzun ve düzensiz seanslardan daha kalıcıdır.",
        "en": "Short, regular repetition builds more lasting skill than long, irregular sessions.",
    },
    {
        "author": None,
        "source": "Genel antrenman bilgeliği",
        "tr": "Aşırı yorgunken yapılan çalışma beceri öğrenmeyi bozabilir ve etkisi yorgunluk geçtikten sonra da sürebilir — yorulunca tempoyu düşür ya da ara ver.",
        "en": "Practising while heavily fatigued can impair skill learning, and the effect may outlast the fatigue — slow down or rest when tired.",
    },
    {
        "author": None,
        "source": "Genel antrenman bilgeliği",
        "tr": "Video izlemek çalışmanın yerini tutmaz ama gözünü eğitir — ikisini birlikte kullan.",
        "en": "Watching video isn't a substitute for training, but it trains the eye — use both together.",
    },
]


def pick_daily_tip(today: date) -> dict:
    """Tarihe göre deterministik günlük ipucu: aynı gün herkes aynısını görür."""
    return TIPS[today.toordinal() % len(TIPS)]
