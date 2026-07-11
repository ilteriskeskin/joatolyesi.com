# Joryu — Lansman Rehberi (baştan sona, adım adım)

Bu doküman lansmana kadar yapılacak HER ŞEYİ sırasıyla anlatır: hangi
hesabı nereden açacaksın, hangi token'ı nereden alacaksın, .env'e ne
yazacaksın, hangi komutu çalıştıracaksın. Sunucu mimarisi DEPLOY.md'de,
roadmap TODO.md'de; lansman BURADAN yürütülür.

Sıra önemli: 1 → 8 bölümlerini yukarıdan aşağı takip et.

---

## 1. Açılacak hesaplar ve alınacak anahtarlar (özet tablo)

| # | Hesap | Nereden | Ne alacaksın | .env'de nereye |
|---|-------|---------|--------------|----------------|
| 1 | Resend (mail) | resend.com — ücretsiz plan yeter (3.000 mail/ay) | API key (`re_...`) + domain doğrulaması | `RESEND_API_KEY` |
| 2 | Sentry (hata izleme) | sentry.io — ücretsiz plan | DSN (`https://...ingest...`) | `SENTRY_DSN` |
| 3 | Lemon Squeezy (ödeme) | lemonsqueezy.com — store onayı 1-2 gün sürebilir, ERKEN BAŞLA | 2 buy link + webhook signing secret | `LS_CHECKOUT_URL_*`, `LS_WEBHOOK_SECRET` |

Zaten var olanlar: DigitalOcean (sunucu + DNS), GitHub (kod), GA4 (analitik, kodda gömülü).

---

## 2. Resend kurulumu (mailler bunsuz GİTMEZ)

Şifre sıfırlama, e-posta doğrulama ve waitlist davetlerinin hepsi buradan çıkar.

