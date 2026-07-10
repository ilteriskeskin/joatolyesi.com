"""İçerik kataloğu: branş bazlı kata/vuruş kütüphanesi + 30 günlük program.

Kata kataloğu her açılışta slug üzerinden upsert edilir (idempotent) —
başlık/açıklama/branş düzeltmeleri deploy ile yayılır. Video URL'leri
sahibin çekimleri hazır olana dek boş.

Kaynaklar: ZNKR Seitei Jōdō ve Seitei Iai müfredatı, Nihon Kendō Kata,
Shintō Musō-ryū kihon seti, Saito yöntemi aiki-jo 20 suburi / aiki-ken
nana suburi, Shotokan kata ve WT Taegeuk poomsae listeleri.
"""

from sqlalchemy import func, select
from sqlalchemy.dialects.postgresql import insert as pg_insert

from app.db import async_session
from app.models import Kata, Program, ProgramDay


def _k(slug: str, title: str, en: str, tr: str, free: bool = False) -> dict:
    return {"slug": slug, "title_en": title, "title_tr": title,
            "description_en": en, "description_tr": tr, "is_free": free}


# --- Aiki-jo: Saito yöntemi 20 suburi + 2 solo kata ---
AIKIJO = [
    _k("choku-tsuki", "Choku tsuki",
       "Tsuki group 1/5 — the direct thrust, first of the 20 jo suburi.",
       "Tsuki grubu 1/5 — doğrudan saplama, 20 jo suburi'nin ilki.", True),
    _k("kaeshi-tsuki", "Kaeshi tsuki",
       "Tsuki group 2/5 — counter thrust with a turning grip change.",
       "Tsuki grubu 2/5 — dönerek tutuş değiştiren karşı saplama."),
    _k("ushiro-tsuki", "Ushiro tsuki",
       "Tsuki group 3/5 — thrust to the rear.",
       "Tsuki grubu 3/5 — geriye saplama."),
    _k("tsuki-gedan-gaeshi", "Tsuki gedan gaeshi",
       "Tsuki group 4/5 — thrust followed by a low sweeping return.",
       "Tsuki grubu 4/5 — saplamanın ardından alçak süpürme dönüşü."),
    _k("tsuki-jodan-gaeshi", "Tsuki jodan gaeshi uchi",
       "Tsuki group 5/5 — thrust into a high turning strike.",
       "Tsuki grubu 5/5 — saplamadan yüksek dönüş vuruşuna geçiş."),
    _k("shomen-uchikomi", "Shomen uchikomi",
       "Uchikomi group 1/5 — overhead strike to the centre line.",
       "Uchikomi grubu 1/5 — merkez hatta tepeden vuruş.", True),
    _k("renzoku-uchikomi", "Renzoku uchikomi",
       "Uchikomi group 2/5 — continuous alternating strikes.",
       "Uchikomi grubu 2/5 — kesintisiz dönüşümlü vuruşlar."),
    _k("menuchi-gedan-gaeshi", "Menuchi gedan gaeshi",
       "Uchikomi group 3/5 — head strike into a low sweeping return.",
       "Uchikomi grubu 3/5 — kafa vuruşundan alçak süpürme dönüşü."),
    _k("menuchi-ushiro-tsuki", "Menuchi ushiro tsuki",
       "Uchikomi group 4/5 — head strike, then thrust to the rear.",
       "Uchikomi grubu 4/5 — kafa vuruşu, ardından geriye saplama."),
    _k("gyaku-yokomen-ushiro-tsuki", "Gyaku yokomen ushiro tsuki",
       "Uchikomi group 5/5 — reverse side strike, then rear thrust.",
       "Uchikomi grubu 5/5 — ters yan vuruş, ardından geriye saplama."),
    _k("katate-gedan-gaeshi", "Katate gedan gaeshi",
       "Katate group 1/3 — one-handed low sweep and return.",
       "Katate grubu 1/3 — tek elle alçak süpürme ve dönüş."),
    _k("katate-toma-uchi", "Katate toma uchi",
       "Katate group 2/3 — long-distance one-handed strike.",
       "Katate grubu 2/3 — uzak mesafeden tek el vuruşu."),
    _k("katate-hachi-no-ji", "Katate hachi no ji gaeshi",
       "Katate group 3/3 — one-handed figure-eight turning pattern.",
       "Katate grubu 3/3 — tek elle sekiz çizen dönüş deseni."),
    _k("hasso-gaeshi-uchi", "Hasso gaeshi uchi",
       "Hasso group 1/5 — figure-eight return into an overhead strike.",
       "Hasso grubu 1/5 — sekiz dönüşünden tepeden vuruş."),
    _k("hasso-gaeshi-tsuki", "Hasso gaeshi tsuki",
       "Hasso group 2/5 — figure-eight return into a thrust.",
       "Hasso grubu 2/5 — sekiz dönüşünden saplama."),
    _k("hasso-gaeshi-ushiro-tsuki", "Hasso gaeshi ushiro tsuki",
       "Hasso group 3/5 — figure-eight return, thrust to the rear.",
       "Hasso grubu 3/5 — sekiz dönüşü, geriye saplama."),
    _k("hasso-gaeshi-ushiro-uchi", "Hasso gaeshi ushiro uchi",
       "Hasso group 4/5 — figure-eight return, strike to the rear.",
       "Hasso grubu 4/5 — sekiz dönüşü, geriye vuruş."),
    _k("hasso-gaeshi-ushiro-barai", "Hasso gaeshi ushiro barai",
       "Hasso group 5/5 — figure-eight return, sweep to the rear.",
       "Hasso grubu 5/5 — sekiz dönüşü, geriye süpürme."),
    _k("hidari-nagare-gaeshi-uchi", "Hidari nagare gaeshi uchi",
       "Nagare group 1/2 — flowing turn to the left ending in a strike.",
       "Nagare grubu 1/2 — sola akışkan dönüş, vuruşla biter."),
    _k("migi-nagare-gaeshi-tsuki", "Migi nagare gaeshi tsuki",
       "Nagare group 2/2 — flowing turn to the right ending in a thrust.",
       "Nagare grubu 2/2 — sağa akışkan dönüş, saplamayla biter."),
    _k("sanjuichi-no-jo", "31 no jo kata",
       "The 31-count solo kata — the backbone of aiki-jo practice.",
       "31 sayılık solo kata — aiki-jo çalışmasının omurgası."),
    _k("jusan-no-jo", "13 no jo kata",
       "The 13-count solo kata; compact and rhythm-focused.",
       "13 sayılık solo kata; kompakt ve ritim odaklı."),
]

