---
type: kata
target: app/seed.py#BOKKEN (aiki-ken suburi 1-7, description_en)
discipline: bokken
status: draft
---

# Aiki-ken suburi 1-7: EN seed metinleri (B-41)

Kaynak belge: `docs/team/content/verified/2026-11-15-30-gun-bokken-programi.md`, "## 4. Suburi hareket açıklamaları" (onaylı TR) ve "Denetim — 2026-11-15" bölümü. Öneriler onaylı TR'nin sadık EN karşılığıdır; TR'de olmayan ayrıntı eklenmedi. Japonca terimler TR'deki gibi (shomen, hanmi, waki gamae, gedan, tsuki).

## Tablo

| Slug | Mevcut EN | Önerilen EN | Dayanak (§4 TR cümlesi) |
|---|---|---|---|
| `bokken-shomen-suburi` | Full overhead cut finishing at belly height; body drops with the cut. | A single, straight shomen cut (a vertical cut from overhead down), made from hanmi stance. | Madde 1: "Hanmi duruştan tek, düz shomen kesişi (tepeden aşağı dikey kesiş)." |
| `aiki-ken-suburi-2` | Step back to jodan, step in and cut. | Step back with the right foot as the sword rises overhead; then step forward with a straight shomen cut. | Madde 2: "Sağ ayakla geri adım atarken kılıç başın üstüne kalkar; ardından öne adımla düz shomen kesişi." |
| `aiki-ken-suburi-3` | (değişmiyor) Step back, raise the sword and lower it to the right side at thigh height (waki gamae); step forward with a shomen cut. Some dojos (e.g. Aikido Australia) teach this suburi to gedan on the step back; follow your teacher's line. | Aynı metin korunur. | Madde 3, üç cümlenin üçü de birebir karşılanıyor (waki gamae, uyluk hizası, gedan ayrımı, hocanın çizgisi). |
| `aiki-ken-suburi-4` | Walking continuous shomen cuts, one per step. | Advancing, switching between right and left stance, with continuous shomen cuts. | Madde 4: "İlerlerken sağ-sol duruş değiştirerek art arda shomen kesişi." |
| `aiki-ken-suburi-5` | (değişmiyor) Advancing, alternating right and left diagonal cuts aimed at the side of the head. | Aynı metin korunur. | Madde 5: "İlerlerken sağa ve sola dönüşümlü, başın yanına yönelen çapraz kesişler." |
| `aiki-ken-suburi-6` | (değişmiyor) A thrust (tsuki) after every cut, repeated alternately on the right and left side. | Aynı metin korunur. | Madde 6: "Her kesişin ardından tsuki; sağ ve sol tarafta dönüşümlü tekrarlanır." |
| `aiki-ken-suburi-7` | (değişmiyor) Cut in the right stance, then step forward and thrust (tsuki) in the left stance; repeated while advancing. | Aynı metin korunur. | Madde 7: "Sağ duruşta kesiş, ardından öne adımla sol duruşta tsuki; tekrarlanarak ilerlenir." |

Özet: 3 satır değişir (suburi 1, 2, 4); suburi 3, 5, 6, 7 mevcut haliyle onaylı TR'ye sadık.

## Mevcut EN'de kaynaksız ifadeler

- **Suburi 1:** "finishing at belly height" (§4'te yok; Denetim'de de geçmiyor), "body drops with the cut" (§4'te yok), "Full" (TR "tek, düz" der; "tam" demez).
- **Suburi 2:** "jodan" §4 metninde geçmiyor ("başın üstüne" der). Denetim [^2] jodan'ı üç kaynakta ✅ buluyor, yani çelişki değil; ancak §4 onaylı metnine bağlı kalmak için "overhead" yazıldı. İsterseniz "(jodan)" parantezi geri eklenebilir, karar content-writer dışı.
- **Suburi 4:** "one per step" §4'te yok (TR "art arda" der, adım başına kesiş sayısı söylemez); "Walking" yerine TR'deki "ilerlerken" ve "sağ-sol duruş değiştirerek" karşılığı eksikti.

## Not (kapsam dışı, değiştirilmedi)

Seed'deki **TR** metinlerde de kaynaksız ifadeler var: suburi 1 "kesiş göbek hizasında biter / diz-kalça-omuz aynı anda düşer / kol gücüyle kesme", suburi 2 "savunma pozisyonundan", suburi 4 "Nefesle eşle: adım-kes-nefes". TR ve EN birlikte düzeltilmeli; TR'yi §4'e hizalamak için developer'a ayrı not gerekir. Ayrıca slug `aiki-ken-suburi-7` başlığı "Nana no suburi", §4 ise "Shichi (nana) no suburi" der; tutarlılık için başlık kararı developer'da.
