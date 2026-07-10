# Joryu / Jo Atölyesi — Deploy & Lansman Rehberi

Tek kaynak: domain, sunucu, deploy akışı ve lansman kontrol listesi.
Claude Code bu dosyayı production hazırlığında referans alır;
"sunucuda çalıştırılacak komutlar" bölümünü proje netleşince günceller.

---

## 1. Domain ve dil stratejisi

- İlk lansman domain'i: **joatolyesi.com** (mevcut)
- Bu domain'de varsayılan dil **TR**, EN seçilebilir (cookie + ?lang=)
- Gelecek: global için joryu.app alınırsa AYNI uygulama, domain'e göre
  varsayılan dil değişir. İkinci deploy yok — host header'a bak.

## 2. DNS (DigitalOcean)

| Kayıt | Tür | Değer        |
|-------|-----|--------------|
| @     | A   | <droplet-ip> |
| www   | A   | <droplet-ip> |

TTL düşük tut (300s) — değişiklikler hızlı otursun.
DNS yayılmadan Caddy sertifika ALAMAZ; önce DNS, sonra compose up.

## 3. Sunucu mimarisi (droplet)

```
İnternet → Caddy (80/443, otomatik SSL) → app (FastAPI, internal :8000)
                                        → postgres (internal, DIŞARI KAPALI)
```

Caddyfile (özet):
```
joatolyesi.com, www.joatolyesi.com {
    reverse_proxy app:8000
}
```

Kurallar:
- 80/443 dışında hiçbir port dışarı açık değil (SSH 22 hariç)
- Postgres portu compose'da host'a MAP EDİLMEZ (ports: yok, sadece internal network)
- SSL Caddy'de otomatik — manuel sertifika yönetimi YOK
  (api-dev.heybooster.ai vakasının tekrarı istenmiyor)

## 4. Firewall (droplet üzerinde)

```bash
ufw allow 22/tcp
ufw allow 80/tcp
ufw allow 443/tcp
ufw enable
```
(Alternatif: DO Cloud Firewall'dan aynı kurallar.)

## 5. Deploy akışı

İlk kurulum:
```bash
git clone <github-repo-url> ~/joryu && cd ~/joryu
cp .env.example .env   # değerleri doldur
docker compose up -d --build
```

Güncelleme:
```bash
cd ~/joryu && git pull && docker compose up -d --build
```

## 6. Bakım cron'ları

```cron
# Günlük Postgres yedeği (03:00) — waitlist + kullanıcı verisi tek değerli varlık
0 3 * * * /home/<user>/joryu/scripts/backup.sh

# Haftalık eski Docker imajı temizliği (Pazar 04:00) — disk dolmasın
0 4 * * 0 docker image prune -af
```

backup.sh gereksinimleri: pg_dump → gzip → tarihli dosya →
son 14 yedeği tut, eskisini sil. (Claude Code script'i yazar.)

## 7. Ödeme

- Lemon Squeezy **test mode**. Canlı anahtarlar ancak lansman kararıyla
  .env'e girer. Test/canlı ayrımı env değişkeniyle.

## 8. Lansman kontrol listesi

- [ ] DNS A kayıtları droplet'e dönük, yayılmış (dig joatolyesi.com)
- [ ] docker compose up -d --build sorunsuz, https://joatolyesi.com açılıyor
- [ ] Sertifika geçerli (Caddy otomatik aldı)
- [ ] Telefondan test: sayfa + waitlist formu mobilde düzgün
- [ ] Kayıt → giriş → pratik kaydı → streak akışı uçtan uca çalışıyor
- [ ] Streak sınır durumları: gece yarısı geçişi (Europe/Istanbul),
      gün atlayınca sıfırlanma
- [ ] Admin CSV export çalışıyor (/admin/waitlist?token=...)
- [ ] backup.sh elle bir kez çalıştırıldı, dump dosyası doğrulandı
- [ ] ufw aktif, sadece 22/80/443 açık, Postgres dışarıdan erişilemiyor

## 9. Trafik kaynak takibi (bio linkleri)

| Platform  | Link                      |
|-----------|---------------------------|
| Instagram | joatolyesi.com/?src=ig    |
| YouTube   | joatolyesi.com/?src=yt    |
| TikTok    | joatolyesi.com/?src=tt    |

`src` waitlist tablosuna yazılır → hangi kanal dönüştürüyor, CSV'den görülür.
Bu veri Phase 1 lansmanında hangi kanala yüklenileceğini belirler.

## 10. Doğrulama kapısı (hatırlatma)

Landing page yayında 2 hafta: **100+ e-posta → uygulama lansmanı**.
20 altı → konumlandırmayı değiştir, lansmanı erteleme kararını gözden geçir.

---

## Sunucuda çalıştırılacak komutlar (Claude Code doldurur)

> Phase 1 production hazırlığı bitince Claude Code bu bölümü projenin
> gerçek dosya/servis adlarıyla, sıralı ve kopyala-yapıştır çalışır
> halde yazar.
