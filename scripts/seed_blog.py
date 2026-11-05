"""Başlangıç blog içeriği: örnek kullanıcılar (girişi olmayan, rastgele
şifreli, gizli profiller; yazılar sitede "Joryu Ekibi" olarak görünür) + branş başına bir yazı. Idempotent — kullanıcı adı
veya yazı başlığı zaten varsa atlar.

Çalıştırma:  docker compose exec app python scripts/seed_blog.py
"""

import asyncio
import secrets

from sqlalchemy import select

from app.constants import DEMO_EMAIL_SUFFIX
from app.db import async_session
from app.models import Post, User
from app.routers.blog import _slugify
from app.security import hash_password

USERS = [
    {"username": "kenshin-yolda", "display_name": "Kenshin", "discipline": "aikijo",
     "bio": "İki yıldır her sabah jo. Bahçede, yağmurda, otel odasında."},
    {"username": "sabah-keiko", "display_name": "Deniz", "discipline": "karate",
     "bio": "Shotokan. Kata'nın tekrar sayısıyla değil, niyetiyle ilgileniyorum."},
    {"username": "tatami-notlari", "display_name": "Tatami Notları", "discipline": "iaido",
     "bio": "Iaido günlüğü. Yavaş olan hızlıdır."},
    {"username": "suburi-defteri", "display_name": "Suburi Defteri", "discipline": "bokken",
     "bio": "Aiki-ken çalışıyorum. Yedi suburi, bin tekrar."},
    {"username": "poomsae-calismasi", "display_name": "Poomsae Çalışması", "discipline": "taekwondo",
     "bio": "Taegeuk'ten siyah kuşak poomsae'lerine giden yolun günlüğü."},
    {"username": "aksam-keiko", "display_name": "Kaan", "discipline": "jodo",
     "bio": "ZNKR Seitei Jodo çalışıyorum. Kılıca karşı sopa — hep kılıç kazanır, ta ki kazanmayana kadar."},
    {"username": "yalniz-kilic", "display_name": "Ege", "discipline": "kenjutsu",
     "bio": "Koryu kenjutsu meraklısı. Kata tek başına da çalışılır, rakip her zaman hayalidir."},
]

