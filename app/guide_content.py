"""Branş rehberi içeriği: kata ve teknik/vuruş sınıflandırması.

Statik, veritabanı gerektirmez. TR birincil ve detaylı; EN özet.
"steps" alanı yalnızca TR ise şablon TR listesini gösterir.
"diagram" -> /static/img/guide/{diagram}.svg
"program" -> branş sayfasının başındaki "başlangıç programı" kutusu.

DOĞRULUK KURALI: Buraya yalnız kaynaklarla doğrulanabilen bilgi yazılır
(standart kata listeleri, teknik adları, yaygın öğretim sırası). Emin
olunmayan adım listeleri YAZILMAZ; TODO.md'deki "Rehber araştırma
listesi"ne eklenir ve içerik sahibi (İlteriş) doğrulayıp ekler.
"""

GUIDE: dict = {
    # ------------------------------------------------------------------ AIKI-JO
    "aikijo": {
        "has_kata": True,
        "intro": {
            "tr": (
                "Aiki-jo, aikidonun kurucusu Morihei Ueshiba'nın 128 cm'lik jo "
                "(sopa) ile geliştirdiği çalışma sistemidir; bugün en yaygın "
                "hali Morihiro Saito'nun derlediği Iwama müfredatıdır. Sistem üç "
                "katmandan oluşur: 20 suburi (tek başına tekrar edilen temel "
                "vuruşlar), kata (13'lü ve 31'li formlar) ve kumijo (eşli "
                "formlar). Tek başına çalışan biri için ideal sıra: önce suburi "
                "gruplarını tek tek otur, sonra 13'lü kata, sonra 31'li kata. "
                "Her seansta 10-15 dk suburi + 1 kata tekrarı yeterli bir "
                "başlangıç programıdır."
            ),
            "en": (
                "Aiki-jo is the staff system of aikido's founder, best known "
                "today through Morihiro Saito's Iwama curriculum: 20 suburi "
                "(solo striking drills), the 13- and 31-count kata, and paired "
                "kumijo. For solo practice: master the suburi groups first, "
                "then the 13 kata, then the 31."
            ),
        },
        "kata": [
            {
                "name": "13 no jo kata",
                "jp": "十三の形",
                "level": {"tr": "Başlangıç", "en": "Beginner"},
                "diagram": "happo",
                "summary": {
                    "tr": (
                        "13 hareketlik giriş katası: tsuki, gedan gaeshi, men uchi ve "
                        "hasso gaeshi tek akışta birleşir. Suburi gruplarını oturttuysan "
                        "yeni hareket yok demektir — kata sadece sıralamadır. Videodan, "
                        "5'erli bloklar halinde ezberle; günde 5 tekrar iki haftada oturtur."
                    ),
                    "en": (
                        "The 13-count introductory kata combining tsuki, gedan gaeshi, "
                        "men uchi and hasso gaeshi in one flow with happo-style turns."
                    ),
                },
                "todo_note": True,
            
            },
            {
                "name": "31 no jo kata",
                "jp": "三十一の形",
                "level": {"tr": "Orta", "en": "Intermediate"},
                "diagram": "happo",
                "summary": {
                    "tr": (
                        "Iwama müfredatının bel kemiği: 31 hareketlik uzun kata. "
                        "Bütün olarak değil, kısa bölümler halinde ezberlenir; her bölümü "
                        "ayrı ayrı 10'ar kez, sonra baştan sona 3 kez çalış. 13'lü kata "
                        "rahat akmadan başlama — aynı kelimelerle yazılmış daha uzun bir "
                        "cümledir."
                    ),
                    "en": (
                        "The backbone of the Iwama curriculum: a 31-count kata, best "
                        "memorised in six sections, each a coherent attack-response "
                        "scenario."
                    ),
                },
                "todo_note": True,
            
            },
            {
                "name": "Happo giri",
                "jp": "八方切り",
                "level": {"tr": "Başlangıç", "en": "Beginner"},
                "diagram": "happo",
                "summary": {
                    "tr": (
                        "8 yöne kesiş çalışması: kuzeyden başlayıp saat yönünde 8 yöne "
                        "sırayla men uchi. Ayak çalışması ve denge için en iyi ısınma; "
                        "her seansın başına 2 tur koy."
                    ),
                    "en": (
                        "Cutting to eight directions in sequence — the best warm-up "
                        "for footwork and balance."
                    ),
                },
            },
        ],
        "techniques": [
            {
                "group": {"tr": "Tsuki serisi (dürtüşler) — suburi 1-5", "en": "Tsuki series — suburi 1-5"},
                "items": [
                    {"name": "Choku tsuki", "detail": {
                        "tr": "Düz dürtüş. Arka el itiş gücünü verir, ön el yönlendirir; jo koltuk altından değil göbek hizasından çıkar. Hedef: boğaz/göğüs (chudan).",
                        "en": "Straight thrust; rear hand drives, front hand aims. Target chudan."}},
                    {"name": "Kaeshi tsuki", "detail": {
                        "tr": "Çevirmeli dürtüş: jo'nun ucu düşman kılıcını savuşturur gibi döner, ardından dürtüş gelir. El değişimini yavaş çalış, hızlanınca kendiliğinden oturur.",
                        "en": "Turning thrust: the tip deflects, then thrusts. Drill the hand change slowly."}},
                    {"name": "Ushiro tsuki", "detail": {
                        "tr": "Arkaya dürtüş. Önce başını çevirip bak, sonra kalçayı döndürerek dürt — kör dürtüş alışkanlığı edinme.",
                        "en": "Rear thrust — look first, then rotate the hips."}},
                    {"name": "Tsuki gedan gaeshi", "detail": {
                        "tr": "Dürtüş + alçak süpürme: tsuki sonrası jo'nun arka ucu diz/ayak bileği seviyesine döner. Dizlerini kır, süpürmeyi kolla değil gövdeyle yap.",
                        "en": "Thrust then low sweep at knee height; power from the torso, not the arms."}},
                    {"name": "Tsuki jodan gaeshi uchi", "detail": {
                        "tr": "Dürtüş + yukarı çevirip tepeden vuruş. Serinin en uzun hareketi; üç parçaya bölüp (tsuki / çevirme / uchi) ayrı ayrı çalış.",
                        "en": "Thrust, high turn, overhead strike — practise in three parts."}},
                ],
            },
            {
                "group": {"tr": "Uchikomi serisi (vuruşlar) — suburi 6-10", "en": "Uchikomi series — suburi 6-10"},
                "items": [
                    {"name": "Shomen uchikomi", "detail": {
                        "tr": "Tepeden merkez vuruş. Jo başın üstünde tam açılır, bitişte uç göz hizasında durur. Kılıçtaki shomen ile aynı gövde mekaniği.",
                        "en": "Overhead centre strike; finish with the tip at eye level."}},
                    {"name": "Renzoku uchikomi", "detail": {
                        "tr": "Ardışık vuruş: sol-sağ el değişimiyle kesintisiz shomen. Ritim çalışmasıdır — metronom gibi 20 tekrar.",
                        "en": "Continuous alternating strikes — a rhythm drill."}},
                    {"name": "Men uchi gedan gaeshi", "detail": {
                        "tr": "Baş vuruşu + alçak karşılık. Vuruştan sonra geri çekilme yok; aynı adımda alçak süpürme gelir.",
                        "en": "Head strike flowing into a low sweep on the same step."}},
                    {"name": "Men uchi ushiro tsuki", "detail": {
                        "tr": "Baş vuruşu + arkaya dürtüş: önde ve arkada iki hasım varsayımı. Omuz üzerinden bakışı unutma.",
                        "en": "Head strike forward, thrust to the rear — two-opponent assumption."}},
                    {"name": "Gyaku yokomen ushiro tsuki", "detail": {
                        "tr": "Ters yandan şakak vuruşu + arkaya dürtüş. Bileğin esnekliğini test eder; ağır ve geniş başla.",
                        "en": "Reverse side strike to the temple, then rear thrust."}},
                ],
            },
            {
                "group": {"tr": "Katate serisi (tek el) — suburi 11-13", "en": "Katate series — suburi 11-13"},
                "items": [
                    {"name": "Katate gedan gaeshi", "detail": {
                        "tr": "Tek elle alçak süpürme; jo'nun ağırlığını tek bilek taşır. Bilek ağrırsa tempoyu düşür, sayıyı artırma.",
                        "en": "One-handed low sweep; mind the wrist load."}},
                    {"name": "Katate toma uchi", "detail": {
                        "tr": "Tek elle uzun menzil vuruşu: jo'nun en ucundan tutulur, menzil maksimuma çıkar. Aiki-jo'nun imza hareketi.",
                        "en": "One-handed long-range strike from the very end of the jo."}},
                    {"name": "Katate hachi no ji gaeshi", "detail": {
                        "tr": "Tek elle 8 çizme: jo önde yatay 8 (∞) çizer. Bilek gevşek, dirsek sabit; jo spin çalışmasının temelidir.",
                        "en": "One-handed figure-eight — the basis of jo spinning."}},
                ],
            },
            {
                "group": {"tr": "Hasso gaeshi serisi — suburi 14-18", "en": "Hasso gaeshi series — suburi 14-18"},
                "items": [
                    {"name": "Hasso gaeshi uchi", "detail": {
                        "tr": "Jo dikeyde omuz hizasına döner (hasso), oradan vuruş. Dönüş sırasında jo yüzüne çarpmasın diye dirsekleri açık tut.",
                        "en": "Turn the jo up to hasso at the shoulder, strike from there."}},
                    {"name": "Hasso gaeshi tsuki", "detail": {"tr": "Hasso'dan dürtüş.", "en": "Thrust from hasso."}},
                    {"name": "Hasso gaeshi ushiro tsuki", "detail": {"tr": "Hasso'dan arkaya dürtüş.", "en": "Rear thrust from hasso."}},
                    {"name": "Hasso gaeshi ushiro uchi", "detail": {"tr": "Hasso'dan arkaya vuruş.", "en": "Rear strike from hasso."}},
                    {"name": "Hasso gaeshi ushiro barai", "detail": {
                        "tr": "Hasso'dan arkaya süpürme — serinin en tekniklisi; kalça dönüşü olmadan yapılamaz.",
                        "en": "Rear sweep from hasso — impossible without hip rotation."}},
                ],
            },
            {
                "group": {"tr": "Nagare gaeshi (akış) — suburi 19-20", "en": "Nagare gaeshi — suburi 19-20"},
                "items": [
                    {"name": "Hidari nagare gaeshi uchi", "detail": {
                        "tr": "Sola akan çevirme + vuruş: savuşturma ve karşılık tek harekette erir. 31'li katanın 5. bölümünün temelidir.",
                        "en": "Flowing left deflection merging into a strike."}},
                    {"name": "Migi nagare gaeshi tsuki", "detail": {
                        "tr": "Sağa akan çevirme + dürtüş. İki nagare'yi art arda bağlayıp 'akış turu' olarak çalışmak jo freestyle'ın kapısını açar.",
                        "en": "Flowing right deflection into a thrust; chains into freestyle work."}},
                ],
            },
        ],
    },
    # ------------------------------------------------------------------ BOKKEN (AIKI-KEN)
    "bokken": {
        "has_kata": True,
        "intro": {
            "tr": (
                "Aiki-ken, aikidonun bokken (tahta kılıç) çalışmasıdır; Iwama "
                "sisteminde 7 suburi, happo giri ve 5 kumitachi'den oluşur. "
                "Kılıç tutuşu (te-no-uchi) her şeyin temelidir: sol el kabzanın "
                "dibinde güç verir, sağ el tsuba'ya yakın yönlendirir, iki "
                "elin de küçük parmakları sıkı, işaret parmakları gevşektir. "
                "Solo program: 10 dk suburi (her birinden 10'ar) + happo giri "
                "2 tur + kumitachi'nin kendi tarafını gölge çalışması."
            ),
            "en": (
                "Aiki-ken is aikido's wooden-sword method: 7 suburi, happo giri "
                "and 5 paired kumitachi. Grip (te-no-uchi) is the foundation — "
                "left hand powers from the pommel, right hand steers."
            ),
        },
        "kata": [
            {
                "name": "Happo giri",
                "jp": "八方切り",
                "level": {"tr": "Başlangıç", "en": "Beginner"},
                "diagram": "happo",
                "summary": {
                    "tr": "8 yöne shomen kesişi. Her dönüşte ayaklar önce, kılıç sonra; kesişler aynı yükseklikte bitmeli.",
                    "en": "Shomen cuts to eight directions; feet turn first, sword follows.",
                },
            },
            {
                "name": "Kumitachi 1-5 (solo hali)",
                "jp": "組太刀",
                "level": {"tr": "İleri", "en": "Advanced"},
                "summary": {
                    "tr": (
                        "Beş eşli kılıç formu. Partner yokken her formun uchitachi "
                        "(saldıran) tarafını gölge olarak çalış: mesafeyi zihninde "
                        "kur, duraklamaları koru. Eşli çalışma imkânı bulduğunda "
                        "beden zaten hazır olur."
                    ),
                    "en": (
                        "The five paired sword forms; practise the attacking side "
                        "solo as shadow work, keeping the pauses."
                    ),
                },
            },
        ],
        "techniques": [
            {
                "group": {"tr": "7 Suburi", "en": "The 7 suburi"},
                "items": [
                    {"name": "Ichi no suburi", "detail": {
                        "tr": "Tam shomen kesişi: kılıç başın üstünde tam açılır, kesiş chudan hizasında durur. Diz-kalça-omuz aynı anda düşer; kol gücüyle kesme. Diğer altı suburi bunun üstüne kurulur — ilk ay sadece bunu çalışmak meşrudur.",
                        "en": "The full overhead cut; the other six build on it. Spending the first month on this alone is legitimate."}},
                    {"name": "Ni — Nana no suburi", "detail": {
                        "tr": "2-7. suburi, ichi'nin üzerine geri çekilme, savuşturma, ardışık kesiş ve tsuki katmanlarını ekler. Her birinin kesin tanımı Iwama çizgisinde videoyla/öğretmenle öğrenilir — kütüphanedeki videolardan takip et; yazılı tarif yanlış alışkanlık oturtur.",
                        "en": "Suburi 2-7 add stepping, deflection, continuous cuts and thrusts on top of ichi. Learn their exact definitions from the videos in the library — written descriptions build bad habits."}},
                ],
            },
            {
                "group": {"tr": "Kamae (duruşlar)", "en": "Kamae (stances)"},
                "items": [
                    {"name": "Seigan / Chudan no kamae", "detail": {
                        "tr": "Temel duruş: kılıcın ucu rakibin boğazına. Bütün suburi buradan başlar, buraya döner.",
                        "en": "The basic guard — tip at the opponent's throat."}},
                    {"name": "Jodan no kamae", "detail": {
                        "tr": "Kılıç başın üstünde, saldırıya hazır. Dirsekler kulakları kapatmaz; koltuk altı açık.",
                        "en": "Sword overhead, ready to strike."}},
                    {"name": "Hasso no kamae", "detail": {
                        "tr": "Kılıç dik, tsuba omuz hizasında. Bekleme ve gözlem duruşu.",
                        "en": "Vertical sword at the shoulder — an observing posture."}},
                    {"name": "Waki gamae", "detail": {
                        "tr": "Kılıç arkada gizli, uzunluğu göstermez. Kesişi 'yoktan' başlatma çalışması.",
                        "en": "Sword hidden behind — striking 'from nowhere'."}},
                    {"name": "Gedan no kamae", "detail": {
                        "tr": "Uç aşağıda, davet duruşu. Buradan yukarı savuşturma (suriage) doğar.",
                        "en": "Tip low — an inviting guard from which rising deflections grow."}},
                ],
            },
        ],
    },
    # ------------------------------------------------------------------ AIKIDO
    "aikido": {
        "has_kata": False,
        "intro": {
            "tr": (
                "Aikidonun geleneksel anlamda solo katası yoktur; sanat eşli "
                "çalışmaya dayanır. Ama tek başına geliştirilebilecek üç temel "
                "katman vardır ve dojoda fark yaratan da bunlardır: tai sabaki "
                "(beden hareketi), ukemi (düşüş) ve ashi sabaki (ayak "
                "çalışması). Solo program önerisi: 5 dk irimi-tenkan turu, 5 dk "
                "shikko (diz yürüyüşü), 10 ukemi (yumuşak zeminde), 5 dk "
                "suburi (bkz. aiki-jo / bokken)."
            ),
            "en": (
                "Aikido has no traditional solo kata — but tai sabaki (body "
                "movement), ukemi (falling) and ashi sabaki (footwork) can all "
                "be trained alone, and they are what set you apart in the dojo."
            ),
        },
        "kata": [],
        "techniques": [
            {
                "group": {"tr": "Tai sabaki (beden hareketleri)", "en": "Tai sabaki"},
                "items": [
                    {"name": "Irimi", "detail": {
                        "tr": "Girme: saldırı hattının içine, rakibin arkasına doğru tek düz adım. Solo çalışmada bir duvar köşesini rakip say, hattın dışına gir.",
                        "en": "Entering straight past the line of attack."}},
                    {"name": "Tenkan", "detail": {
                        "tr": "Dönme: ön ayak sabit, arka ayak 180° süpürür. Günde 20 tekrar — dönüş sonunda omuzlar ve kalça aynı yöne bakmalı.",
                        "en": "Pivot 180° around the front foot."}},
                    {"name": "Irimi-tenkan", "detail": {
                        "tr": "İkisinin birleşimi: gir + dön. Aikidonun 'yürüyüşü' budur; müzikle ritmik çalışmak dengeyi hızla geliştirir.",
                        "en": "Enter then pivot — aikido's fundamental 'walk'."}},
                    {"name": "Shikko", "detail": {
                        "tr": "Diz üstü yürüyüş. Suwariwaza'nın temeli; 2×dojo boyu gidiş-dönüş dizleri ve kalça hareketini açar.",
                        "en": "Knee walking — the base of seated techniques."}},
                ],
            },
            {
                "group": {"tr": "Ukemi (düşüşler)", "en": "Ukemi (falls)"},
                "items": [
                    {"name": "Mae ukemi (öne yuvarlanma)", "detail": {
                        "tr": "Öne yuvarlanma: kol yay olur, temas noktası el kenarından omuza, çapraz sırt üzerinden kalk. Yumuşak zeminde günde 10 tekrar.",
                        "en": "Forward roll along the arm and across the back."}},
                    {"name": "Ushiro ukemi (geriye)", "detail": {
                        "tr": "Geriye yuvarlanma: çene göğüste, sırt yuvarlak. Önce oturuştan, sonra çömelmeden, en son ayakta başlayarak ilerle.",
                        "en": "Backward roll — progress from sitting to standing."}},
                    {"name": "Yoko ukemi (yana)", "detail": {
                        "tr": "Yana düşüş: kol ve bacak aynı anda yere vurur, baş asla değmez.",
                        "en": "Side breakfall — arm and leg strike together."}},
                ],
            },
            {
                "group": {"tr": "Temel el saldırıları (uke tarafı)", "en": "Basic strikes (uke side)"},
                "items": [
                    {"name": "Shomen uchi", "detail": {
                        "tr": "Tepeden el kılıcıyla (tegatana) merkez vuruş. Kılıç kesişiyle aynı mekanik — bokken suburi'si bunu doğrudan besler.",
                        "en": "Overhead strike with the hand blade; same mechanics as a sword cut."}},
                    {"name": "Yokomen uchi", "detail": {
                        "tr": "Şakağa diyagonal vuruş. Omuzdan değil kalçadan başlar.",
                        "en": "Diagonal strike to the temple."}},
                    {"name": "Tsuki", "detail": {
                        "tr": "Karına düz yumruk. Aikido tsuki'si adımla birlikte gelir; yerinde yumruk atma.",
                        "en": "Straight punch to the abdomen, stepping in."}},
                ],
            },
            {
                "group": {"tr": "Temel teknik prensipleri (zihinsel çalışma)", "en": "Core technique principles"},
                "items": [
                    {"name": "Ikkyo", "detail": {
                        "tr": "Birinci prensip: dirsek kontrolü. Solo: ikkyo undo — kollar merkezden yukarı yay çizer, 20 tekrar.",
                        "en": "First principle: elbow control. Solo drill: ikkyo undo."}},
                    {"name": "Shiho nage", "detail": {
                        "tr": "Dört yön fırlatması: kılıç kesişinin atışa dönmüş hali. Solo: bokken ile 4 yöne kesiş yaparak ayak düzenini otur.",
                        "en": "Four-direction throw; drill the footwork with a bokken."}},
                    {"name": "Kote gaeshi / Irimi nage", "detail": {
                        "tr": "Bilek çevirme ve giriş atışı. Eşsiz çalışılamaz ama tai sabaki kalıpları (tenkan + kesiş) atışın %80'idir.",
                        "en": "Wrist turn and entering throw — the tai sabaki patterns are 80% of the throw."}},
                ],
            },
        ],
    },
    # ------------------------------------------------------------------ JODO (ZNKR SEITEI)
    "jodo": {
        "has_kata": True,
        "intro": {
            "tr": (
                "Seitei Jodo, Zen Nihon Kendo Renmei'nin Shinto Muso-ryu'dan "
                "derlediği standart müfredattır: 12 kihon (temel teknik) ve 12 "
                "kata. Kata'lar jo ile tachi (kılıç) arasında eşlidir; tek "
                "başına çalışırken jo tarafını hayali kılıca karşı, mesafe ve "
                "zamanlamayı zihinde kurarak yap (tandoku dosa). Solo program: "
                "12 kihonu sırayla 5'er tekrar (≈15 dk), ardından bildiğin "
                "kataları ikişer kez."
            ),
            "en": (
                "Seitei Jodo is the ZNKR's standard curriculum drawn from "
                "Shinto Muso-ryu: 12 kihon and 12 kata (jo versus sword). "
                "Solo, practise the jo side against an imagined tachi."
            ),
        },
        "kata": [
            {"name": "1. Tsuki Zue", "jp": "着杖", "level": {"tr": "Başlangıç", "en": "Beginner"},
             "summary": {"tr": "Bastona dayanır gibi nötr duruştan gizli karşı saldırı: hiki otoshi ile kılıcı düşürüp tsuki.", "en": "From a neutral walking-stick posture into hiki otoshi and thrust."}},
            {"name": "2. Suigetsu", "jp": "水月", "level": {"tr": "Başlangıç", "en": "Beginner"},
             "summary": {"tr": "Suigetsu (solar plexus) noktasına tek ölümcül dürtüş; girişteki açı alma katanın özüdür.", "en": "A single decisive thrust to the solar plexus."}},
            {"name": "3. Hissage", "jp": "引提", "level": {"tr": "Başlangıç", "en": "Beginner"},
             "summary": {"tr": "Jo gizlenmiş halde bekler, kılıç kesişiyle aynı anda ortaya çıkar.", "en": "The jo waits hidden, appearing with the sword's cut."}},
            {"name": "4. Shamen", "jp": "斜面", "level": {"tr": "Başlangıç", "en": "Beginner"},
             "summary": {"tr": "Şakağa (shamen) çapraz vuruşla kılıcı durdurma.", "en": "Stopping the sword with a diagonal strike to the temple."}},
            {"name": "5. Sakan", "jp": "左貫", "level": {"tr": "Orta", "en": "Intermediate"},
             "summary": {"tr": "Soldan delme: maki otoshi ile kılıcı sarıp düşürdükten sonra dürtüş.", "en": "Wrapping the sword down with maki otoshi, then thrusting."}},
            {"name": "6. Monomi", "jp": "物見", "level": {"tr": "Orta", "en": "Intermediate"},
             "summary": {"tr": "Gözcü duruşundan savunma; uzak mesafeden kontrollü giriş.", "en": "Defence from the lookout posture; controlled entry from distance."}},
            {"name": "7. Kasumi", "jp": "霞", "level": {"tr": "Orta", "en": "Intermediate"},
             "summary": {"tr": "'Sis': jo görüşü perdeler, rakip niyeti okuyamaz.", "en": "'Mist' — the jo veils your intent."}},
            {"name": "8. Tachi Otoshi", "jp": "太刀落", "level": {"tr": "Orta", "en": "Intermediate"},
             "summary": {"tr": "Kılıcı düşürme: hiki otoshi'nin kata içindeki tam uygulaması.", "en": "Dropping the sword — hiki otoshi in full application."}},
            {"name": "9. Rai Uchi", "jp": "雷打", "level": {"tr": "İleri", "en": "Advanced"},
             "summary": {"tr": "'Yıldırım vuruşu': tai atari (beden çarpması) ile mesafeyi çökertip vuruş.", "en": "'Thunder strike' — collapsing distance with tai atari."}},
            {"name": "10. Seigan", "jp": "正眼", "level": {"tr": "İleri", "en": "Advanced"},
             "summary": {"tr": "Kılıcın seigan duruşuna karşı merkez hattı mücadelesi.", "en": "Contesting the centre line against seigan."}},
            {"name": "11. Midare Dome", "jp": "乱留", "level": {"tr": "İleri", "en": "Advanced"},
             "summary": {"tr": "Ardışık saldırıları 'karışıklığı durdurarak' kesme; serinin en hızlı katası.", "en": "Stopping successive attacks — the fastest kata of the set."}},
            {"name": "12. Ran Ai", "jp": "乱合", "level": {"tr": "İleri", "en": "Advanced"},
             "summary": {"tr": "Uzun final katası: 12 kihonun neredeyse tamamını tek senaryoda birleştirir.", "en": "The long final kata combining nearly all twelve kihon."}},
        ],
        "techniques": [
            {
                "group": {"tr": "12 Kihon (temel teknikler)", "en": "The 12 kihon"},
                "items": [
                    {"name": "Honte uchi", "detail": {"tr": "Normal tutuşla temel vuruş — jodonun shomen'i. Bitişte jo'nun ucu rakibin şakağını gösterir.", "en": "Basic strike with the standard grip."}},
                    {"name": "Gyakute uchi", "detail": {"tr": "Ters tutuşla vuruş; jo'nun iki ucu da silahtır fikrini öğretir.", "en": "Strike with the reversed grip — both ends are weapons."}},
                    {"name": "Hiki otoshi uchi", "detail": {"tr": "Kılıcı aşağı düşüren vuruş: jo kılıcın yan yüzüne kayarak iner. Jodonun imza tekniği.", "en": "The signature technique: sliding strike that drops the sword."}},
                    {"name": "Kaeshi tsuki", "detail": {"tr": "Çevirmeli dürtüş: savuşturmadan dönerek boğaza.", "en": "Turning thrust to the throat."}},
                    {"name": "Gyakute tsuki", "detail": {"tr": "Ters tutuşla dürtüş.", "en": "Reversed-grip thrust."}},
                    {"name": "Maki otoshi", "detail": {"tr": "Kılıcı sarıp düşürme: jo kılıca spiral sarılır. Yavaş çalış; hız değil açı iş yapar.", "en": "Spiral wrap that drops the sword — angle over speed."}},
                    {"name": "Kuri tsuke", "detail": {"tr": "Kılıcı ve elleri yere doğru kilitleme.", "en": "Pinning sword and hands downward."}},
                    {"name": "Kuri hanashi", "detail": {"tr": "Kilitleyip fırlatma: kuri tsuke'nin devamı.", "en": "Pinning then casting away."}},
                    {"name": "Tai atari", "detail": {"tr": "Beden çarpması: jo üzerinden gövdeyle itiş.", "en": "Body check through the jo."}},
                    {"name": "Tsuki hazushi uchi", "detail": {"tr": "Dürtüşü savuşturup vuruş.", "en": "Evading a thrust into a strike."}},
                    {"name": "Dou barai uchi", "detail": {"tr": "Gövde süpürmesini savuşturup vuruş.", "en": "Parrying a torso cut into a strike."}},
                    {"name": "Tai hazushi uchi", "detail": {"tr": "Bedeni hattan çıkarıp vuruş: sabaki + uchi tek harekette.", "en": "Off-line evasion merging into a strike."}},
                ],
            },
        ],
    },
    # ------------------------------------------------------------------ JOJUTSU
    "jojutsu": {
        "has_kata": True,
        "intro": {
            "tr": (
                "Jojutsu, jodonun koryu (eski okul) kökenidir; ana kaynak "
                "Shinto Muso-ryu'dur. Teknik temel Seitei Jodo ile aynı 12 "
                "kihon üzerine kurulur (jodo bölümüne bak); fark, kata "
                "setlerinin derinliğindedir: Omote (12), Chudan (12), Ran Ai, "
                "Kage, Samidare, Gohon no Midare ve Okuden setleri. Koryu "
                "kataları öğretmensiz öğrenilmez — solo çalışan biri için "
                "doğru hedef: 12 kihonu kusursuzlaştırmak ve Omote setinin "
                "isimlerini/senaryolarını tanımak."
            ),
            "en": (
                "Jojutsu is the koryu root of jodo (Shinto Muso-ryu). The "
                "technical base is the same 12 kihon (see Jodo); the koryu "
                "depth lies in the kata sets: Omote, Chudan, Ran Ai, Kage, "
                "Samidare and beyond. Solo, perfect the kihon."
            ),
        },
        "kata": [
            {"name": "Omote seti (12 kata)", "jp": "表", "level": {"tr": "Koryu — giriş", "en": "Koryu — entry"},
             "summary": {"tr": "İlk koryu seti: Tachi Otoshi, Tsuba Wari, Sun Dome, Hissage... Seitei'nin atalarıdır; senaryolar daha kısa mesafeli ve serttir.", "en": "The first koryu set — ancestors of the Seitei kata, at closer and harder distance."}},
            {"name": "Chudan seti (12 kata)", "jp": "中段", "level": {"tr": "Koryu — orta", "en": "Koryu — middle"},
             "summary": {"tr": "İkinci set; kılıç tarafı daha inisiyatifli, jo tarafı daha ince açı çalışır.", "en": "Second set with a more assertive sword side."}},
            {"name": "İleri setler (Ran Ai, Kage, Samidare, Okuden)", "jp": "乱合・影・五月雨・奥伝", "level": {"tr": "Koryu — ileri", "en": "Koryu — advanced"},
             "summary": {"tr": "Okul geleneği içinde, öğretmenle aktarılan setler. Solo pratisyen için: isimleri bil, videolarını izle, kihon çalış.", "en": "Transmitted teacher-to-student; know the names, watch, and drill kihon."}},
        ],
        "techniques": [
            {
                "group": {"tr": "Temel (Seitei ile ortak)", "en": "Fundamentals (shared with Seitei)"},
                "items": [
                    {"name": "12 kihon", "detail": {"tr": "Honte uchi'den tai hazushi uchi'ye — tam liste ve açıklamalar Jodo bölümünde.", "en": "From honte uchi to tai hazushi uchi — full list under Jodo."}},
                    {"name": "Suburi rutini", "detail": {"tr": "Koryu jojutsu'da da günlük temel aynıdır: honte uchi 20, gyakute uchi 20, hiki otoshi 20, kaeshi tsuki 20.", "en": "Daily basics: 20 reps each of the four core strikes."}},
                ],
            },
        ],
    },
    # ------------------------------------------------------------------ KENJUTSU
    "kenjutsu": {
        "has_kata": True,
        "intro": {
            "tr": (
                "Kenjutsu tek bir sistem değil, yüzlerce koryu okulunun (Katori "
                "Shinto-ryu, Kashima Shin-ryu, Itto-ryu...) ortak adıdır; her "
                "okulun kendi kataları vardır ve bunlar öğretmenle öğrenilir. "
                "Tek başına çalışan için evrensel olan katman şudur: kamae'ler, "
                "temel kesişler ve suburi. Aşağıdaki müfredat okuldan bağımsız "
                "ortak çekirdektir; okul katası yerine bu çekirdeği derinleştir."
            ),
            "en": (
                "Kenjutsu is the umbrella term for hundreds of koryu sword "
                "schools, each with its own kata taught in person. The "
                "universal solo layer is kamae, fundamental cuts and suburi."
            ),
        },
        "kata": [
            {"name": "Okul kataları hakkında", "jp": "古流形", "level": {"tr": "Bilgi", "en": "Note"},
             "summary": {"tr": "Kenjutsu kataları okula özgüdür (ör. Katori Shinto-ryu'nun Omote no Tachi'si). Okula bağlı değilsen kata taklidi yerine kesiş kalitesine yatırım yap; Iaido veya Kendo kataları standartlaştırılmış alternatiflerdir.", "en": "Kenjutsu kata are school-specific; without a school, invest in cut quality or use the standardised Iaido/Kendo kata."}},
        ],
        "techniques": [
            {
                "group": {"tr": "Temel kesişler", "en": "Fundamental cuts"},
                "items": [
                    {"name": "Kiri oroshi (shomen)", "detail": {"tr": "Dikey merkez kesiş: tepeden başlar, chudan'da durur. Kesişin freni bilek değil karın kasıdır.", "en": "Vertical centre cut braked by the core, not the wrists."}},
                    {"name": "Kesa giri", "detail": {"tr": "Omuzdan çapraza (keşiş cübbesi hattı) kesiş. Sağ ve sol kesa'yı eşit çalış — herkesin zayıf tarafı vardır.", "en": "Diagonal cut along the monk's-robe line, both sides equally."}},
                    {"name": "Gyaku kesa / kiri age", "detail": {"tr": "Aşağıdan yukarı ters çapraz kesiş.", "en": "Rising reverse diagonal cut."}},
                    {"name": "Do giri (yoko ichimonji)", "detail": {"tr": "Yatay gövde kesişi; kalça dönüşüyle atılır.", "en": "Horizontal torso cut driven by the hips."}},
                    {"name": "Tsuki", "detail": {"tr": "Boğaza dürtüş; kesişten daha az kuvvet, daha çok hat ister.", "en": "Thrust to the throat — line over power."}},
                ],
            },
            {
                "group": {"tr": "Kamae ve suburi", "en": "Kamae and suburi"},
                "items": [
                    {"name": "Beş kamae", "detail": {"tr": "Chudan, jodan, gedan, hasso, waki — açıklamalar Bokken bölümünde; kenjutsu'da okullara göre isim ve açı değişir.", "en": "The five guards (see Bokken); names and angles vary by school."}},
                    {"name": "Suburi rutini", "detail": {"tr": "Kiri oroshi 30, kesa giri 20+20, do giri 10+10, tsuki 20. Ayna karşısında haftada bir form kontrolü yap.", "en": "30 vertical, 20+20 diagonal, 10+10 horizontal, 20 thrusts; check form in a mirror weekly."}},
                ],
            },
        ],
    },
    # ------------------------------------------------------------------ KENDO
    "kendo": {
        "has_kata": True,
        "intro": {
            "tr": (
                "Kendo modern kılıç sporu ve yoludur; müsabaka shinai (bambu "
                "kılıç) ve bogu (zırh) ile yapılır ama solo temel çalışması "
                "zengindir: suburi, ashi sabaki ve Nihon Kendo Kata (bokken "
                "ile). Solo program: 10 dk ashi sabaki, 100 suburi (30 joge, "
                "30 shomen, 20 sayu men, 20 haya suburi), sonra bildiğin "
                "kataların iki tarafını da yavaş çalış."
            ),
            "en": (
                "Kendo is the modern way of the sword. Solo work is rich: "
                "suburi, footwork, and the Nihon Kendo Kata with a bokken."
            ),
        },
        "kata": [
            {"name": "Kata 1 — Ipponme", "jp": "一本目", "level": {"tr": "Temel", "en": "Fundamental"},
             "summary": {"tr": "Jodan'a karşı jodan: rakibin kesişini geri çekilerek boşa çıkar, men kesişiyle bitir. Zanshin vurgusu en yüksek katadır.", "en": "Jodan vs jodan — evade by stepping back, finish with men."}},
            {"name": "Kata 2 — Nihonme", "jp": "二本目", "level": {"tr": "Temel", "en": "Fundamental"},
             "summary": {"tr": "Kote kesişine karşı geri çekilip kote ile karşılık.", "en": "Against kote: withdraw and counter-cut kote."}},
            {"name": "Kata 3 — Sanbonme", "jp": "三本目", "level": {"tr": "Temel", "en": "Fundamental"},
             "summary": {"tr": "Tsuki'ye karşı tsuki: merkez hattı mücadelesinin saf hali.", "en": "Thrust against thrust — pure centre-line contest."}},
            {"name": "Kata 4-7", "jp": "四〜七本目", "level": {"tr": "Orta", "en": "Intermediate"},
             "summary": {"tr": "Hasso ve waki kamae'ler, kaeshi (çevirme) ve suriage (kaydırarak yükseltme) teknikleri devreye girer.", "en": "Introduce hasso/waki guards, kaeshi and suriage."}},
            {"name": "Kodachi kata 1-3", "jp": "小太刀", "level": {"tr": "İleri", "en": "Advanced"},
             "summary": {"tr": "Kısa kılıçla üç kata: mesafe kapatma ve irimi çalışması.", "en": "Three short-sword kata — closing distance and entering."}},
        ],
        "techniques": [
            {
                "group": {"tr": "Suburi", "en": "Suburi"},
                "items": [
                    {"name": "Joge buri", "detail": {"tr": "Büyük tam kesiş: kılıç kuyruk sokumuna değecek kadar geri, öne tam uzanım. Omuz açma egzersizi.", "en": "Large full swings opening the shoulders."}},
                    {"name": "Shomen suburi", "detail": {"tr": "Men hizasında biten merkez kesiş; kendonun ekmek teknesi. Sayarak, nefesle: 30 tekrar.", "en": "Centre cuts finishing at men height."}},
                    {"name": "Sayu men", "detail": {"tr": "Sağ-sol çapraz men kesişleri; 45° hat.", "en": "Alternating diagonal men cuts."}},
                    {"name": "Haya suburi", "detail": {"tr": "Sıçramalı hızlı suburi: ileri-geri okuri ashi ile kesintisiz shomen. Kondisyonun ölçüsü — 20'den başla, 50'ye çık.",
                                                        "en": "Jumping fast suburi — the conditioning benchmark."}},
                ],
            },
            {
                "group": {"tr": "Datotsu (vuruş hedefleri)", "en": "Datotsu (targets)"},
                "items": [
                    {"name": "Men", "detail": {"tr": "Başın merkezi ve sağ/sol şakak (sayu men). Kesiş + fumikomi (basış) + kiai aynı anda.", "en": "Centre and sides of the head; cut, stamp and kiai together."}},
                    {"name": "Kote", "detail": {"tr": "Sağ bilek (jodan'a karşı sol da geçerli). Küçük ve keskin kesiş.", "en": "The right wrist — a small, sharp cut."}},
                    {"name": "Do", "detail": {"tr": "Gövdenin sağ/sol yanı; kesiş diyagonal iner, kılıç çekilerek kesilir.", "en": "The torso, cut diagonally with a drawing action."}},
                    {"name": "Tsuki", "detail": {"tr": "Boğaz dürtüşü — yalnız ileri seviyede çalışılır; solo'da hedefe değil mesafeye odaklan.", "en": "Throat thrust — advanced only."}},
                ],
            },
            {
                "group": {"tr": "Ashi sabaki (ayak çalışması)", "en": "Footwork"},
                "items": [
                    {"name": "Okuri ashi", "detail": {"tr": "Kayan adım: ön ayak gider, arka ayak takip eder, topuklar hafif havada. Kendonun tüm hareketi bunun üstüne kurulur.", "en": "The sliding step underlying all kendo movement."}},
                    {"name": "Fumikomi", "detail": {"tr": "Vuruş anındaki sert basış; ayak tabanı düz iner. Yumuşak zeminde çalış, eklem koru.", "en": "The stamping step at the moment of the strike."}},
                    {"name": "Suriashi turları", "detail": {"tr": "Dojo boyu ileri-geri-sağa-sola kayan adım turları; günde 5 dk.", "en": "Sliding-step laps in all four directions."}},
                ],
            },
            {
                "group": {"tr": "Kirikaeshi", "en": "Kirikaeshi"},
                "items": [
                    {"name": "Kirikaeshi (solo)", "detail": {"tr": "Shomen + 9 sayu men + shomen dizisi. Partner/makiwara yoksa havaya, mesafeyi hayal ederek — nefes ve ritim çalışmasıdır.",
                                                             "en": "Shomen + nine alternating men + shomen; solo it is a breath-and-rhythm drill."}},
                ],
            },
        ],
    },
    # ------------------------------------------------------------------ IAIDO (ZNKR SEITEI)
    "iaido": {
        "has_kata": True,
        "intro": {
            "tr": (
                "Iaido kılıcı çekme sanatıdır: her kata nukitsuke (çekişle "
                "kesiş), kirioroshi (esas kesiş), chiburi (kanı silkme) ve "
                "noto (kılıfa koyma) fazlarından oluşur. Seitei Iai'nin 12 "
                "katası standarttır ve iaido zaten SOLO bir sanattır — bu "
                "listedeki en uygun branş. Iaito yoksa bokken ile (saya "
                "olmadan) fazların hepsi çalışılabilir. Program: her seans 3 "
                "kata seç, her birini 5'er kez; ayda bir 12'sini sırayla geç."
            ),
            "en": (
                "Iaido is the art of drawing the sword — inherently a solo "
                "art. Each kata cycles nukitsuke, kirioroshi, chiburi and "
                "noto. The 12 Seitei kata are the standard."
            ),
        },
        "kata": [
            {"name": "1. Mae", "jp": "前", "level": {"tr": "Başlangıç", "en": "Beginner"},
             "summary": {"tr": "Seiza'dan öne: yatay nukitsuke + dikey kirioroshi. Iaidonun alfabesi; ilk 6 ay her seansta çalışılır.", "en": "From seiza: horizontal draw, vertical cut — iaido's alphabet."}},
            {"name": "2. Ushiro", "jp": "後ろ", "level": {"tr": "Başlangıç", "en": "Beginner"},
             "summary": {"tr": "Arkadaki hasma dönerek Mae'nin aynısı; dönüş dizler üstünde.", "en": "Mae turned 180° to a rear opponent."}},
            {"name": "3. Uke Nagashi", "jp": "受け流し", "level": {"tr": "Orta", "en": "Intermediate"},
             "summary": {"tr": "Kesişi kılıçla akıtarak savuşturup tek harekette karşı kesiş.", "en": "Flowing parry merging into a counter-cut."}},
            {"name": "4. Tsuka Ate", "jp": "柄当て", "level": {"tr": "Orta", "en": "Intermediate"},
             "summary": {"tr": "İki hasım: öndekine kabza darbesi, arkadakine dürtüş.", "en": "Pommel strike forward, thrust to the rear."}},
            {"name": "5. Kesa Giri", "jp": "袈裟切り", "level": {"tr": "Orta", "en": "Intermediate"},
             "summary": {"tr": "Ayakta: yukarı ters kesişle çekiş + aşağı kesa kesişi.", "en": "Rising draw-cut then descending kesa cut."}},
            {"name": "6. Morote Tsuki", "jp": "諸手突き", "level": {"tr": "Orta", "en": "Intermediate"},
             "summary": {"tr": "İki elle dürtüş; öne ve arkaya üç hasım senaryosu.", "en": "Two-handed thrust; three opponents."}},
            {"name": "7. Sanpo Giri", "jp": "三方切り", "level": {"tr": "Orta", "en": "Intermediate"},
             "summary": {"tr": "Üç yöne kesiş: sağ, sol, ön — yön değişimlerinde duraklamadan.", "en": "Cutting to three directions without pause."}},
            {"name": "8. Ganmen Ate", "jp": "顔面当て", "level": {"tr": "Orta", "en": "Intermediate"},
             "summary": {"tr": "Kabzayla yüze darbe + arkaya dürtüş + öne kesiş.", "en": "Pommel to the face, rear thrust, forward cut."}},
            {"name": "9. Soete Tsuki", "jp": "添え手突き", "level": {"tr": "İleri", "en": "Advanced"},
             "summary": {"tr": "Destek elli dürtüş: sol el namlunun sırtında.", "en": "Supported thrust with the left hand on the blade's back."}},
            {"name": "10. Shiho Giri", "jp": "四方切り", "level": {"tr": "İleri", "en": "Advanced"},
             "summary": {"tr": "Dört yöne kesiş; Sanpo Giri'nin genişletilmişi.", "en": "Cuts to four directions."}},
            {"name": "11. Sou Giri", "jp": "総切り", "level": {"tr": "İleri", "en": "Advanced"},
             "summary": {"tr": "Ardışık beş kesişle ilerleme: nuki uchi'den sonra kesintisiz seri.", "en": "Advancing with five successive cuts."}},
            {"name": "12. Nuki Uchi", "jp": "抜き打ち", "level": {"tr": "İleri", "en": "Advanced"},
             "summary": {"tr": "Geri çekilerek çekişle aynı anda kesiş — en kısa ve en zor kata.", "en": "Draw and cut in one beat while stepping back — shortest and hardest."}},
        ],
        "techniques": [
            {
                "group": {"tr": "Dört faz", "en": "The four phases"},
                "items": [
                    {"name": "Nukitsuke", "detail": {"tr": "Çekişle kesiş: kılıç kılıftan çıkarken kesmeye başlar; saya biki (kılıfın geri çekilmesi) hızın yarısıdır.", "en": "The draw that cuts; half the speed is the scabbard pulling back."}},
                    {"name": "Kirioroshi", "detail": {"tr": "Esas kesiş: tam yukarı açılım, merkezden aşağı. Bokken suburi'siyle aynı mekanik.", "en": "The main descending cut."}},
                    {"name": "Chiburi", "detail": {"tr": "Kanı silkme: büyük dairesel (o-chiburi) veya yana küçük (yoko chiburi). Acele edilmez — zanshin fazıdır.", "en": "Shaking the blood off — a zanshin phase, never rushed."}},
                    {"name": "Noto", "detail": {"tr": "Kılıfa koyuş: gözler rakipte, el kılıfın ağzını bulur. Yavaş noto, hızlı noto'dan zordur ve daha değerlidir.", "en": "Re-sheathing without looking; slow noto is the hard one."}},
                ],
            },
            {
                "group": {"tr": "Destek çalışmaları", "en": "Supporting drills"},
                "items": [
                    {"name": "Seiza / tate hiza kalkışları", "detail": {"tr": "Diz üstünden tek harekette kalkış; günde 10 tekrar dizleri katalara hazırlar.", "en": "Rising from seiza in one motion, 10 reps daily."}},
                    {"name": "Suburi (bokken)", "detail": {"tr": "Iaito yoksa kirioroshi'yi bokken ile çalış: 30 merkez, 20 kesa.", "en": "Cut mechanics with a bokken when no iaito is available."}},
                ],
            },
        ],
    },
    # ------------------------------------------------------------------ KARATE
    "karate": {
        "has_kata": True,
        "intro": {
            "tr": (
                "Karate kata açısından en zengin branştır; burada Shotokan "
                "müfredatı temel alındı (diğer stillerde isimler değişir: "
                "Heian = Pinan). Solo program iskeleti: kihon (temel duruş + "
                "teknik tekrarları) 15 dk, kata 10 dk, esneklik 5 dk. Kata "
                "öğrenme sırası: Taikyoku Shodan → Heian serisi (1-5) → "
                "Tekki Shodan. Her katayı önce sayarak (adım adım), sonra "
                "akışta, en son gözler kapalı çalış."
            ),
            "en": (
                "Karate is the richest kata tradition; this guide follows the "
                "Shotokan curriculum. Learning order: Taikyoku Shodan, the "
                "five Heian kata, then Tekki Shodan."
            ),
        },
        "kata": [
            {
                "name": "Taikyoku Shodan", "jp": "太極初段", "level": {"tr": "Giriş", "en": "Entry"},
                "diagram": "embusen-h",
                "summary": {
                    "tr": "İlk kata: yalnız gedan barai + oi tsuki, H şeklinde embusen (zemin deseni) üzerinde 20 hareket. Dönüşleri öğrenmenin en temiz yolu.",
                    "en": "First kata: only gedan barai and oi tsuki on an H-shaped embusen, 20 moves.",
                },
                "steps": {
                    "tr": [
                        "Yoi (hazır) — kuzeye bak",
                        "Sola dön (batı): gedan barai, zenkutsu dachi",
                        "İleri adım: oi tsuki (chudan)",
                        "180° dön (doğu): gedan barai",
                        "İleri adım: oi tsuki",
                        "Sola 90° (kuzey): gedan barai + 3 adım oi tsuki (sonuncusu kiai)",
                        "270° dön (batı): gedan barai + oi tsuki",
                        "180° (doğu): gedan barai + oi tsuki",
                        "Sola 90° (güney): gedan barai + 3 oi tsuki (kiai)",
                        "270° dön (batı) ve simetrik tekrar; başlangıç noktasında yame",
                    ],
                    "en": [
                        "Yoi (ready) — facing north",
                        "Turn left (west): gedan barai in zenkutsu dachi",
                        "Step forward: oi tsuki (chudan)",
                        "Turn 180° (east): gedan barai",
                        "Step forward: oi tsuki",
                        "90° left (north): gedan barai + three stepping punches (kiai on the third)",
                        "Turn 270° (west): gedan barai + oi tsuki",
                        "180° (east): gedan barai + oi tsuki",
                        "90° left (south): gedan barai + three punches (kiai)",
                        "Turn 270° (west), mirror the sequence; yame at the start point",
                    ],
                },
            },
            {"name": "Heian Shodan", "jp": "平安初段", "level": {"tr": "Başlangıç (9-8. kyu)", "en": "Beginner"},
             "diagram": "embusen-h",
             "summary": {"tr": "21 hareket: gedan barai, age uke, oi tsuki, shuto uke ve kokutsu dachi tanıtılır. Taikyoku'nun üstüne yalnızca birkaç yeni teknik koyar — geçiş yumuşaktır.", "en": "21 moves adding age uke, shuto uke and kokutsu dachi."}},
            {"name": "Heian Nidan", "jp": "平安二段", "level": {"tr": "Başlangıç (8-7. kyu)", "en": "Beginner"},
             "summary": {"tr": "26 hareket: haiwan uke, yoko geri + uraken kombinasyonu, mae geri ve nukite. Yan tekme dengesi bu katada kurulur.", "en": "26 moves introducing side kick + backfist and nukite."}},
            {"name": "Heian Sandan", "jp": "平安三段", "level": {"tr": "Orta (7-6. kyu)", "en": "Intermediate"},
             "summary": {"tr": "uchi uke çiftleri, kiba dachi'de dirsekler ve meşhur yavaş dönüşlü fumikomi bölümü.", "en": "20 moves: paired uchi uke, elbows in kiba dachi."}},
            {"name": "Heian Yondan", "jp": "平安四段", "level": {"tr": "Orta (6-5. kyu)", "en": "Intermediate"},
             "summary": {"tr": "27 hareket: kakiwake uke, mae geri-uraken hızlı kombinasyonu, hiza geri (diz). Serinin en atletik katası.", "en": "27 moves — the most athletic of the series."}},
            {"name": "Heian Godan", "jp": "平安五段", "level": {"tr": "Orta (5-4. kyu)", "en": "Intermediate"},
             "summary": {"tr": "mizu nagare kamae, sıçrama (tobi) ve zemin geçişi. Heian serisinin finali.", "en": "23 moves with the jump — the series finale."}},
            {"name": "Tekki Shodan", "jp": "鉄騎初段", "level": {"tr": "Orta-ileri (4-3. kyu)", "en": "Intermediate-advanced"},
             "diagram": "embusen-i",
             "summary": {"tr": "29 hareket, tamamı kiba dachi'de ve tek çizgi üzerinde (I embusen). Kalça gücü ve alt beden dayanıklılığı katası; dar alanda bile çalışılır.", "en": "29 moves entirely in horse stance on a single line — ideal for small spaces."}},
        ],
        "techniques": [
            {
                "group": {"tr": "Dachi (duruşlar)", "en": "Stances"},
                "items": [
                    {"name": "Zenkutsu dachi", "detail": {"tr": "Öne eğilimli duruş: ön diz bükük (dizden ayak ucu görünmez), arka bacak gergin, kalça öne dönük. Ağırlık %60 önde.", "en": "Front stance, 60% weight forward."}},
                    {"name": "Kokutsu dachi", "detail": {"tr": "Geriye eğilimli duruş: ağırlık %70 arkada, ayaklar L şeklinde. Shuto uke'nin evi.", "en": "Back stance, 70% rear — home of shuto uke."}},
                    {"name": "Kiba dachi", "detail": {"tr": "Binici duruşu: ayaklar paralel, iki omuz genişliği, dizler dışa. 1 dk sabit durabilmek ilk hedef.", "en": "Horse stance; hold one minute as a first goal."}},
                ],
            },
            {
                "group": {"tr": "Tsuki / Uchi (el teknikleri)", "en": "Punches & strikes"},
                "items": [
                    {"name": "Choku tsuki", "detail": {"tr": "Düz yumruk: yumruk kalçadan döner (hikite), son çeyrekte pronasyon. Karşı el kalçaya aynı hızla çekilir — güç oradadır.", "en": "Straight punch; power comes from the retracting hand."}},
                    {"name": "Oi tsuki", "detail": {"tr": "Adımlı yumruk: adımın ayak basışıyla yumruk aynı anda biter (kime).", "en": "Stepping punch — foot and fist finish together."}},
                    {"name": "Gyaku tsuki", "detail": {"tr": "Ters yumruk: ön bacak sabit, arka kalça döner. Karatenin en çok puan getiren tekniği.", "en": "Reverse punch driven by hip rotation."}},
                    {"name": "Uraken uchi", "detail": {"tr": "Ters yumruk sırtıyla kamçı vuruş; dirsek menteşe gibi.", "en": "Backfist snap from the elbow."}},
                    {"name": "Shuto uchi", "detail": {"tr": "El kılıcıyla vuruş (boyun hedefli); içten ve dıştan iki hattı da çalış.", "en": "Knife-hand strike, inside and outside paths."}},
                    {"name": "Empi (hiji ate)", "detail": {"tr": "Dirsek darbeleri: öne (mae), yukarı (tate), yana (yoko), geriye (ushiro). Yakın mesafenin kralı.", "en": "Elbow strikes in four directions."}},
                ],
            },
            {
                "group": {"tr": "Uke (bloklar)", "en": "Blocks"},
                "items": [
                    {"name": "Age uke", "detail": {"tr": "Yukarı blok: ön kol alnın bir yumruk üstünde, 45° açıyla. Bloklayan kol burnun önünden geçer.", "en": "Rising block at 45° above the forehead."}},
                    {"name": "Soto uke", "detail": {"tr": "Dıştan içe blok: yumruk kulak hizasından merkeze.", "en": "Outside-inward block."}},
                    {"name": "Uchi uke", "detail": {"tr": "İçten dışa blok: kol göğüs önünden dışarı açılır.", "en": "Inside-outward block."}},
                    {"name": "Gedan barai", "detail": {"tr": "Aşağı süpürme: yumruk karşı omuzdan diz üstüne. Her katanın ilk hareketi — en çok tekrar edeceğin blok.", "en": "Downward sweep — the most repeated block in kata."}},
                    {"name": "Shuto uke", "detail": {"tr": "El kılıcıyla blok, kokutsu dachi ile birlikte; karşı el göğüs önünde bekler (kakete).", "en": "Knife-hand block in back stance."}},
                ],
            },
            {
                "group": {"tr": "Geri (tekmeler)", "en": "Kicks"},
                "items": [
                    {"name": "Mae geri", "detail": {"tr": "Öne tekme: diz göğse, ayak topu (koshi) ile it, hızla geri çek. Çekiş vuruştan hızlı olmalı.", "en": "Front kick with the ball of the foot; retract faster than you kick."}},
                    {"name": "Mawashi geri", "detail": {"tr": "Dairesel tekme: diz hedefi gösterir, kalça döner, ayak sırtıyla temas. Önce belden aşağı hedefle başla.", "en": "Roundhouse — knee points, hip turns."}},
                    {"name": "Yoko geri (kekomi/keage)", "detail": {"tr": "Yan tekme: itişli (kekomi) ve kamçılı (keage) iki türü var. Ayak kılıcı (sokuto) ile temas.", "en": "Side kick, thrusting and snapping versions."}},
                    {"name": "Ushiro geri", "detail": {"tr": "Geri tekme: topukla, omuz üzerinden bakarak. Dönüşlü hali en güçlü tekmedir.", "en": "Back kick with the heel, looking over the shoulder."}},
                ],
            },
        ],
    },
    # ------------------------------------------------------------------ TAEKWONDO
    "taekwondo": {
        "has_kata": True,
        "intro": {
            "tr": (
                "Taekwondoda kata karşılığı poomsae'dir; Kukkiwon (WT) "
                "sisteminde renk kuşakları Taegeuk 1-8'i çalışır. Tekme "
                "sanatı olduğu için solo programın yarısı bacak hazırlığıdır: "
                "10 dk dinamik esneme + denge, 15 dk tekme tekrarları (her "
                "tekmeden 10'ar, iki bacak), 10 dk poomsae. Poomsae'yi aynada "
                "çalış; duruş yüksekliğin sabit kalmalı."
            ),
            "en": (
                "Taekwondo's forms are poomsae; the WT colour-belt set is "
                "Taegeuk 1-8. Half of solo practice is leg preparation."
            ),
        },
        "kata": [
            {"name": "Taegeuk 1 — Il Jang", "jp": "태극 1장", "level": {"tr": "Renk kuşağı", "en": "Colour belt"},
             "diagram": "embusen-i",
             "summary": {"tr": "arae makki, momtong jireugi, ap chagi. Yürüyüş duruşu (ap seogi) ağırlıklı — poomsae alfabesi.", "en": "18 moves: low block, middle punch, front kick."}},
            {"name": "Taegeuk 2 — I Jang", "jp": "태극 2장", "level": {"tr": "Renk kuşağı", "en": "Colour belt"},
             "summary": {"tr": "olgul (yüz) seviye teknikleri ve daha çok ap chagi eklenir.", "en": "Adds face-level techniques and more front kicks."}},
            {"name": "Taegeuk 3 — Sam Jang", "jp": "태극 3장", "level": {"tr": "Renk kuşağı", "en": "Colour belt"},
             "summary": {"tr": "sonnal (el kılıcı) blok/vuruş ve ardışık tekme-yumruk kombinasyonları.", "en": "Knife-hand techniques and kick-punch combos."}},
            {"name": "Taegeuk 4 — Sa Jang", "jp": "태극 4장", "level": {"tr": "Renk kuşağı", "en": "Colour belt"},
             "summary": {"tr": "yop chagi (yan tekme) ve dwit kubi (geri duruş) ağırlığı; zorluk sıçraması burada.", "en": "Side kicks and back stance — the difficulty jump."}},
            {"name": "Taegeuk 5 — O Jang", "jp": "태극 5장", "level": {"tr": "Renk kuşağı", "en": "Colour belt"},
             "summary": {"tr": "me jumeok (çekiç yumruk), palkup (dirsek) ve sıçramalı geçişler.", "en": "Hammer fist, elbows and jumping transitions."}},
            {"name": "Taegeuk 6 — Yuk Jang", "jp": "태극 6장", "level": {"tr": "Renk kuşağı", "en": "Colour belt"},
             "summary": {"tr": "dollyo chagi poomsae'ye girer; batangson (avuç dibi) bloklar.", "en": "Roundhouse kick enters the form."}},
            {"name": "Taegeuk 7 — Chil Jang", "jp": "태극 7장", "level": {"tr": "Renk kuşağı", "en": "Colour belt"},
             "summary": {"tr": "juchum seogi (binici duruş), mureup chigi (diz) ve makas blokları.", "en": "Horse stance, knee strike, scissor blocks."}},
            {"name": "Taegeuk 8 — Pal Jang", "jp": "태극 8장", "level": {"tr": "Renk kuşağı", "en": "Colour belt"},
             "summary": {"tr": "sıçramalı çift ap chagi (dubal dangsong). Siyah kuşak sınavının katası.", "en": "The black-belt exam form with the jumping double front kick."}},
            {"name": "Koryo ve ötesi", "jp": "고려", "level": {"tr": "1. dan+", "en": "1st dan+"},
             "summary": {"tr": "Siyah kuşak poomsae'leri: Koryo, Keumgang, Taebaek... Her dan derecesinin kendi formu vardır.", "en": "Black-belt poomsae: Koryo, Keumgang, Taebaek and beyond."}},
        ],
        "techniques": [
            {
                "group": {"tr": "Chagi (tekmeler)", "en": "Kicks"},
                "items": [
                    {"name": "Ap chagi", "detail": {"tr": "Öne tekme: diz göğse, ayak topuyla it. Tüm tekmelerin anasıdır — günde 20+20.", "en": "Front kick — the mother of all kicks."}},
                    {"name": "Dollyo chagi", "detail": {"tr": "Dairesel tekme: destek ayağı 90-180° döner, kalça devrilir, ayak sırtıyla vur. Taekwondonun imzası.", "en": "Roundhouse — taekwondo's signature."}},
                    {"name": "Yop chagi", "detail": {"tr": "Yan tekme: diz göğse çekilir, ayak kılıcıyla itiş; gövde hedefin tersine yatar.", "en": "Side kick with the foot blade."}},
                    {"name": "Dwit chagi", "detail": {"tr": "Geri tekme: topukla, düz hat üzerinde. Dönüşü kısa tut, bakış önce.", "en": "Back kick — straight line, look first."}},
                    {"name": "Naeryo chagi", "detail": {"tr": "Baltalama: bacak yukarı savrulur, topuk düşer. Hamstring esnekliği ister — esnemeden yapma.", "en": "Axe kick — requires hamstring flexibility."}},
                    {"name": "Ap hurigi / Bandal", "detail": {"tr": "Kamçı ve yarım ay tekmeleri: modern müsabakanın hızlı skorları.", "en": "Whip and crescent kicks of modern competition."}},
                ],
            },
            {
                "group": {"tr": "Jireugi / Chigi (el teknikleri)", "en": "Hand techniques"},
                "items": [
                    {"name": "Momtong jireugi", "detail": {"tr": "Gövdeye düz yumruk; karşı el kalçaya çekilir. Poomsae'nin en sık tekniği.", "en": "Middle punch — the most frequent poomsae technique."}},
                    {"name": "Sonnal chigi", "detail": {"tr": "El kılıcıyla vuruş: içe ve dışa. Sonnal mok chigi boyun hedeflidir.", "en": "Knife-hand strikes, inward and outward."}},
                    {"name": "Palkup chigi", "detail": {"tr": "Dirsek darbesi; Taegeuk 5'te tanışırsın.", "en": "Elbow strike (from Taegeuk 5)."}},
                ],
            },
            {
                "group": {"tr": "Makki (bloklar)", "en": "Blocks"},
                "items": [
                    {"name": "Arae makki", "detail": {"tr": "Aşağı blok: kol karşı omuzdan diz üstüne süpürür.", "en": "Low block."}},
                    {"name": "Momtong makki", "detail": {"tr": "Gövde bloğu: içe (an) ve dışa (bakat) iki yönü de çalış.", "en": "Middle block, inward and outward."}},
                    {"name": "Olgul makki", "detail": {"tr": "Yüz bloğu: ön kol alnın üstünde 45°.", "en": "High block."}},
                    {"name": "Sonnal makki", "detail": {"tr": "El kılıcıyla çift blok, dwit kubi ile birlikte.", "en": "Double knife-hand block in back stance."}},
                ],
            },
            {
                "group": {"tr": "Seogi (duruşlar)", "en": "Stances"},
                "items": [
                    {"name": "Ap seogi", "detail": {"tr": "Yürüyüş duruşu: doğal adım genişliği. Taegeuk 1-3'ün ana duruşu.", "en": "Walking stance."}},
                    {"name": "Ap kubi", "detail": {"tr": "Uzun ön duruş: karatedeki zenkutsu'nun karşılığı.", "en": "Long front stance."}},
                    {"name": "Dwit kubi", "detail": {"tr": "Geri duruş: ağırlık %70 arkada, ayaklar L.", "en": "Back stance, 70% rear."}},
                    {"name": "Juchum seogi", "detail": {"tr": "Binici duruş: Taegeuk 7 ve Keumgang'ın temeli.", "en": "Horse stance."}},
                ],
            },
        ],
    },
}


