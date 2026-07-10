# Joryu — Lansman Runbook'u

Bu doküman lansman gününe kadar yapılacak her şeyi, sırasıyla ve
kopyala-yapıştır komutlarla anlatır. Sunucu işleri için DEPLOY.md'ye,
eksik/roadmap için TODO.md'ye bakılır; lansmanın kendisi BURADAN yürütülür.

---

## A. Lansmandan ÖNCE (bir kez yapılacak kurulumlar)

### A1. Resend domain doğrulaması (mailler bunsuz GİTMEZ)

1. https://resend.com/domains → **Add Domain** → `joatolyesi.com`
2. Resend'in verdiği DNS kayıtlarını DigitalOcean DNS'e ekle
   (Networking → joatolyesi.com → Create Record):
   - **TXT** kaydı (SPF): ad `send`, değer Resend'in verdiği `v=spf1 ...`
   - **TXT** kaydı (DKIM): ad `resend._domainkey`, değer Resend'in verdiği uzun anahtar
   - **MX** kaydı: ad `send`, değer `feedback-smtp.eu-west-1.amazonses.com` (panel ne diyorsa)
3. Resend panelinde **Verify** — birkaç dakika/saat sürebilir.
4. Doğrulama testi (sunucuda):
   ```bash
   docker compose exec app python -c "
   import asyncio
   from app.mail import send_email
   asyncio.run(send_email('aliilteriskeskin@gmail.com', 'Joryu test', '<p>Mail altyapısı çalışıyor.</p>'))
   "
   ```
   Gelen kutuna düştüyse tamam. 403 alırsan domain henüz doğrulanmamış.

### A2. Prod .env son hali

Sunucuda `nano /root/joryu/.env` — şunların HEPSİ dolu olmalı:

```
ENV=production                 # secure cookie'ler için şart
WAITLIST_ONLY=true             # lansman anına kadar true kalır
DATABASE_URL=...               # mevcut, dokunma
ADMIN_TOKEN=...                # mevcut, dokunma
SECRET_KEY=...                 # mevcut, dokunma — DEĞİŞTİRİRSEN herkesin oturumu düşer
RESEND_API_KEY=re_...          # Resend panelinden
MAIL_FROM=Joryu <noreply@joatolyesi.com>
BASE_URL=https://joatolyesi.com   # mail linkleri bunu kullanır, http/localhost KALMASIN
SENTRY_DSN=                    # A3'ten sonra doldur (opsiyonel ama önerilir)
LS_WEBHOOK_SECRET=             # A4'ten sonra
LS_CHECKOUT_URL_MONTHLY=       # A4'ten sonra
LS_CHECKOUT_URL_YEARLY=        # A4'ten sonra
```

Değişiklikten sonra: `docker compose up -d` (restart yeterli, build gerekmez).

### A3. Sentry (hata izleme)

1. https://sentry.io → ücretsiz hesap → Create Project → Platform: **FastAPI**
2. Verilen DSN'i `.env`'e `SENTRY_DSN=https://...` olarak ekle, restart.
3. Test: `docker compose exec app python -c "import sentry_sdk; from app.main import app; sentry_sdk.capture_message('lansman testi')"` → Sentry panelinde görünmeli.

### A4. Lemon Squeezy (Pro abonelik)

1. Store → Products: Aylık ($4.99/ay) ve Yıllık ($39/yıl) abonelik ürünleri.
   TR fiyat varyantı için TODO §3-10'a bak.
2. Her ürünün **Share → Buy Link**'ini kopyala → `.env`'e
   `LS_CHECKOUT_URL_MONTHLY` / `LS_CHECKOUT_URL_YEARLY`.
3. Settings → Webhooks → Add: URL `https://joatolyesi.com/webhooks/lemonsqueezy`,
   events: `subscription_created/updated/cancelled/expired`.
   Signing secret'ı `.env`'e `LS_WEBHOOK_SECRET=` olarak ekle.
4. Test mode'da bir satın alma yap; `/billing` sayfasında "aktif" görünmeli.
5. Lansmanda test mode'dan çıkmayı unutma (LS panelinden live'a al,
   linkler ve secret değişir — .env'i güncelle).

### A5. İçerik: kata videoları

