"""İçerik kataloğu: branş bazlı kata/teknik kütüphanesi + 30 günlük program.

Kata kataloğu her açılışta slug üzerinden upsert edilir (idempotent) —
başlık/açıklama/branş/kind düzeltmeleri deploy ile yayılır. Video URL'leri
sahibin çekimleri veya bulunan uygun YouTube videoları hazır olana dek boş
(/admin/katas ekranından eklenir).

`kind`: "kata" (form/poomsae/kihon dizisi) veya "teknik" (tek hareket/vuruş).
/kata sayfasında branş seçilince bu iki tür ayrı sekmelerde listelenir.

Kaynaklar: ZNKR Seitei Jōdō ve Seitei Iai müfredatı, Nihon Kendō Kata,
Shintō Musō-ryū kihon seti, Saito yöntemi aiki-jo 20 suburi / aiki-ken
nana suburi, Shotokan kata/kihon, WT Taegeuk poomsae listeleri.
Kesin olmayan içerik (adım adım dökümler) buraya YAZILMAZ — TODO.md'deki
"Rehber araştırma listesi"nde tutulur.
"""

from sqlalchemy import func, select
from sqlalchemy.dialects.postgresql import insert as pg_insert

from app.db import async_session
from app.models import Kata, Program, ProgramDay


def _k(slug: str, title: str, en: str, tr: str, free: bool = False, kind: str = "kata") -> dict:
    return {"slug": slug, "title_en": title, "title_tr": title,
            "description_en": en, "description_tr": tr, "is_free": free, "kind": kind}


# --- Aiki-jo: kata + Saito yöntemi 20 suburi (teknik) ---
AIKIJO = [
    # Kata
    _k("sanjuichi-no-jo", "31 no jo kata",
       "The 31-count solo kata — the backbone of aiki-jo practice.",
       "31 sayılık solo kata — aiki-jo çalışmasının omurgası.", True),
    _k("jusan-no-jo", "13 no jo kata",
       "The 13-count solo kata; compact and rhythm-focused.",
       "13 sayılık solo kata; kompakt ve ritim odaklı.", True),
    _k("aikijo-happo-giri", "Happo giri",
       "Cutting to eight directions in sequence — the best warm-up for footwork and balance.",
       "8 yöne kesiş çalışması: kuzeyden başlayıp saat yönünde 8 yöne sırayla men uchi. "
       "Ayak çalışması ve denge için en iyi ısınma.", True),
    # Teknik — Tsuki serisi (suburi 1-5)
    _k("choku-tsuki", "Choku tsuki",
       "Straight thrust; rear hand drives, front hand aims. Target chudan.",
       "Düz dürtüş. Arka el itiş gücünü verir, ön el yönlendirir; jo koltuk altından değil "
       "göbek hizasından çıkar. Hedef: boğaz/göğüs (chudan).", True, "teknik"),
    _k("kaeshi-tsuki", "Kaeshi tsuki",
       "Turning thrust: the tip deflects, then thrusts. Drill the hand change slowly.",
       "Çevirmeli dürtüş: jo'nun ucu savuşturur gibi döner, ardından dürtüş gelir. "
       "El değişimini yavaş çalış, hızlanınca kendiliğinden oturur.", kind="teknik"),
    _k("ushiro-tsuki", "Ushiro tsuki",
       "Rear thrust — look first, then rotate the hips.",
       "Arkaya dürtüş. Önce başını çevirip bak, sonra kalçayı döndürerek dürt.", kind="teknik"),
    _k("tsuki-gedan-gaeshi", "Tsuki gedan gaeshi",
       "Thrust then low sweep at knee height; power from the torso, not the arms.",
       "Dürtüş + alçak süpürme: jo'nun arka ucu diz/ayak bileği seviyesine döner. "
       "Dizlerini kır, süpürmeyi kolla değil gövdeyle yap.", kind="teknik"),
    _k("tsuki-jodan-gaeshi", "Tsuki jodan gaeshi uchi",
       "Thrust, high turn, overhead strike — practise in three parts.",
       "Dürtüş + yukarı çevirip tepeden vuruş. Üç parçaya bölüp (tsuki / çevirme / uchi) "
       "ayrı ayrı çalış.", kind="teknik"),
    # Teknik — Uchikomi serisi (suburi 6-10)
    _k("shomen-uchikomi", "Shomen uchikomi",
       "Overhead centre strike; finish with the tip at eye level.",
       "Tepeden merkez vuruş. Jo başın üstünde tam açılır, bitişte uç göz hizasında durur.",
       True, "teknik"),
    _k("renzoku-uchikomi", "Renzoku uchikomi",
       "Continuous alternating strikes — a rhythm drill.",
       "Ardışık vuruş: sol-sağ el değişimiyle kesintisiz shomen. Ritim çalışmasıdır — "
       "metronom gibi 20 tekrar.", kind="teknik"),
    _k("menuchi-gedan-gaeshi", "Men uchi gedan gaeshi",
       "Head strike flowing into a low sweep on the same step.",
       "Baş vuruşu + alçak karşılık. Vuruştan sonra geri çekilme yok; aynı adımda alçak "
       "süpürme gelir.", kind="teknik"),
    _k("menuchi-ushiro-tsuki", "Men uchi ushiro tsuki",
       "Head strike forward, thrust to the rear — two-opponent assumption.",
       "Baş vuruşu + arkaya dürtüş: önde ve arkada iki hasım varsayımı. Omuz üzerinden "
       "bakışı unutma.", kind="teknik"),
    _k("gyaku-yokomen-ushiro-tsuki", "Gyaku yokomen ushiro tsuki",
       "Reverse side strike to the temple, then rear thrust.",
       "Ters yandan şakak vuruşu + arkaya dürtüş. Bileğin esnekliğini test eder; ağır ve "
       "geniş başla.", kind="teknik"),
    # Teknik — Katate serisi (suburi 11-13)
    _k("katate-gedan-gaeshi", "Katate gedan gaeshi",
       "One-handed low sweep; mind the wrist load.",
       "Tek elle alçak süpürme; jo'nun ağırlığını tek bilek taşır. Bilek ağrırsa tempoyu "
       "düşür, sayıyı artırma.", kind="teknik"),
    _k("katate-toma-uchi", "Katate toma uchi",
       "One-handed long-range strike from the very end of the jo.",
       "Tek elle uzun menzil vuruşu: jo'nun en ucundan tutulur, menzil maksimuma çıkar. "
       "Aiki-jo'nun imza hareketi.", kind="teknik"),
    _k("katate-hachi-no-ji", "Katate hachi no ji gaeshi",
       "One-handed figure-eight — the basis of jo spinning.",
       "Tek elle 8 çizme: jo önde yatay 8 (∞) çizer. Bilek gevşek, dirsek sabit; jo spin "
       "çalışmasının temelidir.", kind="teknik"),
    # Teknik — Hasso gaeshi serisi (suburi 14-18)
    _k("hasso-gaeshi-uchi", "Hasso gaeshi uchi",
       "Turn the jo up to hasso at the shoulder, strike from there.",
       "Jo dikeyde omuz hizasına döner (hasso), oradan vuruş. Dönüş sırasında jo yüzüne "
       "çarpmasın diye dirsekleri açık tut.", kind="teknik"),
    _k("hasso-gaeshi-tsuki", "Hasso gaeshi tsuki",
       "Thrust from hasso.", "Hasso'dan dürtüş.", kind="teknik"),
    _k("hasso-gaeshi-ushiro-tsuki", "Hasso gaeshi ushiro tsuki",
       "Rear thrust from hasso.", "Hasso'dan arkaya dürtüş.", kind="teknik"),
    _k("hasso-gaeshi-ushiro-uchi", "Hasso gaeshi ushiro uchi",
       "Rear strike from hasso.", "Hasso'dan arkaya vuruş.", kind="teknik"),
    _k("hasso-gaeshi-ushiro-barai", "Hasso gaeshi ushiro barai",
       "Rear sweep from hasso — impossible without hip rotation.",
       "Hasso'dan arkaya süpürme — serinin en tekniklisi; kalça dönüşü olmadan yapılamaz.",
       kind="teknik"),
    # Teknik — Nagare gaeshi (suburi 19-20)
    _k("hidari-nagare-gaeshi-uchi", "Hidari nagare gaeshi uchi",
       "Flowing left deflection merging into a strike.",
       "Sola akan çevirme + vuruş: savuşturma ve karşılık tek harekette erir. 31'li "
       "katanın 5. bölümünün temelidir.", kind="teknik"),
    _k("migi-nagare-gaeshi-tsuki", "Migi nagare gaeshi tsuki",
       "Flowing right deflection into a thrust; chains into freestyle work.",
       "Sağa akan çevirme + dürtüş. İki nagare'yi art arda bağlayıp 'akış turu' olarak "
       "çalışmak jo freestyle'ın kapısını açar.", kind="teknik"),
]

