"""İpuçları: ünlü dövüş sanatçılarının belgelenmiş öğretilerinden ve genel,
doğrulanabilir antrenman bilgeliğinden günlük bir seçki.

DOĞRULUK KURALI (app/guide_content.py ile aynı): Burada yalnız gerçekten
belgelenmiş, kaynağı gösterilebilen öğretiler yer alır:
- Gichin Funakoshi'nin "Niju Kun" (Karatenin Yirmi İlkesi, 1938) — her biri
  "hitotsu" (bir/ilk) ile başlar, yani orijinalinde numaralı/sıralı değildir
  ve tek bir "resmi" İngilizce/Türkçe çevirisi yoktur; burada anlam olarak
  doğrulanmış, yaygın kabul gören çeviriler kullanılır. Madde numarası iddia
  edilmez.
- Miyamoto Musashi'nin "Dokkodo" (Tek Başına Yürüme Yolu, 1645) — 21
  maddelik öz-disiplin metni; çeviriler arasında kelime farkı olabilir,
  anlam olarak doğrulanmış maddeler kullanılır.
- Jigoro Kano'nun (Judo'nun kurucusu) iki temel ilkesi: Seiryoku Zenyo ve
  Jita Kyoei — kendi yazılarında tanımladığı, yaygın kabul görmüş ilkeler.
- Morihei Ueshiba (Aikido kurucusu) için tam alıntı yerine öğretisinin genel
  özeti verilir (çeviriler arasında kelime farkı olabildiği için).
Uydurma/kaynağı belirsiz "motivasyon sözü" YAZILMAZ. Emin olunmayan bir
öğreti eklenmeden önce TODO.md'ye not düşülür.

`day_of_year % len(TIPS)` ile günlük döner — tablo gerekmez, deterministik.
"""

TIPS: list[dict] = [
    {
        "author": "Gichin Funakoshi",
        "role_tr": "Shotokan karatenin kurucusu",
        "role_en": "Founder of Shotokan karate",
        "source": "Niju Kun (Karatenin Yirmi İlkesi)",
        "tr": "Karate nezaketle (rei) başlar, nezaketle biter — teknikten önce saygı gelir.",
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
        "tr": "Başkalarını kontrol etmeye kalkışmadan önce kendini kontrol et.",
        "en": "First control yourself before attempting to control others.",
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
        "tr": "Her şeyi olduğu gibi kabul et.",
        "en": "Accept everything just the way it is.",
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
        "source": "Go Rin no Sho (Beş Halka Kitabı) — yaygın çeviriyle",
        "tr": "Bin gün çalışmak dövmek (temel atmak), on bin gün çalışmak cilalamaktır (ustalaşmaktır).",
        "en": "A thousand days of training to forge, ten thousand days of training to refine.",
    },
    {
        "author": "Jigoro Kano",
        "role_tr": "Judo'nun kurucusu",
        "role_en": "Founder of Judo",
        "source": "Seiryoku Zenyo ilkesi",
        "tr": "Seiryoku zenyo: enerjini en verimli şekilde kullan — güçle değil, doğru zamanlamayla kazan.",
        "en": "Seiryoku zenyo: maximum efficient use of energy — win with timing, not brute force.",
    },
    {
        "author": "Jigoro Kano",
        "role_tr": "Judo'nun kurucusu",
        "role_en": "Founder of Judo",
        "source": "Jita Kyoei ilkesi",
        "tr": "Jita kyoei: karşılıklı fayda ve ortak gelişim — antrenman partnerin senin en iyi öğretmenin.",
        "en": "Jita kyoei: mutual welfare and benefit — your training partner is one of your best teachers.",
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
        "tr": "Gerçek çalışma günlük tekrardır — bir kerelik ilham değil, her gün dönüp gelen sadakattir.",
        "en": "True practice is daily repetition — not a one-time inspiration, but a discipline you return to every day.",
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
        "tr": "Yorgunken çalışılan teknik, dinlenmişken çalışılandan daha kalıcı hata bırakır — dikkatli ol.",
        "en": "Technique practiced while fatigued leaves more lasting mistakes than technique practiced while fresh — be careful.",
    },
    {
        "author": None,
        "source": "Genel antrenman bilgeliği",
        "tr": "Video izlemek çalışmanın yerini tutmaz ama gözünü eğitir — ikisini birlikte kullan.",
        "en": "Watching video isn't a substitute for training, but it trains the eye — use both together.",
    },
]
