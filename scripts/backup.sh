#!/usr/bin/env bash
# Günlük Postgres yedeği: pg_dump -> gzip -> tarihli dosya, son 14 yedek tutulur.
# Cron'dan root olarak çalıştırılır; compose projesi APP_DIR altında olmalı.
set -euo pipefail

APP_DIR="${APP_DIR:-/root/joryu}"
BACKUP_DIR="${BACKUP_DIR:-/root/backups/joryu}"
KEEP=14

mkdir -p "$BACKUP_DIR"

# .env'den kullanıcı/db adını al
set -a
source "$APP_DIR/.env"
set +a

STAMP=$(date +%Y-%m-%d_%H%M)
FILE="$BACKUP_DIR/joryu_${STAMP}.sql.gz"

docker compose --project-directory "$APP_DIR" exec -T db \
  pg_dump -U "$POSTGRES_USER" -d "$POSTGRES_DB" | gzip > "$FILE"

# Boş dump'a karşı kontrol
[ -s "$FILE" ] || { echo "HATA: yedek dosyası boş: $FILE" >&2; exit 1; }

# En yenisinden KEEP adet kalsın, gerisi silinsin
ls -1t "$BACKUP_DIR"/joryu_*.sql.gz | tail -n +$((KEEP + 1)) | xargs -r rm -f

echo "OK: $FILE ($(du -h "$FILE" | cut -f1))"