# --- Aiki-ken (bokken): kata + nana suburi & kamae (teknik) ---
BOKKEN = [
    # Kata
    _k("bokken-happo-giri", "Happo giri",
       "Shomen cuts to eight directions; feet turn first, sword follows.",
       "8 yöne shomen kesişi. Her dönüşte ayaklar önce, kılıç sonra; kesişler aynı "
       "yükseklikte bitmeli.", True),
    _k("bokken-kumitachi", "Kumitachi 1-5 (solo hali)",
       "The five paired sword forms; practise the attacking side solo as shadow work, "
       "keeping the pauses.",
       "Beş eşli kılıç formu. Partner yokken her formun uchitachi (saldıran) tarafını "
       "gölge olarak çalış: mesafeyi zihninde kur, duraklamaları koru."),
    # Teknik — 7 suburi
    _k("bokken-shomen-suburi", "Aiki-ken suburi 1 — Ichi no suburi",
       "Full overhead cut finishing at belly height; body drops with the cut.",
       "Tam shomen kesişi: kılıç başın üstünde tam açılır, kesiş göbek hizasında biter. "
       "Diz-kalça-omuz aynı anda düşer; kol gücüyle kesme.", True, "teknik"),
    _k("aiki-ken-suburi-2", "Aiki-ken suburi 2 — Ni no suburi",
       "Step back to jodan, step in and cut.",
       "Geri adımla savunma pozisyonundan öne adımla kesiş. Geri çekilirken kılıç "
       "jodan'a kalkar.", kind="teknik"),
    _k("aiki-ken-suburi-3", "Aiki-ken suburi 3 — San no suburi",
       "Low sweep then overhead cut.",
       "Alt savuşturma (gedan) sonrası kesiş: kılıç önce aşağı süpürür, sonra tepeden "
       "iner.", kind="teknik"),
    _k("aiki-ken-suburi-4", "Aiki-ken suburi 4 — Yon no suburi",
       "Walking continuous shomen cuts, one per step.",
       "Ardışık kesiş yürüyüşü: her adımda bir shomen, dojo boyunca. Nefesle eşle: "
       "adım-kes-nefes.", kind="teknik"),
    _k("aiki-ken-suburi-5", "Aiki-ken suburi 5 — Go no suburi",
       "Side deflection returning to a centre cut.",
       "Yan savuşturma + kesiş: kılıç yana açılıp merkeze döner. Bileklerin çizdiği yay "
       "küçük olmalı.", kind="teknik"),
    _k("aiki-ken-suburi-6", "Aiki-ken suburi 6 — Roku no suburi",
       "Deflection finishing with a thrust.",
       "Savuşturma + tsuki: kesiş yerine dürtüşle biter. Tsuki'de arka ayak topuğu "
       "yerden kalkmaz.", kind="teknik"),
    _k("aiki-ken-suburi-7", "Aiki-ken suburi 7 — Nana no suburi",
       "Combines deflection, cut and thrust — the series in one flow.",
       "Serinin birleşimi: savuşturma, kesiş ve tsuki tek akışta. Yedisi art arda = tam "
       "bir mini kata.", kind="teknik"),
    # Teknik — Kamae
    _k("bokken-kamae-seigan", "Seigan / Chudan no kamae",
       "The basic guard — tip at the opponent's throat.",
       "Temel duruş: kılıcın ucu rakibin boğazına. Bütün suburi buradan başlar, buraya "
       "döner.", kind="teknik"),
    _k("bokken-kamae-jodan", "Jodan no kamae",
       "Sword overhead, ready to strike.",
       "Kılıç başın üstünde, saldırıya hazır. Dirsekler kulakları kapatmaz; koltuk altı "
       "açık.", kind="teknik"),
    _k("bokken-kamae-hasso", "Hasso no kamae",
       "Vertical sword at the shoulder — an observing posture.",
       "Kılıç dik, tsuba omuz hizasında. Bekleme ve gözlem duruşu.", kind="teknik"),
    _k("bokken-kamae-waki", "Waki gamae",
       "Sword hidden behind — striking 'from nowhere'.",
       "Kılıç arkada gizli, uzunluğu göstermez. Kesişi 'yoktan' başlatma çalışması.",
       kind="teknik"),
    _k("bokken-kamae-gedan", "Gedan no kamae",
       "Tip low — an inviting guard from which rising deflections grow.",
       "Uç aşağıda, davet duruşu. Buradan yukarı savuşturma (suriage) doğar.",
       kind="teknik"),
]