1. resend.com → hesap aç (GitHub ile girilebilir).
2. **API Keys** → Create API Key → adı `joryu-prod`, izin "Sending access".
   Çıkan `re_...` değerini kopyala — BİR KEZ gösterilir. (.env'e yazacaksın, adım 5.)
3. **Domains** → Add Domain → `joatolyesi.com`, bölge EU seç.
4. Resend'in listelediği DNS kayıtlarını DigitalOcean'a ekle:
   DigitalOcean → Networking → Domains → joatolyesi.com → Create Record.
   Tipik olarak 3 kayıt ister (panel ne diyorsa onu gir):
   - TXT — host: `send`, value: `v=spf1 include:amazonses.com ~all` benzeri (SPF)
   - TXT — host: `resend._domainkey`, value: uzun DKIM anahtarı
   - MX — host: `send`, value: `feedback-smtp.eu-west-1.amazonses.com`, priority 10
5. Resend panelinde **Verify** butonu → "Verified" olana kadar bekle
   (5 dk - birkaç saat). Doğrulanmadan mailler 403 hatası alır.
6. Test (sunucuda, adım 5-6 bittikten sonra):
   ```bash
   docker compose exec app python -c "
   import asyncio
   from app.mail import send_email
   asyncio.run(send_email('aliilteriskeskin@gmail.com', 'Joryu test', '<p>Çalışıyor.</p>'))
   "
   ```
   Gelen kutuna düştüyse tamam.

## 3. Sentry kurulumu (5 dakika)

1. sentry.io → hesap aç → Create Project → platform **FastAPI**, adı `joryu`.
2. Kurulum sayfasındaki **DSN**'i kopyala (`https://xxx@yyy.ingest.de.sentry.io/zzz`).
3. .env'e `SENTRY_DSN=` olarak yaz (adım 5). Boş bırakılırsa Sentry kapalı çalışır — zorunlu değil ama ilk hafta 500'leri görmek için şiddetle önerilir.

## 4. Lemon Squeezy kurulumu (Pro abonelik)

> Store onayı zaman alabilir; başvuruyu lansmandan en az 1 hafta önce yap.
> Onay beklerken her şey **test mode**'da kurulup denenebilir.

1. lemonsqueezy.com → hesap + store aç (store URL: `joryu.lemonsqueezy.com` gibi).
2. **Products** → iki abonelik ürünü:
   - "Joryu Pro Monthly" — $4.99/ay, subscription
   - "Joryu Pro Yearly" — $39/yıl, subscription
3. Her ürün → **Share** → Buy Link'i kopyala → .env'e:
   `LS_CHECKOUT_URL_MONTHLY=` ve `LS_CHECKOUT_URL_YEARLY=`
4. **Settings → Webhooks** → Add endpoint:
   - URL: `https://joatolyesi.com/webhooks/lemonsqueezy`
   - Events: `subscription_created`, `subscription_updated`,
     `subscription_cancelled`, `subscription_expired`
   - Signing secret üret → .env'e `LS_WEBHOOK_SECRET=`
5. Test mode'dayken sahte kartla (4242...) bir abonelik satın al;
   sitede `/billing` "aktif" göstermeli.
6. **Lansman günü:** store'u live'a al. DİKKAT: live modda buy linkler ve
   webhook secret DEĞİŞİR — 3. ve 4. adımı live değerlerle tekrarla, .env'i güncelle.

## 5. Sunucu .env — son hali

```bash
ssh root@<droplet-ip>
nano /root/joryu/.env
```

Şablon (değerleri kendi anahtarlarınla doldur):

```
# --- Veritabanı (mevcut, DOKUNMA) ---
POSTGRES_USER=joryu
POSTGRES_PASSWORD=<mevcut>
POSTGRES_DB=joryu
POSTGRES_HOST=db
POSTGRES_PORT=5432
DATABASE_URL=postgresql+asyncpg://joryu:<mevcut>@db:5432/joryu

# --- Uygulama ---
ENV=production              # secure cookie için ŞART
WAITLIST_ONLY=true          # lansman anına kadar true
ADMIN_TOKEN=<mevcut>        # CSV export + admin ekranları
SECRET_KEY=<mevcut>         # DEĞİŞTİRME: değişirse tüm oturumlar/tokenlar düşer
BASE_URL=https://joatolyesi.com   # mail linkleri; http/localhost KALMASIN

# --- Mail (bölüm 2) ---
RESEND_API_KEY=re_...
MAIL_FROM=Joryu <noreply@joatolyesi.com>

# --- Hata izleme (bölüm 3) ---
SENTRY_DSN=https://...

# --- Ödeme (bölüm 4) ---
LS_WEBHOOK_SECRET=...
LS_CHECKOUT_URL_MONTHLY=https://joryu.lemonsqueezy.com/checkout/buy/...
LS_CHECKOUT_URL_YEARLY=https://joryu.lemonsqueezy.com/checkout/buy/...
```

Kaydettikten sonra: `cd /root/joryu && docker compose up -d` (restart yeter).

## 6. Lansmandan önceki hafta — hazırlık kontrolleri

```bash
cd /root/joryu

# 1) Son kod + migration (0005 dahil: takip sistemi)
git pull
docker compose up -d --build
docker compose exec app alembic current        # "0005 (head)" görmelisin

# 2) Yedek sistemi çalışıyor mu
crontab -l                                     # backup + prune satırları duruyor mu
./scripts/backup.sh && ls -lh /root/backups/joryu/ | tail -2

# 3) Mail testi (bölüm 2/6'daki komut) — gelen kutuna düşmeli

# 4) İçerik: kata videoları
#    https://joatolyesi.com/admin/katas?token=<ADMIN_TOKEN>
#    En azından aiki-jo + bokken videoları ekli olmalı.

# 5) Waitlist kaç kişi? (dry-run, mail GÖNDERMEZ)
docker compose exec app python scripts/send_invites.py

# 6) Disk/RAM kontrolü (512MB droplet)
df -h / && free -m      # disk %80+ veya swap sürekli doluysa 1GB'a yükselt
```

Telefondan da bak: joatolyesi.com açılıyor mu, waitlist formu çalışıyor mu.

## 7. LANSMAN GÜNÜ (sıralı, ~20 dakika)

```bash
cd /root/joryu

# 1) Uygulamayı aç
sed -i 's/WAITLIST_ONLY=true/WAITLIST_ONLY=false/' .env
docker compose up -d

# 2) Duman testi
curl -s -o /dev/null -w "%{http_code}\n" https://joatolyesi.com/register   # 200
curl -s -o /dev/null -w "%{http_code}\n" https://joatolyesi.com/guide      # 200
# Tarayıcıdan tam tur: kayıt ol → doğrulama maili geldi mi → pratik kaydet
# → kuşak göründü mü → profili herkese açık yap → /u/<kullanıcıadı> →
# profil linkini WhatsApp'a yapıştır → kart görseli önizlemede çıkıyor mu

# 3) Lemon Squeezy'yi live'a al (bölüm 4/6) ve .env'i live değerlerle güncelle
docker compose up -d

# 4) Waitlist davetleri
docker compose exec app python scripts/send_invites.py          # son kontrol (dry-run)
docker compose exec app python scripts/send_invites.py --yes    # GÖNDERİR

# 5) Sosyal duyurular (kanal takibi için linkler):
#    Instagram story : https://joatolyesi.com/?src=ig
#    YouTube gönderi : https://joatolyesi.com/?src=yt
#    LinkedIn        : https://joatolyesi.com/?src=li
#    Twitter/X       : https://joatolyesi.com/?src=tw
```

## 8. Lansman sonrası ilk 48 saat

- [ ] Sentry: hata var mı? (özellikle 500'ler ve webhook hataları)
- [ ] `docker compose logs app --since 24h 2>&1 | grep -i error`
- [ ] Resend → Logs: doğrulama/davet mailleri gidiyor mu, bounce oranı?
- [ ] Dönüşüm: `docker compose exec db psql -U joryu -d joryu -c "SELECT count(*) FROM users;"`
      (davet sayısıyla kıyasla)
- [ ] `df -h && free -m` — 512MB droplet zorlanıyorsa DO panelinden
      $12'lik 1GB'a yükselt (~5 dk kesinti, önce yedek al)
- [ ] O gece backup cron'u çalışmış mı: `ls -lh /root/backups/joryu/`
- [ ] İlk gerçek kullanıcılardan geri bildirim topla (Instagram DM)

---

## 9. Acil durumlar

**Site tamamen bozuldu →** eski statik sayfaya dön:
```bash
sudo cp ~/joatolyesi.com.nginx.bak /etc/nginx/sites-available/joatolyesi.com
sudo nginx -t && sudo systemctl reload nginx
```

**Uygulama ayakta ama hatalı →** önceki commit'e dön:
```bash
cd /root/joryu && git log --oneline -5      # sağlam commit'i seç
git checkout <commit> && docker compose up -d --build
# migration geri almak gerekirse: docker compose exec app alembic downgrade -1
```

**Mailler gitmiyor →** Resend → Logs. Uygulama mail hatasında çökmez,
sadece loglar; site çalışmaya devam eder, acele etme.

**DB'yi yedekten dön →**
```bash
zcat /root/backups/joryu/joryu_<tarih>.sql.gz | docker compose exec -T db psql -U joryu -d joryu
```

**Lansmanı geri çek (kayıt/girişi kapat) →**
```bash
sed -i 's/WAITLIST_ONLY=false/WAITLIST_ONLY=true/' /root/joryu/.env
docker compose up -d
```

---

## 10. Envanter (kim nerede)

| Ne | Nerede | Not |
|---|---|---|
| Sunucu | DigitalOcean droplet (fra1, 512MB) | ssh root@... |
| DNS | DigitalOcean → Networking | joatolyesi.com + Resend kayıtları |
| SSL | Let's Encrypt / certbot | otomatik yenilenir, cron EKLEME |
| Mail | resend.com | API key + domain doğrulaması |
| Hata izleme | sentry.io | DSN .env'de |
| Ödeme | lemonsqueezy.com | test→live geçişinde linkler ve secret değişir |
| Analytics | GA4 (G-54NX2S2Z01) | kodda gömülü |
| Kod | github.com/ilteriskeskin/joatolyesi.com | main dalı |
| Yedekler | /root/backups/joryu/ | ayda bir `scp` ile lokale kopyala |
| Admin CSV | joatolyesi.com/admin/waitlist?token=ADMIN_TOKEN | waitlist dökümü |
| Admin kata | joatolyesi.com/admin/katas?token=ADMIN_TOKEN | video ekleme |
