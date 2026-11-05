---
type: guide
target: app/seed.py#WEEKS, app/seed.py#_build_program_days, app/seed.py#seed_content (Program "30-day-jo-suburi")
discipline: aikijo
status: verified
---

# 30 Günlük Jo Suburi Programı — düzeltilmiş metin

Bu dosya, seed'e birebir yapıştırılabilecek onaylı metni içerir. Kod mantığı
(`week_idx`, `focus = focuses[(day_num - 1) % len(focuses)]`) değişmiyor.
Yalnız veri ve metin dizgileri değişiyor.

> Not: Program yalnız `program_count == 0` iken seed ediliyor. Canlı veritabanında
> program satırı varsa bu metin kendiliğinden güncellenmez. Ayrı bir SQL/migration
> gerekir (kapsam dışı, backend'e bildirilecek).

## 1. WEEKS (birebir değiştir)

Liste sıraları bilerek döndürüldü. Hafta w'nin ilk günü `(7w) % len` indeksine
denk geliyor. Bu sırayla her haftanın ilk günü resmi sıradaki ilk suburi oluyor
(hafta 2: 6 → 7 → 8, hafta 3: 11 → 14 → 15, hafta 4: 19 → 20).

```python
# Hafta temaları: (EN tema, TR tema, o haftanın odak suburi listesi)
# Sıra, (day_num - 1) % len ile her haftanın ilk günü resmi sıradaki ilk suburi
# olacak şekilde döndürülmüştür (Saito/Iwama 20 jo suburi numaralandırması).
WEEKS = [
    ("Tsuki fundamentals", "Tsuki temelleri",
     ["choku tsuki", "kaeshi tsuki", "ushiro tsuki"]),
    ("Uchikomi — striking week", "Uchikomi — vuruş haftası",
     ["men uchi gedan gaeshi", "shomen uchikomi", "renzoku uchikomi"]),
    ("Katate & hasso gaeshi", "Katate & hasso gaeshi",
     ["hasso gaeshi uchi", "hasso gaeshi tsuki", "katate gedan gaeshi"]),
    ("Nagare gaeshi — flowing forms", "Nagare gaeshi — akış formları",
     ["migi nagare gaeshi tsuki", "hidari nagare gaeshi uchi"]),
]
```

## 2. Tekrar günü metni (`if day_num % 7 == 0:` dalı)

```python
            title_en, title_tr = "Review & light flow", "Tekrar & hafif akış"
            content_en = (
                f"Week theme: {theme_en}. Today is a review day. Warm up 5 minutes "
                "(wrists, shoulders, hips). Then 10 minutes of slow, deliberate repetition "
                "of everything from this week. Half speed, full attention. "
                "Finish with 5 minutes of free movement."
            )
            content_tr = (
                f"Hafta teması: {theme_tr}. Bugün tekrar günü. 5 dakika ısın "
                "(bilek, omuz, kalça). Sonra bu haftanın tüm çalışmasını 10 dakika yavaş "
                "ve bilinçli tekrar et. Yarı hız, tam dikkat. "
                "5 dakika serbest hareketle bitir."
            )
```

## 3. Normal gün metni (`else:` dalı)

```python
            title_en = f"Focus: {focus}"
            title_tr = f"Odak: {focus}"
            content_en = (
                f"Week theme: {theme_en}. Warm up 5 minutes (wrists, shoulders, hips). "
                f"Main work: {focus} — 3 sets of 20 repetitions, rest between sets. "
                "Last set slower than the first: precision over speed. "
                "If you haven't learned this movement from a teacher yet, ask yours first. "
                "Log your session when you're done."
            )
            content_tr = (
                f"Hafta teması: {theme_tr}. 5 dakika ısın (bilek, omuz, kalça). "
                f"Ana çalışma: {focus} — 3 set x 20 tekrar, setler arası dinlen. "
                "Son set ilkinden yavaş: hızdan önce isabet. "
                "Bu hareketi henüz hocandan öğrenmediysen önce ona danış. "
                "Bitirince seansını kaydet."
            )
```

## 4. Program açıklaması (`seed_content` içinde `Program(...)`)

```python
                description_en=(
                    "One month of daily, structured jo suburi practice. "
                    "Four weekly themes: thrusts, strikes, one-handed and hasso forms, "
                    "and flowing forms. About 10–20 minutes a day."
                ),
                description_tr=(
                    "Bir ay boyunca her gün yapılandırılmış jo suburi çalışması. "
                    "Dört haftalık tema: dürtüşler, vuruşlar, tek el ve hasso formları, "
                    "akış formları. Günde yaklaşık 10–20 dakika."
                ),
```

## Denetim — 2026-11-05
- Sonuç: DÜZELTİLDİ
- Hafta 1-3 suburi adları ✅ Saito/Iwama 20 jo suburi listesiyle uyumlu. Hafta 1 = 1-3 (tsuki), hafta 2 = 6-8 (uchikomi), hafta 3 = 11 (katate) + 14-15 (hasso gaeshi). Gruplar doğru. "Katate & hasso gaeshi" adı içeriği doğru tanımlıyor (iki grubu kapsıyor, 12-13 ve 16-18 atlanmış; seçki olarak kabul edilebilir).
- ⚠️ Gün sırası: modulo nedeniyle hafta 2 renzoku uchikomi (7) ile, hafta 3 hasso gaeshi tsuki (15) ile başlıyordu. Listeler döndürülerek her hafta resmi sıradaki ilk suburi ile başlatıldı.
- ⚠️ Yazım: "menuchi gedan gaeshi", site kataloğundaki "Men uchi gedan gaeshi" ile uyumlu olsun diye "men uchi gedan gaeshi" yapıldı. İki yazım da kaynaklarda geçiyor.
- ❌ Hafta 4: "31-count kata (sections)", "free flow combinations", "full kata runs". Gün şablonu bunları "3 set x 20 tekrar" yapıyordu (60 tam 31'lik kata koşusu gibi gerçek dışı bir yük). TIAE 2026 müfredatında 31 kata 1-12 4. kyu'da, tamamı 3. kyu'da (birkaç ay ile bir yılı aşkın düzenli antrenmandan sonra) isteniyor. Dördüncü haftada yeni başlayana "full kata runs" önermek yanıltıcı. Hafta 4 yerine 20 suburi'nin son grubu olan nagare gaeshi (19-20) kondu. "Akış" teması korundu, 31 kata iddiası kalktı.
- ⚠️ Süre: normal gün 5 dk ısınma + 60 tekrar (tekrar başına ~3-5 sn, ~3-5 dk) + 2 set arası dinlenme ≈ 10-12 dk. Tekrar günü 10+5 = 15 dk. "15–25 dakika" fazla gösteriyordu. "Yaklaşık 10–20 dakika" yapıldı (yeni tekrar günü ısınmayla 20 dk).
- ⚠️ Güvenlik: tekrar gününde ısınma yoktu, eklendi. "Hocana danış" uyarısı eklendi (standartlarda serbest). Sağlık tavsiyesi yok.
- ⚠️ Terim: açıklamadaki "saplamalar" yerine sitedeki tutarlı karşılık "dürtüşler" kullanıldı. "Dönüş formları" ifadesi tek el ve hasso formlarını tam karşılamıyordu, düzeltildi.
- Kaynaklar: https://takemusu-iwama-aikido.org/?p=260, https://aikido-shuren-dojo.com/?p=87, https://takemusu-iwama-aikido.org/wp-content/uploads/2026/02/syllabus2026.pdf (TIAE v4.0; müfredat örgütten örgüte değişir)