- `https://joatolyesi.com/admin/katas?token=<ADMIN_TOKEN>` ekranından
  en azından aiki-jo + bokken setlerine kendi videolarını ekle.
- Video olmayan katalar "Video yakında" gösterir — rehber metinleri
  (/guide) her durumda erişilebilir.

### A6. Yedek + cron kontrolü

```bash
crontab -l                             # backup + prune cron'ları duruyor mu
/root/joryu/scripts/backup.sh          # elle bir kez çalıştır
ls -lh /root/backups/joryu/ | tail -3  # bugünün dump'ı var mı
```

---

## B. LANSMAN GÜNÜ (sıralı, ~15 dakika)

```bash
cd /root/joryu

# 1) Son kodu al, migration'larla birlikte aç
git pull
docker compose up -d --build
docker compose exec app alembic current    # en son revizyonda mı?

# 2) Uygulamayı aç
sed -i 's/WAITLIST_ONLY=true/WAITLIST_ONLY=false/' .env
docker compose up -d

# 3) Duman testi
curl -s -o /dev/null -w "%{http_code}\n" https://joatolyesi.com/register   # 200
curl -s -o /dev/null -w "%{http_code}\n" https://joatolyesi.com/login      # 200
# Tarayıcıdan: kayıt ol → doğrulama maili geldi mi → pratik kaydet → kuşak göründü mü

# 4) Waitlist davetleri — önce dry-run, sonra gerçek gönderim
docker compose exec app python scripts/send_invites.py          # kaç kişi, kimler
docker compose exec app python scripts/send_invites.py --yes    # GÖNDERİR

# 5) Sosyal duyurular (linkler kanal bazlı takip için):
#    Instagram: https://joatolyesi.com/?src=ig   YouTube: ?src=yt
#    LinkedIn:  ?src=li                          Twitter: ?src=tw
```

### Lansman sonrası ilk 48 saat kontrol listesi

- [ ] Sentry'de hata var mı? (özellikle 500'ler)
- [ ] `docker compose logs app --since 24h | grep -i error`
- [ ] Kayıt dönüşümü: kaç davet → kaç hesap
      (`SELECT count(*) FROM users;` + Resend panelinde açılma oranı)
- [ ] Doğrulama mailleri gidiyor mu (Resend → Logs)
- [ ] Disk/RAM: `df -h`, `free -m` (512MB droplet — swap kullanımına bak;
      şişiyorsa droplet'i $12'lik 1GB'a yükselt, 5 dk kesinti)
- [ ] Yedek cron'u o gece çalıştı mı

---

## C. Acil durumlar

**Site tamamen bozuldu →** eski statik sayfaya dön (DEPLOY.md "Geri alma"):
```bash
sudo cp ~/joatolyesi.com.nginx.bak /etc/nginx/sites-available/joatolyesi.com
sudo nginx -t && sudo systemctl reload nginx
```

**Uygulama ayakta ama hatalı →** önceki commit'e dön:
```bash
cd /root/joryu && git log --oneline -5     # sağlam commit'i seç
git checkout <commit> && docker compose up -d --build
```
(Migration geri almak gerekirse: `docker compose exec app alembic downgrade -1`)

**Mailler gitmiyor →** Resend Logs'a bak; domain doğrulaması düşmüş olabilir.
Uygulama mail hatasında ÇÖKMEZ, sadece loglar — acele etme.

**DB'yi yedekten dön →**
```bash
zcat /root/backups/joryu/joryu_<tarih>.sql.gz | docker compose exec -T db psql -U joryu -d joryu
```

---

## D. Hesap/anahtar envanteri

| Ne | Nerede | Not |
|---|---|---|
| Sunucu | DigitalOcean droplet (fra1, 512MB) | ssh root@... |
| DNS | DigitalOcean Networking | joatolyesi.com |
| SSL | Let's Encrypt / certbot | otomatik yenilenir, cron EKLEME |
| Mail | resend.com | domain doğrulaması şart |
| Ödeme | lemonsqueezy.com | test → live geçişini unutma |
| Hata izleme | sentry.io | DSN .env'de |
| Analytics | GA4 (G-54NX2S2Z01) | landing + app base'de |
| Kod | github.com/ilteriskeskin/joatolyesi.com | main dalı |
| Yedekler | /root/backups/joryu/ | ayda bir scp ile lokale kopyala |
