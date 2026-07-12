# Waitlist Büyütme Stratejisi

Joryu şu an `WAITLIST_ONLY=true` modunda: joatolyesi.com'a giren herkes
sadece landing sayfasını (mail toplama formu) görür — başka hiçbir route
(login, guide, blog, kata...) dışarıya açık değil. Bu doküman, o tek
sayfaya trafik çekip mail listesini büyütmenin yollarını anlatır.

## 1. Kanal takibi (altyapı zaten hazır)

Her waitlist kaydı `source` alanına düşer. Kanal bazlı linkler:

| Platform | Link |
|---|---|
| Instagram bio | `https://joatolyesi.com/?src=ig` |
| Instagram Story | `https://joatolyesi.com/?src=igs` |
| YouTube açıklama | `https://joatolyesi.com/?src=yt` |
| TikTok bio | `https://joatolyesi.com/?src=tt` |
| LinkedIn | `https://joatolyesi.com/?src=li` |
| Twitter/X | `https://joatolyesi.com/?src=tw` |

Hangi kanal dönüştürüyor: `https://joatolyesi.com/admin/waitlist?token=<ADMIN_TOKEN>`
CSV'sinin `source` sütunundan. Bütçe/zaman en çok dönüşen kanala gitmeli.

## 2. İçerik taktikleri (kod gerekmez, bugün başlanabilir)

- **Kurucu hikâyesi:** 290+ günlük kesintisiz jo pratiği landing'de zaten
  yazıyor. Bunu bir reels/video'ya çevirip "bu yüzden yaptım" anlatısıyla
  paylaşmak, soğuk bir ürün duyurusundan çok daha güçlü dönüşüm sağlar.
  Otantik kurucu hikâyesi = en ucuz güven inşası.
- **Sosyal kanıt sayacı:** Haftalık "şu ana kadar X kişi bekleme listesinde"
  paylaşımı (Story). Sayı arttıkça FOMO artar — CSV'den kaç kişi olduğunu
  her hafta kontrol et.
- **Yorum/DM tetikleyicisi:** Reels altına doğrudan link koymak yerine
  "linki istersen DM at" / "yorum yaz, link gelsin" — algoritma linksiz
  gönderiyi daha çok gösteriyor, otomasyon (Manychat vb.) linki DM'den yollar.
- **Branş-özel içerik:** Farklı branşlardan (aikido, karate, kendo...)
  kısa "bunu bilmiyordun" videoları + altına genel waitlist linki. Rehber
  içeriği (`app/guide_content.py`) zaten hazır kaynak — oradan kesitler
  paylaşılabilir (lansmandan önce rehber sayfası kapalı olsa da metni
  kullanmak serbest).
- **Karşılaştırmalı anlatı:** "Dojo haftada 2 gün açık, gelişim kalan 5
  günde oluyor" mesajı zaten landing'in ana vaadi — bunu direkt alıntı
  olarak paylaşmak tutarlılığı korur.

## 3. Referans linki (uygulamada, bu turda eklendi)

Waitlist'e katılan herkes artık kendine özel bir davet linki alıyor ve
"sırada kaçıncı olduğunu" görüyor. Klasik waitlist büyütme mekaniği
(Superhuman, Robinhood): sıra numarası + paylaşılabilir link, insanları
arkadaşlarını davet etmeye iter çünkü kendi konumunu iyileştirebileceğini
düşünür (şu an sırayı fiilen değiştirmiyor, ileride "3 davet = 10 sıra
yukarı" gibi bir ödül eklenebilir — bkz. TODO).

Kayıt sonrası ekranda:
- "Listede X. kişisin"
- Kendi referans linki: `joatolyesi.com/?ref=<kod>`
- Link paylaşıldığında ve biri o linkten katıldığında `referred_by`
  alanına düşer — CSV'de kim kimi getirdi görülebilir.

## 4. Ölçüm

Lansman kapısı (BRIEF.md'de zaten var): landing 2 hafta yayında,
**100+ e-posta → uygulama lansmanı**. Bu sayıya referans linkiyle gelenlerin
oranı, hangi kanalın organik paylaşım ürettiğini gösterir — en yüksek
referans oranına sahip kanal, lansman sonrası da öncelikli kanal olmalı.
