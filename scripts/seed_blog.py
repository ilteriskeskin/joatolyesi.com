"""Başlangıç blog içeriği: 3 örnek kullanıcı + 2 yazı ("Jo Nedir?",
"Dachi Pozisyonları"). Idempotent — kullanıcı adı varsa atlar.

Çalıştırma:  docker compose exec app python scripts/seed_blog.py
"""

import asyncio
import secrets

from sqlalchemy import select

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
]

POSTS = [
    {
        "username": "kenshin-yolda",
        "title": "Jo Nedir? Dört Şeftali Ağacından Dojoya",
        "discipline": "aikijo",
        "body": """Jo, yaklaşık 128 cm uzunluğunda, düz ve tırtıksız bir Japon sopasıdır. Kılıç kadar karizmatik görünmeyebilir; ama elinize aldığınız anda anlarsınız: iki ucu da yaşayan, menzili sürekli değişen, saklayacak hiçbir şeyi olmayan bir silahtır.

## Kısa tarih

Jo'nun en bilinen hikâyesi 17. yüzyıla dayanır. Rivayete göre samuray Muso Gonnosuke, efsanevi kılıç ustası Miyamoto Musashi'ye yenildikten sonra inzivaya çekilir, daha kısa ve daha çevik bir sopa üzerine çalışır ve Shinto Muso-ryu jojutsu'yu kurar. Bugün jo iki büyük gelenekte yaşar:

- **Jodo / jojutsu:** kılıca karşı jo — Shinto Muso-ryu ve ZNKR'nin standartlaştırdığı Seitei Jodo
- **Aiki-jo:** aikidonun kurucusu Morihei Ueshiba'nın geliştirdiği, Iwama müfredatıyla (20 suburi, 13'lü ve 31'li kata) yayılan çalışma

## Neden jo ile başlamalı?

Benim için cevap basit: **jo affedicidir ama yalan söylemez.** Kılıçta kesişin doğru olup olmadığını başta göremezsiniz; jo'da dengesiz bir tsuki attığınızda sopa elinizde kımıldar, hemen söyler.

> Jo, vücudunuzun iki tarafını da eşit çalıştıran nadir silahlardandır — sol elinizle de vurursunuz, sağ elinizle de.

## İlk jo'nuzu seçerken

- **Uzunluk:** klasik ölçü 128 cm (4 shaku 2 sun 1 bu). Boyunuz kısaysa koltuk altı hizası da kabul görür.
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
                email=f"{spec['username']}@demo.joatolyesi.com",
                password_hash=await hash_password(secrets.token_urlsafe(24)),  # giriş yapılamaz
                lang="tr",
                username=spec["username"],
                display_name=spec["display_name"],
                bio=spec["bio"],
                discipline=spec["discipline"],
                is_public=True,
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
            db.add(
                Post(
                    user_id=users[spec["username"]].id,
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
