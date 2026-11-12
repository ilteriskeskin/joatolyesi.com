# GSC analizi — 2026-11-12 (son 3 ay, web)

Kaynak: İlteriş'in GSC dışa aktarımı (11 Ağu – 12 Kas). Ham dosyalar repoda değil.

## Tablo
- **4.120 gösterim, 26 tıklama, TO %0,6.** Ortalama pozisyon 8–14, yani çoğu sorguda 1. sayfanın altındayız.
- Gösterim artıyor: haftalık ~250'den ~440'a. Tıklama yerinde sayıyor (haftada 0–5).
- %62 Türkiye, %64 mobil.
- **Gösterimlerin %54'ü karate (1.521) ve taekwondo (761) teknik sayfalarından geliyor.** Kendo 507, rehberler 830, blog 203. Aiki-jo, jodo ve iaido kata sayfaları toplam 176.
- `?lang=en` URL'leri ayrı sayfa olarak indekslenmiş (1.299 gösterim).

## Teşhis
1. **Sorun sıralama değil, tıklama.** `dwit chagi` (200 gösterim, poz. 5,5), `zenkutsu dachi` (155, 7,2), `jo nedir` (104, 9,0), `shuto uchi` (79, 5,7) sorgularında 1. sayfadayız ama 0 tıklama alıyoruz.
2. **Sayfalar ince.** Kata sayfasının içeriği 1–2 cümle (ör. kiba dachi). Başlık "Kiba dachi — Karate — Joryu" kalıbında, meta açıklaması da o tek cümle. Arayan kişi "nedir, nasıl yapılır" diye bakıyor, snippet buna cevap vermiyor.
3. **Ürün odağıyla talep ayrışıyor.** Ürün jo/bokken odaklı, karate ve taekwondo kayıtta seçilemiyordu (`SELECTABLE_DISCIPLINES`). Kata sayfaları 2026-11-04'ten beri sitemap'te. Arama talebi ise en çok bu iki branşta.

## Önerilen işler (BACKLOG B-37, B-38)
- **B-37 En çok gösterim alan 15 sayfayı derinleştirmek.** Her sayfaya "nedir / nasıl yapılır / sık hata" bölümleri, soruya cevap veren title ve meta. Akış: content-writer → fact-checker → developer. Ölçüt: 4 hafta sonra bu 15 sayfanın TO'su %0,5'ten %2'ye çıkmalı.
- **B-38 Karate ve taekwondo yeniden seçilebilir.** İlteriş kararı 2026-11-12. Kayıt, profil, pratik kaydı, kata listesi ve rehber dizini bu branşları yeniden gösterir. (Sitemap'te zaten vardı.)

## B-37 sayfa listesi (gösterime göre)
tkd-dwit-chagi 200 · guide/bokken 217 · karate-zenkutsu-dachi 155 · tkd-naeryo-chagi 131 · blog/jo-nedir 130 · kendo-kodachi-1 130 · karate-kiba-dachi 120 · karate-tekki-shodan 111 · karate-jion 98 · karate-heian-sandan 98 · karate-gyaku-tsuki 97 · guide/kendo 90 · guide/taekwondo 85 · karate-shuto-uchi 79 · karate-heian-godan 70