# --- ZNKR Seitei Jōdō: 12 kata + 12 kihon (teknik) ---
JODO = [
    # Kata
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
    # Teknik — 12 kihon
    _k("jodo-kihon-honte-uchi", "Honte uchi",
       "Basic strike with the standard grip.",
       "Normal tutuşla temel vuruş — jodonun shomen'i. Bitişte jo'nun ucu rakibin "
       "şakağını gösterir.", True, "teknik"),
    _k("jodo-kihon-gyakute-uchi", "Gyakute uchi",
       "Strike with the reversed grip — both ends are weapons.",
       "Ters tutuşla vuruş; jo'nun iki ucu da silahtır fikrini öğretir.", kind="teknik"),
    _k("jodo-kihon-hikiotoshi-uchi", "Hiki otoshi uchi",
       "The signature technique: sliding strike that drops the sword.",
       "Kılıcı aşağı düşüren vuruş: jo kılıcın yan yüzüne kayarak iner. Jodonun imza "
       "tekniği.", kind="teknik"),
    _k("jodo-kihon-kaeshi-tsuki", "Kaeshi tsuki",
       "Turning thrust to the throat.",
       "Çevirmeli dürtüş: savuşturmadan dönerek boğaza.", kind="teknik"),
    _k("jodo-kihon-gyakute-tsuki", "Gyakute tsuki",
       "Reversed-grip thrust.", "Ters tutuşla dürtüş.", kind="teknik"),
    _k("jodo-kihon-maki-otoshi", "Maki otoshi",
       "Spiral wrap that drops the sword — angle over speed.",
       "Kılıcı sarıp düşürme: jo kılıca spiral sarılır. Yavaş çalış; hız değil açı iş "
       "yapar.", kind="teknik"),
    _k("jodo-kihon-kuritsuke", "Kuri tsuke",
       "Pinning sword and hands downward.",
       "Kılıcı ve elleri yere doğru kilitleme.", kind="teknik"),
    _k("jodo-kihon-kurihanashi", "Kuri hanashi",
       "Pinning then casting away.",
       "Kilitleyip fırlatma: kuri tsuke'nin devamı.", kind="teknik"),
    _k("jodo-kihon-taiatari", "Tai atari",
       "Body check through the jo.",
       "Beden çarpması: jo üzerinden gövdeyle itiş.", kind="teknik"),
    _k("jodo-kihon-tsukihazushi", "Tsuki hazushi uchi",
       "Evading a thrust into a strike.",
       "Dürtüşü savuşturup vuruş.", kind="teknik"),
    _k("jodo-kihon-dobarai", "Dou barai uchi",
       "Parrying a torso cut into a strike.",
       "Gövde süpürmesini savuşturup vuruş.", kind="teknik"),
    _k("jodo-kihon-taihazushi", "Tai hazushi uchi",
       "Off-line evasion merging into a strike.",
       "Bedeni hattan çıkarıp vuruş: sabaki + uchi tek harekette.", kind="teknik"),
]