def get_guide(discipline: str) -> dict | None:
    return GUIDE.get(discipline)


# Haftalık başlangıç programları — sayfanın başındaki "sıfırdan başla" kutusu.
# Program tasarımı bize ait (pedagojik öneri); teknik içerik değildir.
PROGRAMS: dict = {
    "aikijo": {
        "tr": [
            "1-2. hafta: Tsuki serisi (suburi 1-5), her birinden 10 tekrar — günde 15 dk",
            "3-4. hafta: + Uchikomi serisi (6-10); tsuki artık ısınman",
            "5-6. hafta: + Katate serisi (11-13) ve 2 tur happo giri",
            "7-8. hafta: + Hasso gaeshi serisi (14-18); videodan 13'lü kataya başla",
            "9. hafta ve sonrası: 10 dk karışık suburi + 13'lü kata ×5; 31'liyi bölüm bölüm ekle",
            "Her seansın son 2 dakikası: serbest akış (jo spin / freestyle) — oyun kısmı, motivasyonu taşır",
        ],
        "en": [
            "Weeks 1-2: tsuki series (suburi 1-5), 10 reps each — 15 min daily",
            "Weeks 3-4: add the uchikomi series (6-10)",
            "Weeks 5-6: add the katate series (11-13) and happo giri",
            "Weeks 7-8: add hasso gaeshi (14-18); start the 13 kata from video",
            "Week 9+: 10 min mixed suburi + 13 kata ×5; add the 31 section by section",
        ],
    },
    "bokken": {
        "tr": [
            "1-4. hafta: sadece ichi no suburi — günde 30 kesiş, ayna karşısında",
            "5-8. hafta: videodan 2-4. suburi; her yeni suburi öncesi 10 ichi",
            "9-12. hafta: 5-7. suburi + 2 tur happo giri",
            "Sürekli: haftada bir gün sadece kamae çalış (5 duruş × 1'er dk sabit)",
        ],
        "en": [
            "Weeks 1-4: only ichi no suburi — 30 cuts daily, in front of a mirror",
            "Weeks 5-8: suburi 2-4 from video",
            "Weeks 9-12: suburi 5-7 plus happo giri",
            "Ongoing: one day a week only kamae (hold each stance 1 min)",
        ],
    },
    "aikido": {
        "tr": [
            "Her gün: 5 dk irimi-tenkan turu (20 dönüş) + 5 dk shikko",
            "Gün aşırı: 10 mae + 10 ushiro ukemi (yumuşak zeminde)",
            "Haftada 2: bokken/jo suburi (kılıç mekaniği aikido tekniklerinin temelidir)",
            "Haftada 1: ayna karşısında shomen/yokomen/tsuki formu — 10'ar tekrar",
        ],
        "en": [
            "Daily: 5 min irimi-tenkan (20 pivots) + 5 min shikko",
            "Every other day: 10 forward + 10 backward ukemi on soft ground",
            "Twice a week: bokken/jo suburi — sword mechanics feed the techniques",
        ],
    },
    "jodo": {
        "tr": [
            "1-4. hafta: honte uchi, gyakute uchi, hiki otoshi — 10'ar tekrar, günde 15 dk",
            "5-8. hafta: 12 kihonun tamamını sırayla 5'er tekrar",
            "9. haftadan sonra: kihon 10 dk + bildiğin kataların jo tarafı 2'şer kez (tandoku)",
            "Kural: yeni kata eklemeden önce içindeki kihonlar tek tek rahat çıkmalı",
        ],
        "en": [
            "Weeks 1-4: honte uchi, gyakute uchi, hiki otoshi — 10 reps each",
            "Weeks 5-8: all 12 kihon in order, 5 reps each",
            "Week 9+: 10 min kihon + the jo side of known kata twice each (tandoku)",
        ],
    },
    "jojutsu": {
        "tr": [
            "Temel program Jodo ile aynıdır: 12 kihonu kusursuzlaştır",
            "Koryu kataları öğretmensiz ÇALIŞMA; isimlerini ve senaryolarını öğren, video izle",
            "Haftada 1: Omote setinden bir katayı videodan analiz et (henüz yapmadan)",
        ],
        "en": [
            "The base program equals Jodo: perfect the 12 kihon",
            "Do not self-teach koryu kata; learn their names and watch, analyse one Omote kata weekly",
        ],
    },
    "kenjutsu": {
        "tr": [
            "Her gün: kiri oroshi 30, kesa giri 20+20 (iki taraf), tsuki 20",
            "Haftada 2: do giri 10+10 ve 5 kamae'de 1'er dk sabit duruş",
            "Haftada 1: ayna/videoyla form kontrolü — kesişin hattı düz mü?",
            "Okula bağlanana kadar okul katası taklit etme; kesiş kalitesine yatır",
        ],
        "en": [
            "Daily: 30 vertical cuts, 20+20 diagonal, 20 thrusts",
            "Twice a week: horizontal cuts and 1-min holds in the five kamae",
            "Weekly: check your line in a mirror or on video",
        ],
    },
    "kendo": {
        "tr": [
            "Her gün: 10 dk ashi sabaki (4 yöne suriashi turları)",
            "Her gün: 100 suburi — 30 joge, 30 shomen, 20 sayu men, 20 haya suburi",
            "Haftada 2: Nihon Kendo Kata'dan bildiğin formların iki tarafını da yavaş çalış",
            "Haftada 1: solo kirikaeshi (nefes + ritim) 5 set",
        ],
        "en": [
            "Daily: 10 min footwork + 100 suburi (30 joge, 30 shomen, 20 sayu men, 20 haya)",
            "Twice a week: both sides of the kata you know, slowly",
            "Weekly: five sets of solo kirikaeshi",
        ],
    },
    "iaido": {
        "tr": [
            "1-8. hafta: sadece Mae — her seans 10 tekrar, dört fazı ayrı ayrı da çalış",
            "9-16. hafta: + Ushiro ve Uke Nagashi; Mae hâlâ her seansın ilk katası",
            "Sonrası: her seans 3 kata × 5 tekrar; ayda bir 12'sini sırayla geç",
            "Her seans önce: 10 seiza kalkışı + 20 kirioroshi (bokken ile olur)",
        ],
        "en": [
            "Weeks 1-8: only Mae — 10 reps per session, drill the four phases separately",
            "Weeks 9-16: add Ushiro and Uke Nagashi; Mae still opens every session",
            "Later: 3 kata × 5 reps per session; run all 12 monthly",
        ],
    },
    "karate": {
        "tr": [
            "Her gün 15 dk kihon: zenkutsu'da oi/gyaku tsuki 20'şer, age/soto/gedan blok 10'ar, mae geri 20",
            "1-4. hafta: Taikyoku Shodan'ı say-adımla ezberle (aşağıdaki adımlar)",
            "5. haftadan sonra: her ay bir Heian katası; eskiler haftada bir tekrar",
            "Haftada 1: kiba dachi sabit duruş (1 dk hedef) + esneklik 10 dk",
        ],
        "en": [
            "Daily 15 min kihon: punches, blocks and front kicks in stance",
            "Weeks 1-4: memorise Taikyoku Shodan step by step",
            "Week 5+: one Heian kata per month, older ones weekly",
        ],
    },
    "taekwondo": {
        "tr": [
            "Her gün: 10 dk dinamik esneme + denge (tek ayak, gözler kapalı 30 sn)",
            "Her gün: ap chagi 20+20, dollyo 15+15, yop 10+10 (iki bacak)",
            "1-6. hafta: Taegeuk 1 — aynada, duruş yüksekliği sabit",
            "Sonrası: her 6-8 haftada bir sonraki Taegeuk; eskiler haftada bir",
        ],
        "en": [
            "Daily: 10 min dynamic stretching + balance work",
            "Daily kicks both legs: 20 front, 15 roundhouse, 10 side",
            "Weeks 1-6: Taegeuk 1 in the mirror at constant stance height",
            "Then: the next Taegeuk every 6-8 weeks, older ones weekly",
        ],
    },
}

for _d, _p in PROGRAMS.items():
    GUIDE[_d]["program"] = _p
