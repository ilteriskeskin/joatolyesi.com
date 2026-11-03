# İçerik ve Doğruluk Standartları

Dövüş sanatları içeriğinde yanlış bilgi, ürünün itibarını bitirir: hocası
olan bir pratisyen hatalı kata sırası gördüğü anda siteye bir daha güvenmez.
Bu yüzden içerik hattının en önemli adımı doğrulamadır.

## Kaynak hiyerarşisi (güçlüden zayıfa)

1. **Resmi müfredat / federasyon:** ZNKR (All Japan Kendo Federation) Seitei Iai ve Seitei Jodo, Nihon Kendō Kata, Aikikai / Iwama (Saito) yayınları, ilgili ryūha'nın resmi siteleri.
2. **Tanınmış hocaların kitapları ve resmi dojo/federasyon yayınları** (yazar, eser, sayfa/bölüm belirtilir).
3. **Saygın ikincil kaynaklar:** akademik çalışmalar, köklü dojo siteleri, federasyon el kitapları.
4. **Zayıf kaynak (tek başına yetmez):** forumlar, Reddit, kişisel bloglar, YouTube açıklamaları, Wikipedia. Yalnız güçlü bir kaynakla birlikte destekleyici olarak kullanılır.

## Kurallar

- **Her olgusal iddia** (tarih, isim, kata sırası, hareket sayısı, ölçü, köken hikâyesi) en az **bir güçlü (1-2)** ya da **birbirinden bağımsız iki orta (3)** kaynağa dayanır.
- **Kaynaklar çelişiyorsa** içerik bunu açıkça söyler ("Iwama çizgisinde X, Aikikai Hombu'da Y olarak öğretilir") ya da iddia çıkarılır.
- **Rivayet olarak işaretlenir:** Muso Gonnosuke–Musashi gibi efsaneler "rivayete göre" diye yazılır.
- **Adım adım kata dökümleri** en yüksek risktir: yalnızca resmi müfredattan ya da açıkça atfedilen bir kaynaktan yazılır. Emin olunmayan dökümler yazılmaz; `TODO.md` §3b "Rehber araştırma listesi"ne eklenir.
- **Güvenlik:** Sağlık/sakatlanma tavsiyesi verilmez. Isınma ve "hocana danış" uyarısı serbesttir.
- **Ekipman önerileri:** Ölçüler kaynaklı yazılır. Marka ya da affiliate linki konmaz (BRIEF kapsam dışı).
- **Dil:** TR birincil ve detaylı, EN özet. Japonca terimler Hepburn romanizasyonuyla ve tutarlı yazılır (makron tercihi dosya içinde tutarlı olsun: `jōdō` veya `jodo`, karışık değil).
- **Telif:** Kaynaklardan uzun alıntı yapılmaz. Bilgi kendi cümlelerimizle yazılır.

## Taslak formatı (`docs/team/content/drafts/<slug>.md`)

```markdown
---
type: guide | kata | blog | tip
target: app/guide_content.py#aikijo.kata  (nereye girecek)
discipline: aikijo
status: draft
---

# Başlık (TR)

Metin... İddia cümlesi.[^1]

[^1]: Kaynak: yazar, eser/sayfa adı, URL, erişim tarihi — ve kaynakta bu iddiayı destekleyen kısmın kendi cümlemizle özeti.
```

## Denetim sonucu (fact-checker ekler)

```markdown
## Denetim — YYYY-MM-DD
- Sonuç: ONAYLANDI | DÜZELTİLDİ | REDDEDİLDİ
- [^1] ✅ doğrulandı (kaynak açıldı, iddiayı destekliyor)
- [^2] ⚠️ zayıf kaynak → cümle yumuşatıldı / çıkarıldı
- [^3] ❌ doğrulanamadı → TODO.md §3b'ye taşındı
```

Yalnız **ONAYLANDI** ya da **DÜZELTİLDİ** durumundaki taslaklar `content/verified/`'e geçer ve koda girebilir.
