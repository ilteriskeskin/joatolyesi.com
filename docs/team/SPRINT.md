# Aktif Sprint — 2026-11-12

Dal: `team/sprint-2026-11-12` (`main`'den; 08–11 dalları merge edildi). Push, deploy ve prod erişimi yok, `.env` okunmaz.
Planlı sprint, tek iş. Planı orkestratör yazdı, 11 raporundaki "Sonraki" önerisini izledi.

## İş: B-31 Günün ipucu — `developer` → `qa-reviewer`

- `app/tips_content.py`'ye `docs/team/content/verified/2026-11-11-gunun-ipucu-denetimi.md`'deki DÜZELT metinleri aynen uygulanır.
- #10 (Dokkōdō 1. madde) Japonca edisyondan teyit edilmedi ve İlteriş teyit vermedi → kural gereği **kaldırılır**.
- Dashboard'da günlük dönen tek ipucu kartı (tarihe göre deterministik seçim; aynı gün herkes aynı ipucunu görür). Kaynak etiketi gösterilir.
- Yeni metin üretilmez; yalnız doğrulanmış içerik.

## Başarı ölçütü
Testler yeşil; dashboard'da kart görünür; ölçüm: dashboard dönüşü (ipucu kartı tıklama/görüntülenme GA olayı varsa).

## Sonuç
Developer uyguladı, QA GEÇTİ verdi (0c8cae9). DB'li `test_dashboard_renders_tip_card` Docker kapalı olduğu için atlandı.