# --- Kenjutsu: okul kataları hakkında (kata, bilgilendirici) + temel kesişler/kamae (teknik) ---
KENJUTSU = [
    _k("ken-okul-katalari", "Okul kataları hakkında",
       "Kenjutsu kata are school-specific; without a school, invest in cut quality or "
       "use the standardised Iaido/Kendo kata.",
       "Kenjutsu kataları okula özgüdür (ör. Katori Shinto-ryu'nun Omote no Tachi'si). "
       "Okula bağlı değilsen kata taklidi yerine kesiş kalitesine yatırım yap; Iaido "
       "veya Kendo kataları standartlaştırılmış alternatiflerdir.", True),
    _k("ken-shomen-giri", "Shomen giri",
       "Vertical centre cut braked by the core, not the wrists.",
       "Dikey merkez kesiş: tepeden başlar, chudan'da durur. Kesişin freni bilek değil "
       "karın kasıdır.", True, "teknik"),
    _k("ken-kesa-giri", "Kesa giri",
       "Diagonal cut along the monk's-robe line, both sides equally.",
       "Omuzdan çapraza (keşiş cübbesi hattı) kesiş. Sağ ve sol kesa'yı eşit çalış — "
       "herkesin zayıf tarafı vardır.", kind="teknik"),
    _k("ken-gyaku-kesa", "Gyaku kesa giri",
       "Rising reverse diagonal cut.",
       "Aşağıdan yukarı ters çapraz kesiş.", kind="teknik"),
    _k("ken-do-giri", "Do giri (yoko ichimonji)",
       "Horizontal torso cut driven by the hips.",
       "Yatay gövde kesişi; kalça dönüşüyle atılır.", kind="teknik"),
    _k("ken-tsuki", "Tsuki",
       "Thrust to the throat — line over power.",
       "Boğaza dürtüş; kesişten daha az kuvvet, daha çok hat ister.", kind="teknik"),
    _k("ken-kamae", "Beş kamae",
       "The five guards (see Bokken); names and angles vary by school.",
       "Chudan, jodan, gedan, hasso, waki — açıklamalar Bokken bölümünde; kenjutsu'da "
       "okullara göre isim ve açı değişir.", kind="teknik"),
    _k("ken-suburi-rutini", "Suburi rutini",
       "30 vertical, 20+20 diagonal, 10+10 horizontal, 20 thrusts; check form in a "
       "mirror weekly.",
       "Kiri oroshi 30, kesa giri 20+20, do giri 10+10, tsuki 20. Ayna karşısında "
       "haftada bir form kontrolü yap.", kind="teknik"),
]

# --- Kendo: Nihon Kendō Kata (kata) + vuruşlar/suburi/ayak çalışması (teknik) ---
KENDO = [
    _k(f"kendo-kata-{i}", f"Nihon Kendō Kata {i} ({name})",
       f"Kendō kata {i} — tachi (long sword) form, uchidachi vs shidachi.",
       f"Kendō kata {i} — tachi (uzun kılıç) formu, uchidachi–shidachi.", i == 1)
    for i, name in [(1, "Ipponme"), (2, "Nihonme"), (3, "Sanbonme"),
                    (4, "Yonhonme"), (5, "Gohonme"), (6, "Ropponme"), (7, "Nanahonme")]
] + [
    _k(f"kendo-kodachi-{i}", f"Kodachi Kata {i}",
       f"Kendō kodachi kata {i} — short sword against long sword.",
       f"Kendō kodachi kata {i} — uzun kılıca karşı kısa kılıç.")
    for i in (1, 2, 3)
] + [
    # Teknik — 4 datotsu
    _k("kendo-men", "Men uchi",
       "Strike to the head — the first of kendo's four target strikes.",
       "Kafaya vuruş — kendonun dört hedef vuruşunun ilki.", True, "teknik"),
    _k("kendo-kote", "Kote uchi",
       "Strike to the wrist.", "Bileğe vuruş.", kind="teknik"),
    _k("kendo-do", "Do uchi",
       "Strike to the trunk.", "Gövdeye vuruş.", kind="teknik"),
    _k("kendo-tsuki", "Tsuki",
       "Thrust to the throat guard.", "Boğaz korumasına saplama.", kind="teknik"),
    # Teknik — suburi
    _k("kendo-joge-buri", "Joge buri",
       "Large full swings opening the shoulders.",
       "Büyük tam kesiş: kılıç kuyruk sokumuna değecek kadar geri, öne tam uzanım. "
       "Omuz açma egzersizi.", kind="teknik"),
    _k("kendo-shomen-suburi", "Shomen suburi",
       "Centre cuts finishing at men height.",
       "Men hizasında biten merkez kesiş; kendonun ekmek teknesi. Sayarak, nefesle: 30 "
       "tekrar.", kind="teknik"),
    _k("kendo-sayu-men", "Sayu men",
       "Alternating diagonal men cuts.",
       "Sağ-sol çapraz men kesişleri; 45° hat.", kind="teknik"),
    _k("kendo-haya-suburi", "Haya suburi",
       "Jumping fast suburi — the conditioning benchmark.",
       "Sıçramalı hızlı suburi: ileri-geri okuri ashi ile kesintisiz shomen. Kondisyonun "
       "ölçüsü — 20'den başla, 50'ye çık.", kind="teknik"),
    # Teknik — ashi sabaki + kirikaeshi
    _k("kendo-okuri-ashi", "Okuri ashi",
       "The sliding step underlying all kendo movement.",
       "Kayan adım: ön ayak gider, arka ayak takip eder, topuklar hafif havada.",
       kind="teknik"),
    _k("kendo-fumikomi", "Fumikomi",
       "The stamping step at the moment of the strike.",
       "Vuruş anındaki sert basış; ayak tabanı düz iner. Yumuşak zeminde çalış, eklem "
       "koru.", kind="teknik"),
    _k("kendo-kirikaeshi", "Kirikaeshi (solo)",
       "Shomen + nine alternating men + shomen; solo it is a breath-and-rhythm drill.",
       "Shomen + 9 sayu men + shomen dizisi. Partner/makiwara yoksa havaya, mesafeyi "
       "hayal ederek — nefes ve ritim çalışmasıdır.", kind="teknik"),
]