# --- Aiki-ken (bokken): nana suburi + happo giri ---
BOKKEN = [
    _k("bokken-shomen-suburi", "Aiki-ken suburi 1 — Shomen",
       "First of the seven aiki-ken suburi: the vertical cut.",
       "Yedi aiki-ken suburi'nin ilki: dikey kesiş.", True),
    _k("aiki-ken-suburi-2", "Aiki-ken suburi 2",
       "Shomen cut with a stepping withdrawal and re-entry.",
       "Geri çekilip yeniden girerek yapılan shomen kesişi."),
    _k("aiki-ken-suburi-3", "Aiki-ken suburi 3",
       "Cut driven from a rear jodan chamber, stepping through.",
       "Arkadan jodan pozisyonundan adım alarak kesiş."),
    _k("aiki-ken-suburi-4", "Aiki-ken suburi 4",
       "Continuous alternating shomen cuts, advancing each step.",
       "Her adımda ilerleyen kesintisiz dönüşümlü shomen kesişleri."),
    _k("aiki-ken-suburi-5", "Aiki-ken suburi 5",
       "Alternating diagonal cuts combined with body turns.",
       "Gövde dönüşleriyle birleşen dönüşümlü çapraz kesişler."),
    _k("aiki-ken-suburi-6", "Aiki-ken suburi 6",
       "Stepping cuts combined with a thrust (tsuki).",
       "Saplama (tsuki) ile birleşen adımlı kesişler."),
    _k("aiki-ken-suburi-7", "Aiki-ken suburi 7",
       "The full combination: cut, turn and thrust in one flow.",
       "Tam kombinasyon: tek akışta kesiş, dönüş ve saplama."),
    _k("bokken-happo-giri", "Happo giri",
       "Eight-direction cutting practice.",
       "Sekiz yöne kesiş çalışması."),
]

