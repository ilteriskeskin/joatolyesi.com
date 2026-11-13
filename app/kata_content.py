"""Kata/teknik detay sayfaları için slug'a göre içerik (B-40 şablonu, B-37 ilk parti).

İÇERİK KURALI: Metinler yalnız docs/team/content/verified/ altındaki fact-checker onaylı
dosyalardan aynen alınır (kaynak: 2026-11-13-b37-ilk-5-sayfa.md). Burada olmayan slug
sayfası eski görünümde kalır. Onaylı dosyada EN için yalnız title/meta/özet vardır;
bu yüzden EN'de adımlar ve hatalar boştur (şablon boş bölümü göstermez).

Yapı: CONTENT[slug][lang] = {title, meta, nedir, adimlar, sik_hatalar, ilgili}.
`ilgili` slug listesidir; DB'de olmayanlar sayfada atlanır.
"""

CONTENT: dict[str, dict[str, dict]] = {
    "tkd-dwit-chagi": {
        "tr": {
            "title": "Dwit chagi (geri tekme) nedir, nasıl yapılır?",
            "meta": "Dwit chagi, taekwondoda topukla yapılan geri tekmedir. Adımlarını, sık yapılan hataları ve ilgili tekmeleri bu rehberde bul.",
            "nedir": (
                'Dwit chagi ("dwi chagi" diye de yazılır) taekwondonun geri tekmesidir. Vücut hedeften dönülür, '
                "ardından arka bacak düz bir hatta hedefe sürülür. Vuruş yüzeyi topuktur. Dönüş dairesel bir spin "
                "değildir: önce gövde döner, sonra tekme düz bir çizgide gider."
            ),
            "adimlar": [
                "Dövüş duruşundan, ayaklarının ön kısmı üzerinde dönerek sırtını hedefe çevir.",
                "Dönüş boyunca rakibi gözden kaçırma. Taekwondo kaynaklarının çoğu omuz üstünden bakmayı öğretir. Bazı eğitmenler ise koltuk altından ya da düz bakmayı önerir. Okulunun tarifini hocana sor.",
                "Tekme atacak bacağın ayağını destek bacağının dizine yakın çek.",
                "Bacağı düz bir hatta geri sür. Ayak bileği bükülü, parmaklar hafif aşağı baksın; yalnız topuk temas etsin.",
                "Bacağı aynı hattan geri topla, sonra ayağı yere bırak ve dengede kal.",
            ],
            "sik_hatalar": [
                "Bacağı düz hat yerine daire çizerek savurmak.",
                "Topuk yerine ayak tabanının ön kısmıyla vurmak.",
                "Başı geç döndürüp rakibi bir an görememek.",
                "Bacağı geri toplamadan yere bırakmak ya da dönüşte savrulup dengeyi kaybetmek.",
            ],
            "ilgili": ["tkd-ap-chagi", "tkd-yop-chagi", "tkd-dollyo-chagi"],
        },
        "en": {
            "title": "Dwit chagi (back kick): what it is and how to do it",
            "meta": "Dwit chagi is taekwondo's back kick, delivered with the heel. Learn the steps, common mistakes and related kicks.",
            "nedir": (
                "Dwit chagi (also spelled dwi chagi) turns the body away from the target and drives the rear leg "
                "straight back, striking with the heel. It is a turn followed by a linear kick, not a circular spin. "
                "Chamber the foot near the supporting knee, kick in a straight line with the ankle flexed, then pull "
                "the leg back along the same line before setting it down. Most taekwondo sources teach looking over "
                "the shoulder; some coaches prefer other cues, so follow your instructor. Common errors: circling the "
                "leg, hitting with the ball of the foot, turning the head late, dropping the leg without re-chambering. "
                "Related: front kick, side kick, roundhouse."
            ),
            "adimlar": [],
            "sik_hatalar": [],
            "ilgili": ["tkd-ap-chagi", "tkd-yop-chagi", "tkd-dollyo-chagi"],
        },
    },
    "karate-zenkutsu-dachi": {
        "tr": {
            "title": "Zenkutsu dachi nedir, nasıl yapılır?",
            "meta": "Zenkutsu dachi, karatenin ileri duruşudur. Ayak mesafesi, ön diz, arka bacak ve ağırlık dağılımını adım adım ve sık hatalarla öğren.",
            "nedir": (
                "Zenkutsu dachi karatenin ileri duruşudur. Duruş uzun ve görece dardır, ön diz bükülür ve ağırlığın "
                "çoğu ön bacağa verilir. Ağırlık oranı ve arka bacağın konumu kaynağa ve ekole göre değişir (aşağıya bak)."
            ),
            "adimlar": [
                "Ayakları uzun ve dar bir duruşta yerleştir. Yaygın tarif yana yaklaşık bir, ileri yaklaşık iki omuz genişliğidir. Uygun uzunluk, yapılan tekniğe göre değişir.",
                "Ön dizi bük, ön ayak ileri baksın.",
                "Arka bacağı uzat. Birçok tarifte arka bacak düz ya da neredeyse düzdür. Bazı ekoller arka dizi hafif bükük tutar. Arka ayak hafifçe dışa döner, açı kaynağa göre değişir. Okulunun tarifini hocana sor.",
                "Ağırlığın çoğunu ön bacağa ver. Kaynaklar farklı oranlar verir: 60/40, yaklaşık üçte iki ya da yaklaşık %80.",
            ],
            "sik_hatalar": [
                "Duruşu gereğinden kısa ya da uzun kurmak. Kısa duruşta denge kolay bozulur. Fazla uzun duruş hareketi yavaşlatır ve beli zorlayabilir.",
                "Arka ayağı aşırı dışa açmak ya da yanlış yöne çevirmek.",
            ],
            "ilgili": ["karate-kokutsu-dachi", "karate-kiba-dachi", "karate-choku-tsuki", "karate-oi-tsuki"],
        },
        "en": {
            "title": "Zenkutsu dachi: what it is and how to do it",
            "meta": "Zenkutsu dachi is karate's front stance. Learn foot spacing, front knee, rear leg and weight distribution, plus common mistakes.",
            "nedir": (
                "Zenkutsu dachi is a long, fairly narrow stance with a bent front knee and most of the weight on the "
                "front leg. A common guideline is about one shoulder-width across and two front to back, adjusted to "
                "the technique. The rear leg is straight or nearly straight in most descriptions, though some schools "
                "keep a slight bend. The rear foot turns out slightly, at an angle that varies by source. Weight ratios "
                "also vary (60/40, about two-thirds, about 80%), so follow your instructor. Common errors: a stance too "
                "short or too long, and a rear foot turned out too far. Related: kokutsu dachi, kiba dachi, choku tsuki, oi tsuki."
            ),
            "adimlar": [],
            "sik_hatalar": [],
            "ilgili": ["karate-kokutsu-dachi", "karate-kiba-dachi", "karate-choku-tsuki", "karate-oi-tsuki"],
        },
    },
    "tkd-naeryo-chagi": {
        "tr": {
            "title": "Naeryo chagi (baltalama tekmesi) nedir, nasıl yapılır?",
            "meta": "Naeryo chagi, taekwondoda topuğun yukarıdan aşağı indiği baltalama tekmesidir. Adımları ve sık yapılan hataları bu rehberde bul.",
            "nedir": (
                'Naeryo chagi ("naeryeo chagi" diye de yazılır) taekwondonun baltalama tekmesidir (axe kick). Bacak '
                "yukarı kaldırılır, sonra topuk ya da ayak tabanı hedefe yukarıdan aşağı indirilir."
            ),
            "adimlar": [
                "Dengeli bir duruştan başla. Destek dizi hafif bükük olsun, destek ayağı biraz dışa dönsün.",
                "Bacağı hedefin üzerine kaldır. Kaynaklar farklı yollar anlatır: bacağı düz kaldırmak, içten ya da dıştan yay çizerek kaldırmak ya da önce dizi göğüs hizasına çekmek.",
                "Tepe noktasından topuğu (ya da ayak tabanını) hedefe doğru aşağı indir.",
                "Tekmeden sonra ayağı kontrollü biçimde yere bırak ve dengeni koru.",
            ],
            "sik_hatalar": [
                "Bacağı kontrol edebileceğinden yükseğe kaldırmak. Denge geriye kaçar, düşme riski doğar.",
                "Tekmeden sonra dengeyi kaybetmek.",
            ],
            "ilgili": ["tkd-ap-chagi", "tkd-dollyo-chagi", "tkd-yop-chagi", "tkd-dwit-chagi"],
        },
        "en": {
            "title": "Naeryo chagi (axe kick): what it is and how to do it",
            "meta": "Naeryo chagi is taekwondo's axe kick: the leg rises and the heel drops down. Learn the steps and common mistakes.",
            "nedir": (
                "Naeryo chagi (also spelled naeryeo chagi) raises the leg above the target and brings the heel or sole "
                "down onto it. Start balanced with the standing knee slightly bent and the standing foot turned a little "
                "outward. Lift the leg straight, in an arc, or from a chest-level chamber depending on your school, drop "
                "the heel, then set the foot down under control. Common errors: lifting higher than you can control, "
                "losing balance after the kick. Related: front kick, roundhouse, side kick, back kick."
            ),
            "adimlar": [],
            "sik_hatalar": [],
            "ilgili": ["tkd-ap-chagi", "tkd-dollyo-chagi", "tkd-yop-chagi", "tkd-dwit-chagi"],
        },
    },
    "karate-kiba-dachi": {
        "tr": {
            "title": "Kiba dachi nedir, nasıl yapılır?",
            "meta": "Kiba dachi, karatenin binici duruşudur. Ayak genişliği, diz ve sırt yerleşimi ile sık yapılan hataları adım adım öğren.",
            "nedir": (
                'Kiba dachi ("binici duruşu") karatede ayakların paralel ve geniş açıldığı, dizlerin büküldüğü ve '
                "ağırlığın iki ayağa eşit dağıldığı temel duruştur. Sırt dik tutulur. Ayak genişliği ve duruş yüksekliği "
                "okula göre değişir. Ayakların paralel olması ortak özelliktir."
            ),
            "adimlar": [
                "Ayakları paralel ve ileri bakacak şekilde, omuz genişliğinden geniş aç. Tarifler bir ile iki omuz genişliği arasında değişir.",
                "Dizleri bükerek alçal ve ağırlığı iki ayağa eşit ver.",
                "Sırtı dik tut.",
                "Dizleri hafifçe dışa doğru tut ve içe çökmelerine izin verme. Bazı tariflerde diz ve ayaklar hafif içe bakar. Okulunun tarifini hocana sor.",
            ],
            "sik_hatalar": [
                "Dizlerin içe çökmesi.",
                "Ayakların paralelliğini bozup ayak uçlarını dışa açmak.",
                "Gövdeyi öne eğmek ya da kalçayı geriye çıkarmak. Sırt dik kalmalı.",
            ],
            "ilgili": ["karate-zenkutsu-dachi", "karate-kokutsu-dachi", "karate-choku-tsuki"],
        },
        "en": {
            "title": "Kiba dachi (horse stance): what it is and how to do it",
            "meta": "Kiba dachi is karate's horse stance: wide, parallel feet, low centre. Learn set-up, knee position and common mistakes.",
            "nedir": (
                "Kiba dachi uses wide, parallel feet (one to two shoulder-widths, depending on the source), bent knees, "
                "weight shared evenly and an upright back. Width and height vary by school. Most descriptions keep the "
                "knees pressed slightly outward, though some teach a slight inward angle, so follow your instructor. "
                "Common errors: knees collapsing inward, feet turning out, leaning forward or sticking the hips back. "
                "Related: zenkutsu dachi, kokutsu dachi, choku tsuki."
            ),
            "adimlar": [],
            "sik_hatalar": [],
            "ilgili": ["karate-zenkutsu-dachi", "karate-kokutsu-dachi", "karate-choku-tsuki"],
        },
    },
}


def get_kata_content(slug: str, lang: str) -> dict | None:
    """Slug için içerik; yoksa None (sayfa eski görünümde kalır). Dil yoksa TR'ye düşer."""
    entry = CONTENT.get(slug)
    if not entry:
        return None
    return entry.get("en" if lang == "en" else "tr") or entry.get("tr")