# --- ZNKR Seitei Iai: 12 kata + dört faz / destek çalışmaları (teknik) ---
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
    # Teknik — dört faz
    _k("iaido-nukitsuke", "Nukitsuke",
       "The draw that cuts; half the speed is the scabbard pulling back.",
       "Çekişle kesiş: kılıç kılıftan çıkarken kesmeye başlar; saya biki (kılıfın geri "
       "çekilmesi) hızın yarısıdır.", True, "teknik"),
    _k("iaido-kirioroshi", "Kirioroshi",
       "The main descending cut.",
       "Esas kesiş: tam yukarı açılım, merkezden aşağı. Bokken suburi'siyle aynı "
       "mekanik.", kind="teknik"),
    _k("iaido-chiburi", "Chiburi",
       "Shaking the blood off — a zanshin phase, never rushed.",
       "Kanı silkme: büyük dairesel (o-chiburi) veya yana küçük (yoko chiburi). Acele "
       "edilmez — zanshin fazıdır.", kind="teknik"),
    _k("iaido-noto", "Noto",
       "Re-sheathing without looking; slow noto is the hard one.",
       "Kılıfa koyuş: gözler rakipte, el kılıfın ağzını bulur. Yavaş noto, hızlı "
       "noto'dan zordur ve daha değerlidir.", kind="teknik"),
    _k("iaido-seiza-kalkis", "Seiza / tate hiza kalkışları",
       "Rising from seiza in one motion, 10 reps daily.",
       "Diz üstünden tek harekette kalkış; günde 10 tekrar dizleri katalara "
       "hazırlar.", kind="teknik"),
    _k("iaido-bokken-suburi", "Suburi (bokken)",
       "Cut mechanics with a bokken when no iaito is available.",
       "Iaito yoksa kirioroshi'yi bokken ile çalış: 30 merkez, 20 kesa.", kind="teknik"),
]

# --- Aikido: klasik solo kata yok — tai sabaki, ukemi, saldırılar, prensipler (teknik) ---
AIKIDO = [
    # Teknik — tai sabaki
    _k("aikido-irimi", "Irimi",
       "Entering straight past the line of attack.",
       "Girme: saldırı hattının içine, rakibin arkasına doğru tek düz adım. Solo "
       "çalışmada bir duvar köşesini rakip say, hattın dışına gir.", True, "teknik"),
    _k("aikido-tenkan", "Tenkan",
       "Pivot 180° around the front foot.",
       "Dönme: ön ayak sabit, arka ayak 180° süpürür. Günde 20 tekrar — dönüş sonunda "
       "omuzlar ve kalça aynı yöne bakmalı.", kind="teknik"),
    _k("aikido-irimi-tenkan", "Irimi-tenkan",
       "Enter then pivot — aikido's fundamental 'walk'.",
       "İkisinin birleşimi: gir + dön. Aikidonun 'yürüyüşü' budur; müzikle ritmik "
       "çalışmak dengeyi hızla geliştirir.", kind="teknik"),
    _k("aikido-shikko", "Shikko",
       "Knee walking — the base of seated techniques.",
       "Diz üstü yürüyüş. Suwariwaza'nın temeli; 2×dojo boyu gidiş-dönüş dizleri ve "
       "kalça hareketini açar.", kind="teknik"),
    # Teknik — ukemi
    _k("aikido-mae-ukemi", "Mae ukemi (öne yuvarlanma)",
       "Forward roll along the arm and across the back.",
       "Öne yuvarlanma: kol yay olur, temas noktası el kenarından omuza, çapraz sırt "
       "üzerinden kalk. Yumuşak zeminde günde 10 tekrar.", True, "teknik"),
    _k("aikido-ushiro-ukemi", "Ushiro ukemi (geriye)",
       "Backward roll — progress from sitting to standing.",
       "Geriye yuvarlanma: çene göğüste, sırt yuvarlak. Önce oturuştan, sonra "
       "çömelmeden, en son ayakta başlayarak ilerle.", kind="teknik"),
    _k("aikido-yoko-ukemi", "Yoko ukemi (yana)",
       "Side breakfall — arm and leg strike together.",
       "Yana düşüş: kol ve bacak aynı anda yere vurur, baş asla değmez.", kind="teknik"),
    # Teknik — temel el saldırıları
    _k("aikido-shomen-uchi", "Shomen uchi",
       "Overhead strike with the hand blade; same mechanics as a sword cut.",
       "Tepeden el kılıcıyla (tegatana) merkez vuruş. Kılıç kesişiyle aynı mekanik — "
       "bokken suburi'si bunu doğrudan besler.", kind="teknik"),
    _k("aikido-yokomen-uchi", "Yokomen uchi",
       "Diagonal strike to the temple.",
       "Şakağa diyagonal vuruş. Omuzdan değil kalçadan başlar.", kind="teknik"),
    _k("aikido-tsuki", "Tsuki",
       "Straight punch to the abdomen, stepping in.",
       "Karına düz yumruk. Aikido tsuki'si adımla birlikte gelir; yerinde yumruk atma.",
       kind="teknik"),
    # Teknik — prensipler / atışlar
    _k("aikido-ikkyo", "Ikkyo",
       "First principle — arm pin through the elbow.",
       "Birinci prensip: dirsek kontrolü. Solo: ikkyo undo — kollar merkezden yukarı "
       "yay çizer, 20 tekrar.", kind="teknik"),
    _k("aikido-nikyo", "Nikyo",
       "Second principle — wrist turn that takes the balance.",
       "İkinci prensip — dengeyi bozan bilek kilidi.", kind="teknik"),
    _k("aikido-sankyo", "Sankyo",
       "Third principle — spiral wrist control.",
       "Üçüncü prensip — spiral bilek kontrolü.", kind="teknik"),
    _k("aikido-yonkyo", "Yonkyo",
       "Fourth principle — pressure control on the forearm.",
       "Dördüncü prensip — ön kola baskı kontrolü.", kind="teknik"),
    _k("aikido-gokyo", "Gokyo",
       "Fifth principle — pin used against weapon attacks.",
       "Beşinci prensip — silahlı saldırılara karşı sabitleme.", kind="teknik"),
    _k("aikido-shiho-nage", "Shiho nage",
       "Four-direction throw; drill the footwork with a bokken.",
       "Dört yön fırlatması: kılıç kesişinin atışa dönmüş hali. Solo: bokken ile 4 "
       "yöne kesiş yaparak ayak düzenini otur.", kind="teknik"),
    _k("aikido-irimi-nage", "Irimi nage",
       "Entering throw — moving through the attack line.",
       "Girerek fırlatma — saldırı hattının içinden geçiş.", kind="teknik"),
    _k("aikido-kote-gaeshi", "Kote gaeshi",
       "Outward wrist-turn throw; the tai sabaki patterns are 80% of the throw.",
       "Bileği dışa çevirerek fırlatma. Eşsiz çalışılamaz ama tai sabaki kalıpları "
       "(tenkan + kesiş) atışın %80'idir.", kind="teknik"),
    _k("aikido-kaiten-nage", "Kaiten nage",
       "Rotary throw.", "Dairesel fırlatma.", kind="teknik"),
    _k("aikido-tenchi-nage", "Tenchi nage",
       "Heaven-and-earth throw — one hand high, one low.",
       "Gök-yer fırlatması — bir el yukarı, bir el aşağı.", kind="teknik"),
    _k("aikido-koshi-nage", "Koshi nage",
       "Hip throw.", "Kalça fırlatması.", kind="teknik"),
    _k("aikido-kokyu-nage", "Kokyu nage",
       "Breath throw — off-balance and cast without a joint lock; the umbrella term for "
       "a whole family of throws with no single fixed form.",
       "Nefes fırlatması: eklem kilidi olmadan dengeyi bozup savurma. Tek bir sabit "
       "formu yoktur — bir çok atışın şemsiye adıdır.", kind="teknik"),
    _k("aikido-kokyu-ho", "Kokyu-ho (kokyu dosa)",
       "Seated power-extension exercise: unbalance a two-hand grip using the centre, "
       "not arm strength — distinct from the kokyu-nage throw.",
       "Oturarak güç açma egzersizi: suwariwaza'da iki elden tutuşu kol gücüyle değil "
       "merkezden dengeyi bozarak çöz. Kokyu-nage atışından farklıdır — bu bir egzersizdir.",
       kind="teknik"),
    _k("aikido-juji-nage", "Juji nage (juji garami)",
       "Cross-arm throw — the arms are locked into an X shape before the throw.",
       "Çapraz kol fırlatması: atmadan önce kollar X şeklinde kilitlenir; juji-garami "
       "olarak da bilinir.", kind="teknik"),
    _k("aikido-sumi-otoshi", "Sumi otoshi",
       "Corner drop — off-balance straight back into the rear corner; deceptively "
       "simple, easy to muscle instead of blend.",
       "Köşe düşürmesi: rakibi arka köşesine doğru dengeyi bozarak düşür. Basit "
       "görünür ama kaba kuvvetle yapılırsa yozlaşır — kalça değil dengeyle çalış.",
       kind="teknik"),
]

