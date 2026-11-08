# Aktif Sprint — 2026-11-08

Dal: `team/sprint-2026-11-08` (`main`'den; önceki sprint dalları merge edildi). Push/deploy/prod erişimi yok, `.env` okunmaz.
Planlı sprint; kullanım tasarrufu gereği tek pazarlama/içerik turu, kod işi yok. Plan orkestratör tarafından yazıldı (BACKLOG önerilen sırası: B-35 kalan → B-32).

## İş: B-35 kalan — B-21 kampanya taslağını yeni çerçeveye uyarla — `growth-marketer` → `fact-checker`

Hipotez: Instagram kampanyası "hocan yoksa buradan, temelden başla; topluluk yanında" çerçevesiyle ve sitedeki program metinleriyle aynı dili konuşursa, hocası olmayan ziyaretçinin `sign_up` → `program_enroll` dönüşümü artar.

Kapsam (yalnız taslak; site kodu değişmez, hiçbir yere gönderi atılmaz):
- `docs/team/marketing/2026-11-05-30-gun-jo-kampanyasi.md` güncellenir: eski "hocandan öğrenmiş olmalısın / hocasız denmez" ifadeleri kaldırılır; bio, takvim, pin yorumlar, DM şablonu yeni çerçeveye.
- Program tavsiyeleri (her hareket en az 10 tekrar; önce temel vuruşlar, katalar program bitince) İlteriş'in tavsiyesi olarak geçer; sayaç/kilit vaadi yok.
- Güvenlik notu (ısın, yavaş başla, ağrıda dur) korunur. "Hocaya gerek yok" vaadi verilmez. Sahte kullanıcı/istatistik/yorum yok.
- Metinler sitedeki doğrulanmış metinlerle (`docs/team/content/verified/2026-11-07-ogrenme-yolu-metinleri.md`) tutarlı.
- fact-checker teknik/olgusal iddiaları ve çerçeve uyumunu denetler.

## Başarı ölçütü
fact-checker ONAY. Metrik (kampanya yayınından 14 gün, GA4): `sign_up` (utm_source=instagram), `program_enroll`, `program_day_complete` day≥7.