# --- ZNKR Seitei Jōdō: 12 kata ---
JODO = [
    _k("jodo-tsukizue", "Tsukizue",
       "Seitei Jōdō kata 1 — 'leaning on the staff'; opens the set.",
       "Seitei Jōdō kata 1 — 'bastona dayanma'; seriyi açar.", True),
    _k("jodo-suigetsu", "Suigetsu",
       "Seitei Jōdō kata 2 — thrust to the solar plexus (suigetsu).",
       "Seitei Jōdō kata 2 — güneş sinirağına (suigetsu) saplama."),
    _k("jodo-hissage", "Hissage",
       "Seitei Jōdō kata 3 — the jo held hidden, drawn at the last moment.",
       "Seitei Jōdō kata 3 — jo gizli tutulur, son anda çıkar."),
    _k("jodo-shamen", "Shamen",
       "Seitei Jōdō kata 4 — strike to the side of the head.",
       "Seitei Jōdō kata 4 — başın yan tarafına vuruş."),
    _k("jodo-sakan", "Sakan",
       "Seitei Jōdō kata 5 — controlling the sword from the left side.",
       "Seitei Jōdō kata 5 — kılıcı sol taraftan kontrol etme."),
    _k("jodo-monomi", "Monomi",
       "Seitei Jōdō kata 6 — 'the lookout'; watching, then intercepting.",
       "Seitei Jōdō kata 6 — 'gözcü'; izleyip araya girme."),
    _k("jodo-kasumi", "Kasumi",
       "Seitei Jōdō kata 7 — 'mist'; deceptive covering movement.",
       "Seitei Jōdō kata 7 — 'sis'; yanıltıcı örtme hareketi."),
    _k("jodo-tachi-otoshi", "Tachi otoshi",
       "Seitei Jōdō kata 8 — dropping the sword with a strike.",
       "Seitei Jōdō kata 8 — vuruşla kılıcı düşürme."),
    _k("jodo-rai-uchi", "Rai uchi",
       "Seitei Jōdō kata 9 — 'thunder strike'; from the chūdan series.",
       "Seitei Jōdō kata 9 — 'gök gürültüsü vuruşu'; chūdan serisinden."),
    _k("jodo-seigan", "Seigan",
       "Seitei Jōdō kata 10 — thrust toward the eyes from chūdan.",
       "Seitei Jōdō kata 10 — chūdan'dan gözlere doğru saplama."),
    _k("jodo-midare-dome", "Midare dome",
       "Seitei Jōdō kata 11 — 'stopping the disorder'; complex exchanges.",
       "Seitei Jōdō kata 11 — 'karmaşayı durdurma'; yoğun değişimler."),
    _k("jodo-ran-ai", "Ran ai",
       "Seitei Jōdō kata 12 — the longest kata of the set; closes the series.",
       "Seitei Jōdō kata 12 — setin en uzun kataı; seriyi kapatır."),
]

