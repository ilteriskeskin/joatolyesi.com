# Metrikler

İlteriş haftada bir günceller: GA4 + `scripts/weekly_metrics.py` çıktısı.

DB metrikleri (salt okuma; demo + sahip hesabı hariç; varsayılan son tamamlanan Pazartesi-Pazar haftası):

```
docker compose exec app python scripts/weekly_metrics.py [--week-start YYYY-MM-DD]
```

Çıktının ilk satırı aşağıdaki tabloya yapıştırılır; GA sütunları (`—`) GA4'ten elle doldurulur.

Ekip bu dosyayı **okur**, rakam uydurmaz. Bir hafta boşsa PO raporda ister.

**Kuzey yıldızı:** haftalık aktif pratisyen (o hafta ≥1 pratik kaydı olan gerçek kullanıcı; demo hesaplar hariç).

## Haftalık tablo

| Hafta | GA aktif kull. (28g) | Yeni kull. | Ort. etkileşim | Google organik oturum | Instagram oturum | Yeni kayıt | Haftalık aktif pratisyen | Not |
|---|---|---|---|---|---|---|---|---|
| 2026-11-02 (başlangıç) | 40 | 38 | 20 sn | 17 | ~5 | ? | ? | Geri gelen kullanıcı ≈ 0. Ashburn/Altoona/San Jose/Dublin büyük ihtimalle bot veya veri merkezi. "Pratik" sayfası 3 kullanıcı. |

## Başlangıç notları (2026-11-02, son 28 gün GA4)

- En çok görüntülenen: Pratik (16), Landing EN (13), Kata ve suburi kütüphanesi (11), Landing TR (8), Jodo rehberi (4), Bokken (4), Kokutsu dachi/Karate (3).
- Landing hemen çıkma oranı: %66-75.
- Kaynaklar (oturum): google/organic 17, direct 14, instagram 4+1, facebook 3+3+2, threads 2.
- **GA4'te özel olay yok:** kayıt ve pratik kaydı GA'da ölçülmüyor. Dönüşüm hunisi şu an görünmez (bkz. BACKLOG B-01).

## GA4 olayları

Deploy sonrası GA4'e düşen özel olaylar (parametrelerde kişisel veri yok; admin sayfalarında GA yüklenmez):

| Olay | Ne zaman | Parametreler |
|---|---|---|
| `sign_up` | Kayıttan sonraki ilk sayfa yüklemesinde, bir kez (yenilemede tekrarlanmaz) | `method: email`, `discipline` |
| `practice_logged` | Dashboard'dan pratik kaydı (HTMX) veya kata sayfasında "Bugün bunu çalıştım" | `discipline`, `minutes`, `source: dashboard \| kata` |
| `share_card` | Paylaş (native), X, WhatsApp veya kart indirme tıklaması | `method: native \| x \| whatsapp \| download`, `context: dashboard \| profile` |
| `pwa_install` | Tarayıcının `appinstalled` olayı (iOS Safari bu olayı vermez, oradaki yüklemeler ölçülmez) | — |

**İlteriş yapacak:** GA4 → Yönetici → Etkinlikler'de `sign_up` ve `practice_logged`'ı **Key event** (anahtar etkinlik) olarak işaretle. İlk anlamlı veri deploy'dan ≥1 hafta sonra.