# --- Karate (Shotokan): kata + duruş/yumruk/blok/tekme (teknik) ---
KARATE = [
    # Kata
    _k("karate-taikyoku-shodan", "Taikyoku Shodan",
       "First kata: only gedan barai and oi tsuki on an H-shaped embusen, 20 moves. "
       "The cleanest way to learn turns.",
       "İlk kata: yalnız gedan barai + oi tsuki, H şeklinde embusen (zemin deseni) "
       "üzerinde 20 hareket. Dönüşleri öğrenmenin en temiz yolu.", True),
    _k("karate-heian-shodan", "Heian Shodan",
       "21 moves adding age uke, shuto uke and kokutsu dachi.",
       "21 hareket: gedan barai, age uke, oi tsuki, shuto uke ve kokutsu dachi "
       "tanıtılır. Taikyoku'nun üstüne yalnızca birkaç yeni teknik koyar.", True),
    _k("karate-heian-nidan", "Heian Nidan",
       "26 moves introducing side kick + backfist and nukite.",
       "26 hareket: haiwan uke, yoko geri + uraken kombinasyonu, mae geri ve nukite. "
       "Yan tekme dengesi bu katada kurulur."),
    _k("karate-heian-sandan", "Heian Sandan",
       "20 moves: paired uchi uke, elbows in kiba dachi.",
       "20 hareket: uchi uke çiftleri, kiba dachi'de dirsekler ve meşhur yavaş dönüşlü "
       "fumikomi bölümü."),
    _k("karate-heian-yondan", "Heian Yondan",
       "27 moves — the most athletic of the series.",
       "27 hareket: kakiwake uke, mae geri-uraken hızlı kombinasyonu, hiza geri (diz). "
       "Serinin en atletik katası."),
    _k("karate-heian-godan", "Heian Godan",
       "23 moves with the jump — the series finale.",
       "23 hareket: mizu nagare kamae, sıçrama (tobi) ve zemin geçişi. Heian serisinin "
       "finali."),
    _k("karate-tekki-shodan", "Tekki Shodan",
       "29 moves entirely in horse stance on a single line — ideal for small spaces.",
       "29 hareket, tamamı kiba dachi'de ve tek çizgi üzerinde (I embusen). Kalça gücü "
       "ve alt beden dayanıklılığı katası; dar alanda bile çalışılır."),
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
    _k("karate-jitte", "Jitte",
       "'Ten hands' — defence-oriented kata built around blocking a staff (bo) attack.",
       "'On el' — bir sopa (bo) saldırısına karşı savunmayı esas alan blok ağırlıklı kata."),
    _k("karate-bassai-sho", "Bassai Sho",
       "Companion to Bassai Dai — same 'storming a fortress' theme, lighter and faster.",
       "Bassai Dai'nin eşi — aynı 'kaleyi yarma' teması, daha hafif ve hızlı."),
    _k("karate-gankaku", "Gankaku",
       "'Crane on a rock' — one-legged stances testing balance, formerly known as Chinto.",
       "'Kayadaki turna' — dengeyi sınayan tek ayak duruşları; eski adı Chinto."),
    _k("karate-hangetsu", "Hangetsu",
       "'Half moon' — slow breathing kata in a deep hangetsu-dachi, tension over speed.",
       "'Yarım ay' — derin hangetsu-dachi'de yavaş nefesli kata; hız yerine gerilim."),
    # Teknik — dachi
    _k("karate-zenkutsu-dachi", "Zenkutsu dachi",
       "Front stance, 60% weight forward.",
       "Öne eğilimli duruş: ön diz bükük (dizden ayak ucu görünmez), arka bacak "
       "gergin, kalça öne dönük. Ağırlık %60 önde.", True, "teknik"),
    _k("karate-kokutsu-dachi", "Kokutsu dachi",
       "Back stance, 70% rear — home of shuto uke.",
       "Geriye eğilimli duruş: ağırlık %70 arkada, ayaklar L şeklinde. Shuto uke'nin "
       "evi.", kind="teknik"),
    _k("karate-kiba-dachi", "Kiba dachi",
       "Horse stance; hold one minute as a first goal.",
       "Binici duruşu: ayaklar paralel, iki omuz genişliği, dizler dışa. 1 dk sabit "
       "durabilmek ilk hedef.", kind="teknik"),
    # Teknik — tsuki/uchi
    _k("karate-choku-tsuki", "Choku tsuki",
       "Straight punch; power comes from the retracting hand.",
       "Düz yumruk: yumruk kalçadan döner (hikite), son çeyrekte pronasyon. Karşı el "
       "kalçaya aynı hızla çekilir — güç oradadır.", kind="teknik"),
    _k("karate-oi-tsuki", "Oi tsuki",
       "Stepping punch — foot and fist finish together.",
       "Adımlı yumruk: adımın ayak basışıyla yumruk aynı anda biter (kime).",
       kind="teknik"),
    _k("karate-gyaku-tsuki", "Gyaku tsuki",
       "Reverse punch driven by hip rotation.",
       "Ters yumruk: ön bacak sabit, arka kalça döner. Karatenin en çok puan getiren "
       "tekniği.", kind="teknik"),
    _k("karate-uraken-uchi", "Uraken uchi",
       "Backfist snap from the elbow.",
       "Ters yumruk sırtıyla kamçı vuruş; dirsek menteşe gibi.", kind="teknik"),
    _k("karate-shuto-uchi", "Shuto uchi",
       "Knife-hand strike, inside and outside paths.",
       "El kılıcıyla vuruş (boyun hedefli); içten ve dıştan iki hattı da çalış.",
       kind="teknik"),
    _k("karate-empi", "Empi (hiji ate)",
       "Elbow strikes in four directions.",
       "Dirsek darbeleri: öne (mae), yukarı (tate), yana (yoko), geriye (ushiro). "
       "Yakın mesafenin kralı.", kind="teknik"),
    # Teknik — uke
    _k("karate-age-uke", "Age uke",
       "Rising block at 45° above the forehead.",
       "Yukarı blok: ön kol alnın bir yumruk üstünde, 45° açıyla.", kind="teknik"),
    _k("karate-soto-uke", "Soto uke",
       "Outside-inward block.",
       "Dıştan içe blok: yumruk kulak hizasından merkeze.", kind="teknik"),
    _k("karate-uchi-uke", "Uchi uke",
       "Inside-outward block.",
       "İçten dışa blok: kol göğüs önünden dışarı açılır.", kind="teknik"),
    _k("karate-gedan-barai", "Gedan barai",
       "Downward sweep — the most repeated block in kata.",
       "Aşağı süpürme: yumruk karşı omuzdan diz üstüne. Her katanın ilk hareketi.",
       kind="teknik"),
    _k("karate-shuto-uke", "Shuto uke",
       "Knife-hand block in back stance.",
       "El kılıcıyla blok, kokutsu dachi ile birlikte.", kind="teknik"),
    # Teknik — geri
    _k("karate-mae-geri", "Mae geri",
       "Front kick with the ball of the foot; retract faster than you kick.",
       "Öne tekme: diz göğse, ayak topu (koshi) ile it, hızla geri çek.", kind="teknik"),
    _k("karate-mawashi-geri", "Mawashi geri",
       "Roundhouse — knee points, hip turns.",
       "Dairesel tekme: diz hedefi gösterir, kalça döner, ayak sırtıyla temas.",
       kind="teknik"),
    _k("karate-yoko-geri", "Yoko geri",
       "Side kick, thrusting and snapping versions.",
       "Yan tekme: itişli (kekomi) ve kamçılı (keage) iki türü var.", kind="teknik"),
    _k("karate-ushiro-geri", "Ushiro geri",
       "Back kick with the heel, looking over the shoulder.",
       "Geri tekme: topukla, omuz üzerinden bakarak.", kind="teknik"),
    _k("karate-kakato-geri", "Kakato geri",
       "Axe kick — the leg swings up then drops with the heel; used to break a "
       "rising guard.",
       "Balta tekmesi: bacak yukarı savrulup topukla düşer; yükselen korumayı kırmak "
       "için kullanılır.", kind="teknik"),
    _k("karate-nukite", "Nukite",
       "Spear-hand thrust with the fingertips; conditioning comes before power.",
       "Parmak uçlarıyla saplama vuruş (mızrak el). Güçten önce parmak "
       "kondisyonu gelir — makiwara veya kum ile kademeli sertleştir.", kind="teknik"),
]