# --- Shintō Musō-ryū jōjutsu: 12 kihon ---
JOJUTSU = [
    _k("smr-honte-uchi", "Honte uchi",
       "SMR kihon 1 — the fundamental strike with the natural grip.",
       "SMR kihon 1 — doğal tutuşla temel vuruş.", True),
    _k("smr-gyakute-uchi", "Gyakute uchi",
       "SMR kihon 2 — strike with the reversed grip.",
       "SMR kihon 2 — ters tutuşla vuruş."),
    _k("smr-hikiotoshi-uchi", "Hikiotoshi uchi",
       "SMR kihon 3 — dropping strike that knocks the sword down.",
       "SMR kihon 3 — kılıcı aşağı düşüren indirme vuruşu."),
    _k("smr-kaeshi-tsuki", "Kaeshi tsuki",
       "SMR kihon 4 — counter thrust.",
       "SMR kihon 4 — karşı saplama."),
    _k("smr-gyakute-tsuki", "Gyakute tsuki",
       "SMR kihon 5 — thrust from the reversed grip.",
       "SMR kihon 5 — ters tutuştan saplama."),
    _k("smr-maki-otoshi", "Maki otoshi",
       "SMR kihon 6 — wrapping the sword and dropping it.",
       "SMR kihon 6 — kılıcı sarıp düşürme."),
    _k("smr-kuritsuke", "Kuritsuke",
       "SMR kihon 7 — pinning the sword arm against the body.",
       "SMR kihon 7 — kılıç kolunu gövdeye sabitleme."),
    _k("smr-kurihanashi", "Kurihanashi",
       "SMR kihon 8 — pinning and then casting the sword away.",
       "SMR kihon 8 — sabitleyip kılıcı savurarak uzaklaştırma."),
    _k("smr-taiatari", "Taiatari",
       "SMR kihon 9 — body check delivered with the jo.",
       "SMR kihon 9 — jo ile yapılan gövde çarpması."),
    _k("smr-tsukihazushi-uchi", "Tsukihazushi uchi",
       "SMR kihon 10 — evading the thrust and striking.",
       "SMR kihon 10 — saplamadan sıyrılıp vurma."),
    _k("smr-dobarai-uchi", "Dobarai uchi",
       "SMR kihon 11 — sweeping the torso cut aside and striking.",
       "SMR kihon 11 — gövde kesişini süpürüp vurma."),
    _k("smr-taihazushi-uchi", "Taihazushi uchi",
       "SMR kihon 12 — shifting the body off line and striking.",
       "SMR kihon 12 — gövdeyi hattan çıkarıp vurma."),
]

# --- Kenjutsu: temel kesişler ---
KENJUTSU = [
    _k("ken-shomen-giri", "Shomen giri",
       "The vertical cut to the centre of the head — the foundation of all sword work.",
       "Başın merkezine dikey kesiş — tüm kılıç çalışmasının temeli.", True),
    _k("ken-kesa-giri", "Kesa giri",
       "Diagonal cut following the line of the monk's sash (kesa).",
       "Keşiş kuşağı (kesa) hattını izleyen çapraz kesiş."),
    _k("ken-gyaku-kesa", "Gyaku kesa giri",
       "Rising diagonal cut from below.",
       "Aşağıdan yükselen çapraz kesiş."),
    _k("ken-do-giri", "Do giri",
       "Horizontal cut across the trunk.",
       "Gövdeye yatay kesiş."),
    _k("ken-tsuki", "Tsuki",
       "Straight thrust with the point.",
       "Uçla düz saplama."),
]

# --- Kendo: 4 temel vuruş + Nihon Kendō Kata (7 tachi + 3 kodachi) ---
KENDO = [
    _k("kendo-men", "Men uchi",
       "Strike to the head — the first of kendo's four target strikes.",
       "Kafaya vuruş — kendonun dört hedef vuruşunun ilki.", True),
    _k("kendo-kote", "Kote uchi",
       "Strike to the wrist.",
       "Bileğe vuruş."),
    _k("kendo-do", "Do uchi",
       "Strike to the trunk.",
       "Gövdeye vuruş."),
    _k("kendo-tsuki", "Tsuki",
       "Thrust to the throat guard.",
       "Boğaz korumasına saplama."),
] + [
    _k(f"kendo-kata-{i}", f"Nihon Kendō Kata {i} ({name})",
       f"Kendō kata {i} — tachi (long sword) form, uchidachi vs shidachi.",
       f"Kendō kata {i} — tachi (uzun kılıç) formu, uchidachi–shidachi.")
    for i, name in [(1, "Ipponme"), (2, "Nihonme"), (3, "Sanbonme"),
                    (4, "Yonhonme"), (5, "Gohonme"), (6, "Ropponme"), (7, "Nanahonme")]
] + [
    _k(f"kendo-kodachi-{i}", f"Kodachi Kata {i}",
       f"Kendō kodachi kata {i} — short sword against long sword.",
       f"Kendō kodachi kata {i} — uzun kılıca karşı kısa kılıç.")
    for i in (1, 2, 3)
]

