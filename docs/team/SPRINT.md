# Aktif Sprint — 2026-11-06

Dal: `team/sprint-2026-11-06` (`main`'den; önceki sprint dalları merge edilmiş). Push/deploy/prod erişimi yok, `.env` okunmaz.
Planlı (zamanlanmış) sprint; kullanım tasarrufu gereği tek iş. Plan tasarruf için orkestratör tarafından yazıldı (B-21 taslağı 2026-11-05'te hazırlandığı için BACKLOG sırasındaki sonraki iş B-22).

## İş

### B-22 Program e-posta dizisi (gün 1/3/7) — `developer` → `qa-reviewer`
Hipotez: Programa kaydolan ama ilk haftada bırakan kullanıcıya "kaldığın gün"e tek tıkla dönüş linki verilirse 7. gün tamamlama (`program_day_complete` day≥7) artar.
Not (orkestratör): B-27'deki günlük hatırlatma, hatırlatması açık kayıtlı kullanıcıya zaten "Bugün: Gün N" gönderiyor. B-22'nin farkı, geride kalan kişiye özel "kaldığın yerden devam" metni ve hatırlatması kapalı olanlara izin istemek.

Kapsam: Programa enroll olmuş, tamamlamamış kullanıcıya enroll'dan sonraki 1., 3. ve 7. günde, o gün program günü tamamlamadıysa bir kez e-posta: sıradaki tamamlanmamış güne link. Mevcut hatırlatma altyapısının (app/reminders.py, scripts/send_reminders.py) üzerine kurulur; aynı gün kişiye iki mail gitmez; tek tıkla çıkış ve hatırlatma tercihi geçerli. **Yalnız e-posta hatırlatması açık kullanıcıya gider** (izin; kapalı olan ile hiç seçmemiş olanı ayırt edemiyoruz). O gün dizi maili günlük hatırlatmanın yerine geçer. Hatırlatması kapalı kullanıcıya program gün sayfasında (enroll sonrası) B-27'deki tek tıkla açma kartı gösterilir; her dizi adımı bir kez gönderilir (idempotent). Yeni bağımlılık/servis yok. Mail içeriği yalnız ürün yapısı (gün no, hafta teması) — yeni teknik iddia yok.

## Başarı ölçütü
Testler yeşil (taze DB'de iki koşu). Ölçülecek metrik: 14 günde enroll edenlerin `program_day_complete` day≥3 ve day≥7 oranı (GA4).

## QA — B-22 (2026-11-06, qa-reviewer)

**Karar: GEÇTİ**

Testler: taze test Postgres'inde (`joryu-test-pg`) `pytest` iki kez art arda: 141 passed / 141 passed (tests/test_b22.py: 12 test). Migration `0012` downgrade 0011 -> upgrade head temiz; tek head. (Dolu/eski DB'de `test_flows.py::test_kata_hides_karate_taekwondo_but_keeps_data` seed kirliliğiyle düşebiliyor; B-22 ile ilgisiz, taze DB'de yeşil.)

Kontroller:
1. Gün 1/3/7 + idempotentlik: `app/reminders.py` `comeback_step` yalnız age in (1,3,7) ve age > last_comeback_step iken adım döner; script gönderimden SONRA işaretler (`scripts/send_reminders.py:38-42`), hata durumunda işaretlenmez. Tek `build_reminder` çağrısı -> aynı gün tek mail, dizi maili günlük hatırlatmanın yerine geçiyor. Push dizi maili kullanmıyor (test var).
2. Hatırlatması kapalı kullanıcı e-posta listesine hiç girmiyor (`main`, `User.reminders_enabled` filtresi); bugün pratik kaydedenler hariç. Test var.
3. Open redirect: `_reminder_return` `//evil.com`, `/programs//evil.com`, `https://evil.com`, `\`, `:` içeren, boş ve CR/LF'li girdilerde `/app`'e düşüyor; `/programs/../` aynı origin'de kaldığı için zararsız; CR/LF Location'da %0D%0A kodlanıyor. Açık yok. POST formlarında csrf_token mevcut.
4. Migration: `nullable=False, server_default="0"` mevcut satırları sorunsuz dolduruyor; downgrade drop_column.
5. i18n: `mail_comeback_subject/body` TR ve EN'de var, kart metinleri mevcut anahtarları kullanıyor.
6. Metinde sayı yalnız gün numarası; teknik iddia/sahte sayı yok. Odak yalnız program günü başlığı. Kaynak maliyeti: yeni servis/bağımlılık yok. Kapsam B-22 ile sınırlı (test_b27.py değişikliği yalnız `created_at=None` uyumu).

Düşük önemli notlar (RED değil):
- Gönderim başarılı + commit hatası arasında çökme olursa adım tekrar gönderilebilir (`scripts/send_reminders.py:38-42`); mail servisi idempotency anahtarı sunmadıkça kabul edilebilir.
- Cron o gün çalışmazsa 1/3/7 adımı tam gün eşleşmesi gerektiğinden atlanır (tasarım gereği "bir kez", telafi yok).
- "Kaldığın yerden devam" metni, programda geride kalmamış ama pratiği o gün yapmamış kullanıcıya da gider; sorun değil, yalnız ton notu.