POSTS = [
    {
        "username": "kenshin-yolda",
        "title": "Jo Nedir? Dört Şeftali Ağacından Dojoya",
        "discipline": "aikijo",
        "body": """Jo, yaklaşık 128 cm uzunluğunda, düz ve tırtıksız bir Japon sopasıdır. Kılıç kadar karizmatik görünmeyebilir; ama elinize aldığınız anda anlarsınız: iki ucu da yaşayan, menzili sürekli değişen, saklayacak hiçbir şeyi olmayan bir silahtır.

## Kısa tarih

Jo'nun en bilinen hikâyesi 17. yüzyılın başına dayanır. Rivayete göre samuray Muso Gonnosuke, efsanevi kılıç ustası Miyamoto Musashi'ye yenildikten sonra inzivaya çekilir, yeni bir sopa tekniği geliştirir ve Shinto Muso-ryu jojutsu'yu kurar. Okulun kendi aktarımına göre Gonnosuke daha sonra Musashi'yle yeniden karşılaşıp onu yenmiştir; bu ikinci karşılaşma okul dışındaki kaynaklarla doğrulanamaz. Bugün jo iki büyük gelenekte yaşar:

- **Jodo / jojutsu:** kılıca karşı jo — Shinto Muso-ryu ve ZNKR'nin standartlaştırdığı Seitei Jodo
- **Aiki-jo:** aikidonun kurucusu Morihei Ueshiba'nın geliştirdiği, Iwama müfredatıyla (20 suburi, 13'lü ve 31'li kata) yayılan çalışma

## Neden jo ile başlamalı?

Jo ile başlamanın bir gerekçesi şu görüşle özetlenebilir: **jo affedicidir ama yalan söylemez.** Bu bakışa göre kılıçta kesişin doğru olup olmadığı başlangıçta her zaman kolay fark edilmez; jo'da ise dengesiz bir tsuki çoğu zaman sopanın elinizde kımıldamasıyla kendini belli eder.

> Jo, özellikle jododa, vücudun iki yanında da kullanılır: temel teknikler hem sağdan hem soldan çalışılır, eller yer değiştirir. Kılıç çalışmasında bu kadar iki taraflı bir kullanım daha az görülür.

## İlk jo'nuzu seçerken

- **Uzunluk:** geleneksel ölçü yaklaşık 128 cm (4 shaku 2 sun 1 bu). Boyunuza uygun ölçü dojodan dojoya değişebilir; satın almadan önce hocanıza danışın.
- **Ağaç:** Japonya'da beyaz meşe (shiro kashi) standarttır. Türkiye'de dişbudak veya gürgen iyi iş görür; budaksız ve düz olsun.
- **Çap:** 24-26 mm arası. İnce jo hızlıdır ama kumijo'da (eşli çalışma) darbe yer.

Başlamak için dojo bile şart değil: iki metre boşluk, bir jo ve günde on beş dakika. Gerisi tekrar.""",
    },
    {
        "username": "sabah-keiko",
        "title": "Dachi: Karatenin Temeli Ayaklarda Kurulur",
        "discipline": "karate",
        "body": """Yeni başlayanlar yumruğa bakar, ustalar ayaklara. Dachi (duruş), karatede tekniğin taşıyıcı kolonudur: duruş yanlışsa yumruk ne kadar hızlı olursa olsun güç yere kaçar.

## Üç temel dachi

**Zenkutsu dachi (öne eğilimli duruş).** Ön diz bükük, arka bacak gergin, ağırlığın kabaca %60'ı önde. Kontrol: dizinizin üstünden baktığınızda ayak parmaklarınızı görmemelisiniz. Oi tsuki ve gyaku tsuki'nin evi burasıdır — kalça dönüşü bu duruştan güç alır.

**Kokutsu dachi (geriye eğilimli duruş).** Ağırlığın ~%70'i arkada, ayaklar L biçiminde. Savunmanın duruşudur; shuto uke ile birlikte öğrenilir. En sık hata: arka dizin içe çökmesi. Diz, ayak ucuyla aynı yöne bakmalı.

**Kiba dachi (binici duruş).** Ayaklar paralel, iki omuz genişliği, dizler dışa itilmiş, sırt dik. Tekki katalarının tamamı bu duruşta yapılır. İlk hedef: bir dakika kımıldamadan durabilmek. Bacaklarınız titriyorsa doğru yapıyorsunuz demektir.

## Çalışma önerisi

1. Ayna karşısında her duruşta 30'ar saniye — haftada üç gün
2. Duruşlar arası geçiş: zenkutsu → kokutsu → kiba, adım almadan kalça dönüşüyle
3. Ayda bir kez telefonla video çekip ilk ayınızla kıyaslayın

> Duruş çalışması sıkıcıdır. Sıkıcı olduğu için de çoğu kişi atlar; aradaki fark tam olarak burada açılır.

Not: isimler stiller arasında değişebilir (ör. taekwondoda ap kubi, juchum seogi). Prensip aynıdır: kökü sağlam olmayan ağaç rüzgârda eğilir.""",
    },
    {
        "username": "suburi-defteri",
        "title": "Aiki-ken'e Başlarken: Yedi Suburi Neden Bu Kadar Önemli?",
        "discipline": "bokken",
        "body": """Aiki-ken'e yeni başlayanlar genellikle kumitachi (eşli form) çalışmaya can atar — kılıç kılıca karşı gelince heyecan orada. Ama Saito yönteminin temeli yedi suburi'dir; kumitachi'nin her hareketi bu yedisinin bir kombinasyonundan ibarettir.

## Yedi suburi, kısaca

1. **Ikkajo no suburi** — dikey kesiş, shomen'e iniş
2. **Nikajo no suburi** — kesiş + kesiş (iki vuruşluk zincir)
3. **Sankajo no suburi** — üç kesişlik zincir
4. **Shihogiri** — dört yöne kesiş
5. **Gyaku kesa giri** — ters çapraz kesiş
6. **Zengo giri** — öne-arkaya kesiş
7. **Sonkyo giri** — çömelerek kesiş

## Neden tek başına yeterli değil, ama şart

Suburi'yi tek başına bin kez tekrar etseniz bile kumitachi'deki mesafe ve zamanlama hissini vermez — o ancak eşli çalışmada gelir. Ama suburi olmadan kumitachi'ye girerseniz kesişiniz güvenilmez olur: mesafe doğru olsa bile kılıç hattı kayar.

> Suburi, kılıcın "dilini" öğrendiğiniz yerdir. Kumitachi, o dille konuştuğunuz yer.

## Solo çalışma önerisi

- Her suburi'yi günde 10 tekrar, yavaş ve kontrollü — hız sonra gelir
- Aynadan değil, gölgenizden çalışın: kesişin düz olup olmadığını gölge söyler
- Shihogiri'de dönüşler arası duraklamayın; dört kesiş tek nefeste bitmeli

Kılıcınız yoksa endişelenmeyin — düzgün bir sopa veya süpürge sapı bile mesafe ve kalça dönüşünü öğretir. Gerçek kılıcın ağırlığı ancak temel oturunca fark yaratır.""",
    },
    {
        "username": "poomsae-calismasi",
        "title": "Poomsae Çalışırken Gözden Kaçan Üç Detay",
        "discipline": "taekwondo",
        "body": """Taegeuk serisini ezberleyen çoğu kişi hareket sırasını doğru bilir ama üç detayı gözden kaçırır — ve bu üçü, bir poomsae'yi "doğru" ile "iyi" arasında ayıran şeydir.

## 1. Duraklama noktaları (jumbi ve son duruş)

Her poomsae hazır duruşla (jumbi seogi) başlar ve biter; aradaki geçiş çoğu kişide aceleyle olur. Oysa jumbi'de bir nefeslik durmak, hakemin (ya da izleyicinin) gördüğü ilk ve son şeydir. Taegeuk'ün başında ve sonunda tam iki saniye kıpırdamadan durun.

## 2. Nefes ve kihap zamanlaması

Kihap (haykırış), rastgele bir hareketle değil, poomsae'nin "vurgu" noktasıyla eşleşir — genelde en güçlü tekniğin geldiği an. Taegeuk Sam-jang'da örneğin çift yumruk anında gelir. Nefesinizi o ana kadar tutmak, gücü orada patlatmanızı sağlar.

## 3. Sigi (duruş) geçişleri tekme kadar önemli

Yeni başlayanlar tekmeye odaklanır, ama tekmeden sonraki inişte duruş (ap seogi, ap kubi seogi) tam oturmazsa bütün poomsae sallantılı görünür. Her tekmeden sonra ayağınızı doğru duruşa **tam** yerleştirin — bir sonraki tekniğe erken geçmeyin.

## Solo çalışma önerisi

- Aynı poomsae'yi üç kez art arda çalışın: birinci hız için, ikinci duruş netliği için, üçüncü kihap zamanlaması için
- Video çekip jumbi'deki duraklamanızı sayaçla ölçün — çoğu kişi bir saniyeden az durduğunu görünce şaşırır

> Poomsae bir koreografi değildir; her duruşun bir savunma/saldırı anlamı vardır. Anlamını bilmediğiniz bir hareketi hızlandırmak, sadece hatayı hızlandırmaktır.""",
    },
    {
        "username": "tatami-notlari",
        "title": "Iaido'da Nukitsuke: Hız Yanılsaması",
        "discipline": "iaido",
        "body": """Iaido'ya yeni başlayanların neredeyse hepsi aynı hatayı yapar: nukitsuke'yi (kını çekip kesme) hızlandırmaya çalışmak. Oysa ZNKR Seitei Iai'nin öğrettiği şey tam tersi bir sıra: önce doğru, sonra hızlı.

## Nukitsuke'nin dört bileşeni

Nukitsuke tek bir hareket gibi görünür ama aslında dört şeyin aynı anda uyumlu olmasını gerektirir:

1. **Saya biki** — kının kesişe karşı geri çekilmesi (kılıcı sıyırmak, itmek değil)
2. **Kılıcın açısı** — ağız kenarının (ha) doğru açıda hedefe gelmesi
3. **Kalça dönüşü** — gücün bilekten değil kalçadan gelmesi
4. **Göz hizası** — kesiş bitmeden önce hedefe kilitlenmiş bakış

Bu dördü aynı anda oturmadan hız eklemek, sadece düzensizliği hızlandırır — tecrübeli bir gözün en çok yakaladığı hata budur.

## Neden "yavaş olan hızlıdır"

Iaido'da gerçek hedef, düşmanı kesmeden önce görmeden hareket etmemektir (metsuke). Kesiş ne kadar keskin görünürse görünsün, saya biki geç kalmışsa veya açı bozuksa, gerçek bir kılıçla o kesiş işe yaramaz. Yavaş çalışıp dört bileşeni ayrı ayrı doğrulamak, hız gelince otomatik olarak doğru kalmanızı sağlar.

## Solo çalışma önerisi

- Nukitsuke'yi üçe bölerek çalışın: saya biki tek başına, açı tek başına, sonra ikisini birleştirip yavaş tam hareket
- Ayna karşısında kının ağzının (koiguchi) kesiş sırasında ne kadar döndüğünü izleyin — gereğinden fazla dönüyorsa kalçanız erken açılıyor demektir
- Chiburi ve noto'yu (kılıcı silme ve kına sokma) nukitsuke kadar ciddiye alın; iaido'da form, kesişle bitmez.

> Bir kılıç ustası kesişin hızından değil, kesişin gerekmediği anı bilmesinden tanınır.""",
    },
    {
        "username": "joryu",
        "title": "Aiki-jo'nun 20 Suburi'si: Aikidoyu Sopayla Anlamak",
        "discipline": "aikijo",
        "body": """Aiki-jo'ya yeni başlayanlar genelde aynı soruyu sorar: "Bu aikido mu, jodo mu?" Cevap ikisi de değil, ikisinin kesişimi. Aikido'nun kurucusu Morihei Ueshiba, kendi prensiplerini (irimi, tenkan, kokyu) bir sopa üzerinden somutlaştırmak için jo çalışmasını geliştirdi; öğrencisi Morihiro Saito bu çalışmayı Iwama'da sistematikleştirip bugün dünyada en yaygın öğretilen aiki-jo müfredatı hâline getirdi. Bu müfredatın omurgası 20 suburi'dir.

## Suburi neden "sopa sallamak" değildir

Yeni başlayanlar suburi'yi ısınma hareketi sanır. Oysa her suburi, boş elle yapılan bir aikido tekniğinin jo üzerinden tekrarıdır: tsuki (itiş) irimi'yi, uchi (vuruş) kesme hattını, kaeshi (dönüş) tenkan'ı öğretir. Jo elinizde olduğu için hata gizlenemez — dengesiz bir adım attığınızda sopanın ucu titrer, kalçanız geç döndüğünde vuruş hattı kayar. Boş elle fark etmeyeceğiniz bir dengesizliği jo hemen ele verir.

> Jo, aikidoyu büyüten bir mercek gibidir: gövdenizin yaptığı her küçük hatayı sopanın ucunda büyütüp size gösterir.

## 20'nin mantığı

Saito'nun sistemleştirdiği 20 suburi, tek tek ezberlenecek 20 ayrı hareket değil, birbirinin üzerine inşa edilen gruplardır: düz itişler (tsuki), kesme vuruşları (uchi), bunların geri dönüşleri (kaeshi) ve daha ileri kombinasyonlar. Sıralama bilinçlidir — her yeni suburi, bir öncekinin gövde mekaniğini bir adım ileri taşır. Bu yüzden 14. suburi'yi 3. suburi'yi atlayarak öğrenmeye çalışmak, temelsiz inşaata benzer.

Tam sıralama ve isimler öğrettiğiniz dojoya ve hangi çizgiyi (Iwama, Ki Society gibi) takip ettiğinize göre küçük farklar gösterebilir — bu yüzden burada tek tek listelemek yerine kendi hocanızın veya uygulamadaki kata kütüphanesinin verdiği sırayı esas almanızı öneririz.

## Solo çalışma önerisi

1. İlk beş suburi'yi bir ay boyunca günde beşer tekrar çalışın — hız değil, gövde-kalça-jo uyumu hedef
2. Her suburi'nin sonunda bir saniye durun (zanshin): jo'nun ucu titriyorsa denge tam oturmamış demektir
3. Ayda bir video çekip bir önceki ayla karşılaştırın; aiki-jo'da ilerleme haftalık değil aylık görülür

Dojoya gitmeden, sadece iki metrekarelik bir alanda bile bu 20 suburi'nin ilk birkaçıyla başlamak, aikidonun gövde mantığını anlamanın en doğrudan yollarından biridir.""",
    },
    {
        "username": "aksam-keiko",
        "title": "Jodo ve Jojutsu: Aynı Silah, İki Farklı Yol",
        "discipline": "jodo",
        "body": """Jojutsu'nun en bilinen geleneği, okulun kendi aktarımına göre 17. yüzyıl başında samuray Muso Gonnosuke'nin kurduğu Shinto Muso-ryu'dur — bu hikâye bu blogda daha önce de anlatıldı. Ama az bilinen şey şu: bugün "jodo" adıyla dünyada öğretilen şeyin büyük kısmı, o eski okulun kendisi değil, ondan 20. yüzyılda türetilmiş standart bir müfredat.

## Koryu'dan gendai'ye

Shinto Muso-ryu, klasik anlamda bir **koryu**'dur (eski okul): yüzlerce yıldır aynı hoca-öğrenci zinciriyle, değişmeden aktarılan bir gelenek. 1968'de Japonya Kendo Federasyonu (ZNKR), bu geleneğin içinden on iki temel kata seçip standartlaştırarak **Seitei Jodo**'yu oluşturdu — amaç, farklı dojolarda öğrenen kendocuların ortak bir dille jo çalışabilmesiydi. Bugün dünya çapında öğretilen jodonun büyük kısmı bu Seitei müfredatıdır; orijinal Shinto Muso-ryu'nun tamamı (60'tan fazla kata) hâlâ ayrı, daha derin bir çizgi olarak yaşıyor.

## Jo neden hep kazanır

Jodo kata'larının en çarpıcı özelliği şudur: neredeyse tüm kata'larda jo tarafı kazanır, kılıç tarafı kaybeder. Bu tesadüf değil — tarihsel olarak jonun kılıca karşı üstünlüğünü öğretmek üzere tasarlanmış bir sistem. Ama bu, kılıcın zayıf olduğu anlamına gelmez: kata'lardaki her hareket, jo'nun mesafe (maai) ve zamanlama avantajını nasıl kullandığını gösterir. Kılıç menzilde geç kalırsa veya açı hatası yaparsa, daha kısa ama daha çevik olan jo araya girer.

> Jodo'da kazanmak hız meselesi değildir — kılıcın açılmasını beklemek ve o an araya girmek meselesidir.

## Solo çalışma önerisi

- Kata'ları eşsiz çalışamıyorsanız bile, jo tarafının tek başına yaptığı adım-kalça-jo koordinasyonunu (kata'nın "iskeleti") tek başına tekrar edin
- Suburi'lerde açının netliğine odaklanın: jo'nun ucu hedefe tam kilitlenmeden vuruş bitmemelidir
- Seitei'nin on iki kata'sını sırayla değil, hangi temel prensibi öğrettiğine göre gruplandırıp çalışmak (tsuki grubu, uchi grubu gibi) ilerlemeyi hızlandırır

Kılıç ortağınız olmasa da, jo'nun tek başına attığı her adımda o hayali kılıcın nerede olduğunu hayal etmek — jodoyu koreografiden çalışan bir sisteme çevirir.""",
    },
    {
        "username": "yalniz-kilic",
        "title": "Kenjutsu Nedir, Kendo'dan Farkı Ne?",
        "discipline": "kenjutsu",
        "body": """"Kenjutsu mu çalışıyorsun, kendo mu?" — bu soruyu duymayan kenjutsu pratisyeni yoktur. İkisi de kılıç sanatı, ikisi de Japon kökenli, ama amaçları ve araçları kökten farklı.

## İki farklı hedef

**Kendo**, 20. yüzyılda spor olarak standartlaştırılmış bir disiplindir: bambu kılıç (shinai), koruyucu ekipman (bogu), sayılan vuruşlar ve karşılıklı serbest çalışma (jigeiko) üzerine kuruludur. Amaç, güvenli bir çerçevede rakibi "yenmek".

**Kenjutsu** ise Edo öncesi dönemden kalma **koryu** okullarının (Itto-ryu, Yagyu Shinkage-ryu, Katori Shinto-ryu gibi onlarca farklı gelenek) genel adıdır — gerçek savaş alanı için geliştirilmiş, kılıcın (bokken veya gerçek kılıç) doğrudan kullanıldığı, çoğunlukla önceden belirlenmiş kata'lar üzerinden aktarılan bir sistemdir. Serbest dövüş neredeyse hiç yoktur; her hareketin bir öncekiyle ve sonrakiyle kesin bir ilişkisi vardır.

## Neden kata, serbest çalışma değil

Gerçek bir kılıçla (veya onun ağırlığını taklit eden bir bokkenle) serbest dövüş yapmak güvenli değildir — bu yüzden kenjutsu, bilgiyi kata aracılığıyla aktarır. Kata, ezberlenmiş bir koreografi gibi görünse de aslında iki tarafın (kılıç tutan taraflardan biri genelde "kazanan" rolündedir) belirli bir mesafe, zamanlama ve niyet senaryosunu güvenli bir çerçevede tekrar tekrar çalışmasıdır. Tekrar sayısı arttıkça, kata'nın "koreografi" hissi kaybolur ve gerçek bir karşılaşmanın refleksine dönüşür.

> Kenjutsu'da rakip çoğu zaman hayalidir — ama niyetiniz gerçek olmalı. Sahte bir kesiş, kata'yı da sahteleştirir.

## Solo çalışma önerisi

- Suburi (tek başına kesiş tekrarı) kenjutsu'nun temelidir: her kesişte maai (mesafe) hayal edin — hayali rakip her zaman doğru mesafede olmalı
- Zanshin'i (kesiş sonrası tetikte kalma duruşu) ihmal etmeyin; kesiş bitince gevşemek, koryu geleneklerinde en sık eleştirilen hatadır
- Kata'nın adımlarını hızlandırmadan önce, her adımın "neden" o yönde olduğunu (hangi saldırıya karşılık geldiğini) anlamaya çalışın — anlamadan hızlandırılan kata, sadece hatayı hızlandırır

Bir dojo veya eğitmen bulmak kenjutsu için özellikle önemlidir — çoğu koryu, kata'ların doğru aktarımı için canlı bir öğretmen ister. Ama temel suburi ve duruş çalışması, bir bokken ve iki metrekarelik bir alanla her gün tek başına da ilerletilebilir.""",
    },
]