# --- ZNKR Seitei Iai: 12 kata ---
IAIDO = [
    _k("iaido-mae", "Mae",
       "Seitei Iai kata 1 — draw and cut against an opponent in front, from seiza.",
       "Seitei Iai kata 1 — seiza'dan öndeki rakibe çekiş ve kesiş.", True),
    _k("iaido-ushiro", "Ushiro",
       "Seitei Iai kata 2 — turning draw against an opponent behind.",
       "Seitei Iai kata 2 — arkadaki rakibe dönerek çekiş."),
    _k("iaido-ukenagashi", "Ukenagashi",
       "Seitei Iai kata 3 — flowing parry that turns into a cut.",
       "Seitei Iai kata 3 — kesişe dönüşen akışkan savuşturma."),
    _k("iaido-tsuka-ate", "Tsuka-ate",
       "Seitei Iai kata 4 — strike with the hilt, then cut; from tatehiza.",
       "Seitei Iai kata 4 — kabzayla vuruş, ardından kesiş; tatehiza'dan."),
    _k("iaido-kesagiri", "Kesagiri",
       "Seitei Iai kata 5 — rising and descending diagonal cuts.",
       "Seitei Iai kata 5 — yükselen ve inen çapraz kesişler."),
    _k("iaido-morote-tsuki", "Morote-tsuki",
       "Seitei Iai kata 6 — two-handed thrust between cuts.",
       "Seitei Iai kata 6 — kesişler arasında çift el saplama."),
    _k("iaido-sanpogiri", "Sanpōgiri",
       "Seitei Iai kata 7 — cutting three opponents in three directions.",
       "Seitei Iai kata 7 — üç yöndeki üç rakibe kesiş."),
    _k("iaido-ganmen-ate", "Ganmen-ate",
       "Seitei Iai kata 8 — strike to the face with the hilt, thrust behind.",
       "Seitei Iai kata 8 — kabzayla yüze vuruş, arkaya saplama."),
    _k("iaido-soete-tsuki", "Soete-tsuki",
       "Seitei Iai kata 9 — supported thrust with the hand on the blade.",
       "Seitei Iai kata 9 — el namlu üzerinde destekli saplama."),
    _k("iaido-shihogiri", "Shihōgiri",
       "Seitei Iai kata 10 — cutting four opponents in four directions.",
       "Seitei Iai kata 10 — dört yöndeki dört rakibe kesiş."),
    _k("iaido-sogiri", "Sōgiri",
       "Seitei Iai kata 11 — series of five complete cuts.",
       "Seitei Iai kata 11 — beş tam kesişten oluşan seri."),
    _k("iaido-nukiuchi", "Nukiuchi",
       "Seitei Iai kata 12 — sudden draw-and-cut; closes the set.",
       "Seitei Iai kata 12 — ani çekiş-kesiş; seti kapatır."),
]

# --- Aikido: temel teknikler ---
AIKIDO = [
    _k("aikido-ukemi", "Ukemi",
       "The art of falling safely — the first skill of aikido.",
       "Güvenli düşme sanatı — aikidonun ilk becerisi.", True),
    _k("aikido-ikkyo", "Ikkyo",
       "First principle — arm pin through the elbow.",
       "Birinci prensip — dirsek üzerinden kol sabitleme.", True),
    _k("aikido-nikyo", "Nikyo",
       "Second principle — wrist turn that takes the balance.",
       "İkinci prensip — dengeyi bozan bilek kilidi."),
    _k("aikido-sankyo", "Sankyo",
       "Third principle — spiral wrist control.",
       "Üçüncü prensip — spiral bilek kontrolü."),
    _k("aikido-yonkyo", "Yonkyo",
       "Fourth principle — pressure control on the forearm.",
       "Dördüncü prensip — ön kola baskı kontrolü."),
    _k("aikido-gokyo", "Gokyo",
       "Fifth principle — pin used against weapon attacks.",
       "Beşinci prensip — silahlı saldırılara karşı sabitleme."),
    _k("aikido-irimi-nage", "Irimi nage",
       "Entering throw — moving through the attack line.",
       "Girerek fırlatma — saldırı hattının içinden geçiş."),
    _k("aikido-shiho-nage", "Shiho nage",
       "Four-direction throw.",
       "Dört yön fırlatması."),
    _k("aikido-kote-gaeshi", "Kote gaeshi",
       "Outward wrist-turn throw.",
       "Bileği dışa çevirerek fırlatma."),
    _k("aikido-kaiten-nage", "Kaiten nage",
       "Rotary throw.",
       "Dairesel fırlatma."),
    _k("aikido-tenchi-nage", "Tenchi nage",
       "Heaven-and-earth throw — one hand high, one low.",
       "Gök-yer fırlatması — bir el yukarı, bir el aşağı."),
    _k("aikido-koshi-nage", "Koshi nage",
       "Hip throw.",
       "Kalça fırlatması."),
]

