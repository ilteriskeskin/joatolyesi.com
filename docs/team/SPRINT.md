# Aktif Sprint — 2026-11-07

Dal: `team/sprint-2026-11-07` (`team/sprint-2026-11-06` üstünden; o dal merge bekliyor). Push/deploy/prod erişimi yok, `.env` okunmaz.
Planlı sprint; kullanım tasarrufu gereği tek içerik turu. Plan orkestratör tarafından yazıldı (BACKLOG önerilen sırası: B-33 + B-35).

## İş: B-33 Program içi tavsiyeler + B-35 Konumlandırma metinleri — `content-writer` → `fact-checker` → `developer` → `qa-reviewer`

Hipotez: Hocası olmayan Instagram ziyaretçisine "buradan, temelden başla" denirse ve programın sonunda bir sonraki adım (katalar) gösterilirse program kaydı ve bitirme sonrası kata sayfası ziyareti artar.

Kapsam (yalnız metin + şablonda gösterim; yeni alan, sayaç, kilit, migration yok):
- Program açılış/detay sayfası: `program_dojo_note` yeni çerçeveye ("hocan yoksa buradan, temelden başla; topluluk yanında"), güvenlik notu korunur; "kimin için" + iki tavsiye (her hareketi en az 10 tekrar; önce temel vuruşlar, katalara program bitince).
- 1. gün sayfası: iki tavsiyenin kısa hali.
- Program bitiş mesajı: "Sırada katalar" → aiki-jo kata listesi linki.
- Landing hero alt metnine kısa ek (programa davet, temelden başla).
- TR + EN. Tavsiyeler İlteriş'in program tavsiyesi olarak yazılır; olgusal teknik iddia eklenmez.
- B-21 kampanya taslağı güncellemesi bu sprintte yok (sonraki).

## Başarı ölçütü
Testler yeşil. Metrik (14 gün, GA4): `program_enroll` / program sayfası görüntüleme; program bitirenlerin kata sayfası ziyareti.