async def main() -> None:
    async with async_session() as db:
        users: dict[str, User] = {}
        for spec in USERS:
            existing = (
                await db.execute(select(User).where(User.username == spec["username"]))
            ).scalar_one_or_none()
            if existing:
                users[spec["username"]] = existing
                print(f"var: {spec['username']}")
                continue
            user = User(
                email=f"{spec['username']}{DEMO_EMAIL_SUFFIX}",
                password_hash=await hash_password(secrets.token_urlsafe(24)),  # giriş yapılamaz
                lang="tr",
                username=spec["username"],
                display_name=spec["display_name"],
                bio=spec["bio"],
                discipline=spec["discipline"],
                is_public=False,  # yazı sahibi (FK) olarak gerekli; kamuya açık gösterilmez
                referral_code=secrets.token_hex(5),
            )
            db.add(user)
            await db.flush()
            users[spec["username"]] = user
            print(f"eklendi: {spec['username']}")

        for spec in POSTS:
            existing = (
                await db.execute(select(Post.id).where(Post.title == spec["title"]))
            ).scalar_one_or_none()
            if existing:
                print(f"yazı var: {spec['title']}")
                continue
            author = users.get(spec["username"])
            if author is None:
                # Bu yazının yazarı USERS listesinde değil (ör. gerçek sahip
                # hesabı "joryu") — kendi kaydını yapmış mı diye DB'den bak.
                author = (
                    await db.execute(select(User).where(User.username == spec["username"]))
                ).scalar_one_or_none()
            if author is None:
                print(f"atlandı (kullanıcı '{spec['username']}' henüz kayıtlı değil): {spec['title']}")
                continue
            db.add(
                Post(
                    user_id=author.id,
                    slug=_slugify(spec["title"]),
                    title=spec["title"],
                    body=spec["body"],
                    discipline=spec["discipline"],
                )
            )
            print(f"yazı eklendi: {spec['title']}")
        await db.commit()


if __name__ == "__main__":
    asyncio.run(main())