# --- Karate (Shotokan): temel kata seti ---
KARATE = [
    _k("karate-heian-shodan", "Heian Shodan",
       "First Shotokan kata — basic blocks and lunging punches.",
       "İlk Shotokan kataı — temel bloklar ve hamleli yumruklar.", True),
    _k("karate-heian-nidan", "Heian Nidan",
       "Second Heian kata — side kicks and double-hand techniques.",
       "İkinci Heian kataı — yan tekmeler ve çift el teknikleri."),
    _k("karate-heian-sandan", "Heian Sandan",
       "Third Heian kata — turning and close-range techniques.",
       "Üçüncü Heian kataı — dönüş ve yakın mesafe teknikleri."),
    _k("karate-heian-yondan", "Heian Yondan",
       "Fourth Heian kata — knee strikes and open-hand blocks.",
       "Dördüncü Heian kataı — diz vuruşları ve açık el blokları."),
    _k("karate-heian-godan", "Heian Godan",
       "Fifth Heian kata — jump and water-flow blocks.",
       "Beşinci Heian kataı — sıçrama ve akış blokları."),
    _k("karate-tekki-shodan", "Tekki Shodan",
       "First Tekki kata — performed entirely in horse stance, on one line.",
       "İlk Tekki kataı — tamamen at duruşunda, tek hat üzerinde."),
    _k("karate-bassai-dai", "Bassai Dai",
       "'To storm a fortress' — powerful hip-driven blocks and strikes.",
       "'Kaleyi yarma' — kalçadan güç alan bloklar ve vuruşlar."),
    _k("karate-kanku-dai", "Kanku Dai",
       "'Viewing the sky' — the longest of the core Shotokan kata.",
       "'Göğe bakış' — temel Shotokan katalarının en uzunu."),
    _k("karate-enpi", "Enpi",
       "'Flying swallow' — quick level changes and darting movement.",
       "'Uçan kırlangıç' — hızlı seviye değişimleri ve atak hareket."),
    _k("karate-jion", "Jion",
       "Temple-named kata — solid stances and classical techniques.",
       "Tapınak adını taşıyan kata — sağlam duruşlar, klasik teknikler."),
]

# --- Taekwondo (WT): Taegeuk 1–8 + Koryo + Keumgang ---
TKD_TAEGEUK = [
    ("il", 1, "Keon", "heaven", "gök"),
    ("i", 2, "Tae", "lake", "göl"),
    ("sam", 3, "Ri", "fire", "ateş"),
    ("sa", 4, "Jin", "thunder", "gök gürültüsü"),
    ("o", 5, "Seon", "wind", "rüzgâr"),
    ("yuk", 6, "Gam", "water", "su"),
    ("chil", 7, "Gan", "mountain", "dağ"),
    ("pal", 8, "Gon", "earth", "yer"),
]
TAEKWONDO = [
    _k(f"tkd-taegeuk-{num}", f"Taegeuk {name.capitalize()} Jang",
       f"Taegeuk poomsae {num} — represents {trigram} ({en_sym}).",
       f"Taegeuk poomsae {num} — {trigram} ({tr_sym}) öğesini temsil eder.",
       num == 1)
    for name, num, trigram, en_sym, tr_sym in TKD_TAEGEUK
] + [
    _k("tkd-koryo", "Koryo",
       "First black-belt poomsae — named after the Goryeo dynasty.",
       "İlk siyah kuşak poomsae'si — adını Goryeo hanedanından alır."),
    _k("tkd-keumgang", "Keumgang",
       "'Diamond' — slow, powerful black-belt poomsae.",
       "'Elmas' — yavaş ve güçlü siyah kuşak poomsae'si."),
]

