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

Sunucuda halihazırda **nginx** çalışıyor ve `/var/www` altındaki başka
siteleri yayınlıyor. 80/443 nginx'te kalır; Caddy KULLANILMAZ.
Joryu, mevcut sitelere DOKUNMADAN yeni bir nginx server block olarak eklenir.

```
İnternet → nginx (80/443, mevcut) ── diğer siteler (/var/www/..., AYNEN KALIR)
                                  └─ joatolyesi.com → 127.0.0.1:8000 (Docker: FastAPI)
                                                          └─ postgres (internal, DIŞARI KAPALI)
```

Kurallar:
- Diğer sitelerin server block'larına ve `/var/www`'a ASLA dokunulmaz;
  sadece joatolyesi.com'a ait yeni bir conf dosyası eklenir
- App portu compose'da `127.0.0.1:8000` — dışarıdan doğrudan erişilemez
- Postgres portu compose'da host'a MAP EDİLMEZ (ports: yok, sadece internal network)
- SSL certbot ile (sunucudaki mevcut düzen neyse o); sadece joatolyesi.com
  için sertifika yenilenir, diğer sertifikalara dokunulmaz

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

## Sunucuda çalıştırılacak komutlar — Phase 0 (waitlist-only) yayını

> Senaryo: joatolyesi.com şu ana kadar nginx'ten statik index.html olarak
> yayındaydı. Aynı makinede `/var/www` altında başka canlı siteler var —
> aşağıdaki adımların hiçbiri onlara dokunmaz. Sadece joatolyesi.com'un
> kendi server block'u değişir.

### 0) Ön kontrol — çakışma var mı?

```bash
# 8000 portu boş mu? (doluysa compose.yml'de 127.0.0.1:8001:8000 yap,
# nginx conf'ta proxy_pass'i de 8001 yap)
sudo ss -tlnp | grep :8000 || echo "8000 bos"

# Docker ve compose kurulu mu?
docker --version && docker compose version

# joatolyesi.com'un MEVCUT nginx conf'u hangisi? (yedeklemek için)
grep -rl "joatolyesi" /etc/nginx/sites-enabled/ /etc/nginx/conf.d/ 2>/dev/null
```

Docker yoksa: https://docs.docker.com/engine/install/ (resmî script yeterli).

### 1) Uygulamayı kur ve başlat

```bash
git clone https://github.com/ilteriskeskin/joatolyesi.com.git ~/joryu && cd ~/joryu
cp .env.example .env
nano .env
```

`.env`'de doldurulacaklar:
- `POSTGRES_PASSWORD` ve `DATABASE_URL` içindeki şifre (aynı olacak) → `openssl rand -hex 24`
- `ADMIN_TOKEN` → `openssl rand -hex 32` (CSV export bununla açılır, sakla)
- `SECRET_KEY` → `openssl rand -hex 32`
- `ENV=production`
- `WAITLIST_ONLY=true`  ← Phase 0'ın anahtarı: sadece landing + mail toplama
- Lemon Squeezy alanları şimdilik boş kalır

```bash
docker compose up -d --build

# Migration'ları çalıştır (waitlist tablosu burada oluşur)
docker compose exec app alembic upgrade head

# Yerelden doğrula: landing 200 dönmeli
curl -sI http://127.0.0.1:8000/ | head -1
```

### 2) nginx: statik site yerine reverse proxy

Önce mevcut conf'u yedekle (adım 0'da bulunan dosya, örn.
`/etc/nginx/sites-available/joatolyesi.com`):

```bash
sudo cp /etc/nginx/sites-available/joatolyesi.com ~/joatolyesi.com.nginx.bak
```

Sonra AYNI dosyanın içeriğini şununla değiştir (başka dosyaya dokunma;
`ssl_certificate` satırlarını eski conf'tan aynen koru — certbot yazmıştı):

```nginx
server {
    listen 80;
    listen [::]:80;
    server_name joatolyesi.com www.joatolyesi.com;
    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl http2;
    listen [::]:443 ssl http2;
    server_name joatolyesi.com www.joatolyesi.com;

    # Eski conf'taki certbot satırlarını AYNEN buraya taşı:
    ssl_certificate     /etc/letsencrypt/live/joatolyesi.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/joatolyesi.com/privkey.pem;
    include             /etc/letsencrypt/options-ssl-nginx.conf;
    ssl_dhparam         /etc/letsencrypt/ssl-dhparams.pem;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host              $host;
        proxy_set_header X-Real-IP         $remote_addr;
        proxy_set_header X-Forwarded-For   $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

> Site şimdiye kadar HTTP-only yayındaysa (sertifika yoksa): üstteki 443
> bloğunu atla, 80 bloğunda `return 301` yerine `location /` proxy bloğunu
> kullan, sonra `sudo certbot --nginx -d joatolyesi.com -d www.joatolyesi.com`
> çalıştır — certbot conf'u kendisi SSL'e çevirir.

```bash
# Sözdizimi kontrolü — "syntax is ok" görmeden reload ETME
sudo nginx -t

# reload restart DEĞİLDİR: diğer sitelerde kesinti olmaz
sudo systemctl reload nginx
```

### 3) Doğrulama

```bash
curl -sI https://joatolyesi.com/ | head -1          # HTTP/2 200
curl -s -o /dev/null -w "%{http_code}\n" https://joatolyesi.com/login   # 404 (waitlist-only)

# Waitlist formu uçtan uca
curl -s -X POST https://joatolyesi.com/waitlist -d "email=test@test.com&lang=tr"

# Kayıt düştü mü? (CSV export, ADMIN_TOKEN ile)
curl -s "https://joatolyesi.com/admin/waitlist?token=<ADMIN_TOKEN>"

# Diğer siteler hâlâ ayakta mı? Birkaçını kontrol et:
curl -sI https://<diger-site>/ | head -1
```

Tarayıcıdan da bak: sayfada login/register linki OLMAMALI, waitlist formu
çalışmalı (TR/EN dil değişimi dahil).

### 4) Güncelleme akışı (sonraki deploylar)

```bash
cd ~/joryu && git pull && docker compose up -d --build
docker compose exec app alembic upgrade head   # yeni migration varsa
```

### 5) App lansmanı günü (Phase 1'e geçiş)

```bash
cd ~/joryu
sed -i 's/WAITLIST_ONLY=true/WAITLIST_ONLY=false/' .env
docker compose up -d   # restart yeterli, build gerekmez
```

Sonra toplanan maillere "yayındayız" duyurusu (CSV: adım 3'teki export).

### Geri alma (rollback)

Bir şey ters giderse eski statik site 2 komutla geri gelir:

```bash
sudo cp ~/joatolyesi.com.nginx.bak /etc/nginx/sites-available/joatolyesi.com
sudo nginx -t && sudo systemctl reload nginx
docker compose -f ~/joryu/compose.yml down   # istenirse
```

(Eski statik dosyalar `/var/www`'da duruyorsa silme — rollback sigortan.)