# --- Taekwondo (WT): Taegeuk + kara kuşak poomsae (kata) + chagi/jireugi/makki/seogi (teknik) ---
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
    _k("tkd-taebaek", "Taebaek",
       "Third black-belt poomsae — named after Mt. Taebaek, symbol of the founding legend.",
       "3. siyah kuşak poomsae'si — kuruluş efsanesinin simgesi Taebaek Dağı'ndan adını alır."),
    _k("tkd-pyongwon", "Pyongwon",
       "'Vast plain' — wide, expansive movements.",
       "'Uçsuz ova' — geniş ve yayılan hareketler."),
    _k("tkd-sipjin", "Sipjin",
       "'Ten' — symbolises steady growth and development.",
       "'On' — istikrarlı büyüme ve gelişimi simgeler."),
    _k("tkd-jitae", "Jitae",
       "'On the earth' — grounded stances, humility toward the ground.",
       "'Yeryüzünde' — yere basan duruşlar, toprağa karşı alçakgönüllülük."),
    _k("tkd-cheonkwon", "Cheonkwon",
       "'Sky' — reverent, expansive movement toward the heavens.",
       "'Gökyüzü' — göğe doğru saygılı ve geniş hareket."),
    _k("tkd-hansu", "Hansu",
       "'Water' — flowing, adaptable movement.",
       "'Su' — akışkan ve uyum sağlayan hareket."),
    _k("tkd-ilyeo", "Ilyeo",
       "'Oneness' — final black-belt poomsae; body and mind as one, named for a monk's teaching.",
       "'Birlik' — son siyah kuşak poomsae'si; beden ve zihnin birliği, bir keşiş öğretisinden adını alır."),
] + [
    # Teknik — chagi
    _k("tkd-ap-chagi", "Ap chagi",
       "Front kick — the mother of all kicks.",
       "Öne tekme: diz göğse, ayak topuyla it. Tüm tekmelerin anasıdır.", True, "teknik"),
    _k("tkd-dollyo-chagi", "Dollyo chagi",
       "Roundhouse — taekwondo's signature.",
       "Dairesel tekme: destek ayağı 90-180° döner, kalça devrilir, ayak sırtıyla vur.",
       kind="teknik"),
    _k("tkd-yop-chagi", "Yop chagi",
       "Side kick with the foot blade.",
       "Yan tekme: diz göğse çekilir, ayak kılıcıyla itiş.", kind="teknik"),
    _k("tkd-dwit-chagi", "Dwit chagi",
       "Back kick — straight line, look first.",
       "Geri tekme: topukla, düz hat üzerinde. Dönüşü kısa tut, bakış önce.",
       kind="teknik"),
    _k("tkd-naeryo-chagi", "Naeryo chagi",
       "Axe kick — requires hamstring flexibility.",
       "Baltalama: bacak yukarı savrulur, topuk düşer. Hamstring esnekliği ister.",
       kind="teknik"),
    _k("tkd-ap-hurigi", "Ap hurigi / Bandal",
       "Whip and crescent kicks of modern competition.",
       "Kamçı ve yarım ay tekmeleri: modern müsabakanın hızlı skorları.", kind="teknik"),
    # Teknik — el
    _k("tkd-momtong-jireugi", "Momtong jireugi",
       "Middle punch — the most frequent poomsae technique.",
       "Gövdeye düz yumruk; karşı el kalçaya çekilir.", kind="teknik"),
    _k("tkd-sonnal-chigi", "Sonnal chigi",
       "Knife-hand strikes, inward and outward.",
       "El kılıcıyla vuruş: içe ve dışa.", kind="teknik"),
    _k("tkd-palkup-chigi", "Palkup chigi",
       "Elbow strike (from Taegeuk 5).",
       "Dirsek darbesi; Taegeuk 5'te tanışırsın.", kind="teknik"),
    # Teknik — makki
    _k("tkd-arae-makki", "Arae makki",
       "Low block.", "Aşağı blok: kol karşı omuzdan diz üstüne süpürür.", kind="teknik"),
    _k("tkd-momtong-makki", "Momtong makki",
       "Middle block, inward and outward.",
       "Gövde bloğu: içe (an) ve dışa (bakat) iki yönü de çalış.", kind="teknik"),
    _k("tkd-olgul-makki", "Olgul makki",
       "High block.", "Yüz bloğu: ön kol alnın üstünde 45°.", kind="teknik"),
    _k("tkd-sonnal-makki", "Sonnal makki",
       "Double knife-hand block in back stance.",
       "El kılıcıyla çift blok, dwit kubi ile birlikte.", kind="teknik"),
    # Teknik — seogi
    _k("tkd-ap-seogi", "Ap seogi",
       "Walking stance.", "Yürüyüş duruşu: doğal adım genişliği.", kind="teknik"),
    _k("tkd-ap-kubi", "Ap kubi",
       "Long front stance.", "Uzun ön duruş: karatedeki zenkutsu'nun karşılığı.",
       kind="teknik"),
    _k("tkd-dwit-kubi", "Dwit kubi",
       "Back stance, 70% rear.", "Geri duruş: ağırlık %70 arkada, ayaklar L.",
       kind="teknik"),
    _k("tkd-juchum-seogi", "Juchum seogi",
       "Horse stance.", "Binici duruş: Taegeuk 7 ve Keumgang'ın temeli.",
       kind="teknik"),
]

CATALOG: dict[str, list[dict]] = {
    "aikijo": AIKIJO,
    "bokken": BOKKEN,
    "jodo": JODO,
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
        all_slugs: set[str] = set()
        for discipline, items in CATALOG.items():
            for i, item in enumerate(items):
                values = {**item, "discipline": discipline, "sort_order": i}
                all_slugs.add(item["slug"])
                stmt = pg_insert(Kata).values(**values).on_conflict_do_update(
                    index_elements=["slug"],
                    set_={k: v for k, v in values.items() if k != "slug"},
                )
                await db.execute(stmt)

        # Katalogdan çıkarılan/yeniden adlandırılan eski satırları temizle
        # (kata tablosuna FK yok — pratik kayıtları etkilenmez).
        await db.execute(Kata.__table__.delete().where(Kata.slug.not_in(all_slugs)))

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