CATALOG: dict[str, list[dict]] = {
    "aikijo": AIKIJO,
    "bokken": BOKKEN,
    "jodo": JODO,
    "jojutsu": JOJUTSU,
    "kenjutsu": KENJUTSU,
    "kendo": KENDO,
    "iaido": IAIDO,
    "aikido": AIKIDO,
    "karate": KARATE,
    "taekwondo": TAEKWONDO,
}

# Hafta temaları: (EN tema, TR tema, o haftanın odak suburi listesi)
WEEKS = [
    ("Tsuki fundamentals", "Tsuki temelleri",
     ["choku tsuki", "kaeshi tsuki", "ushiro tsuki"]),
    ("Uchikomi — striking week", "Uchikomi — vuruş haftası",
     ["shomen uchikomi", "renzoku uchikomi", "menuchi gedan gaeshi"]),
    ("Katate & hasso gaeshi", "Katate & hasso gaeshi",
     ["katate gedan gaeshi", "hasso gaeshi uchi", "hasso gaeshi tsuki"]),
    ("Flow — toward the 31 kata", "Akış — 31'lik kataya doğru",
     ["31-count kata (sections)", "free flow combinations", "full kata runs"]),
]


def _build_program_days() -> list[dict]:
    days = []
    for day_num in range(1, 31):
        week_idx = min((day_num - 1) // 7, 3)
        theme_en, theme_tr, focuses = WEEKS[week_idx]
        focus = focuses[(day_num - 1) % len(focuses)]
        if day_num % 7 == 0:
            title_en, title_tr = "Review & light flow", "Tekrar & hafif akış"
            content_en = (
                f"Week theme: {theme_en}. Today is a review day. 10 minutes of slow, "
                "deliberate repetition of everything from this week. Half speed, full attention. "
                "Finish with 5 minutes of free movement."
            )
            content_tr = (
                f"Hafta teması: {theme_tr}. Bugün tekrar günü. Bu haftanın tüm çalışmasını "
                "10 dakika yavaş ve bilinçli tekrar et. Yarı hız, tam dikkat. "
                "5 dakika serbest hareketle bitir."
            )
        else:
            title_en = f"Focus: {focus}"
            title_tr = f"Odak: {focus}"
            content_en = (
                f"Week theme: {theme_en}. Warm up 5 minutes (wrists, shoulders, hips). "
                f"Main work: {focus} — 3 sets of 20 repetitions, rest between sets. "
                "Last set slower than the first: precision over speed. "
                "Log your session when you're done."
            )
            content_tr = (
                f"Hafta teması: {theme_tr}. 5 dakika ısın (bilek, omuz, kalça). "
                f"Ana çalışma: {focus} — 3 set x 20 tekrar, setler arası dinlen. "
                "Son set ilkinden yavaş: hızdan önce isabet. "
                "Bitirince seansını kaydet."
            )
        days.append({
            "day_number": day_num,
            "title_en": title_en,
            "title_tr": title_tr,
            "content_en": content_en,
            "content_tr": content_tr,
        })
    return days


async def seed_content() -> None:
    async with async_session() as db:
        for discipline, items in CATALOG.items():
            for i, item in enumerate(items):
                values = {**item, "discipline": discipline, "sort_order": i}
                stmt = pg_insert(Kata).values(**values).on_conflict_do_update(
                    index_elements=["slug"],
                    set_={k: v for k, v in values.items() if k != "slug"},
                )
                await db.execute(stmt)

        program_count = (await db.execute(select(func.count(Program.id)))).scalar_one()
        if program_count == 0:
            program = Program(
                slug="30-day-jo-suburi",
                title_en="30-Day Jo Suburi Program",
                title_tr="30 Günlük Jo Suburi Programı",
                description_en=(
                    "One month of daily, structured jo suburi practice. "
                    "Four weekly themes: thrusts, strikes, turning forms, and flow. "
                    "15–25 minutes a day."
                ),
                description_tr=(
                    "Bir ay boyunca her gün yapılandırılmış jo suburi çalışması. "
                    "Dört haftalık tema: saplamalar, vuruşlar, dönüş formları ve akış. "
                    "Günde 15–25 dakika."
                ),
                duration_days=30,
            )
            db.add(program)
            await db.flush()
            for day in _build_program_days():
                db.add(ProgramDay(program_id=program.id, **day))

        await db.commit()
