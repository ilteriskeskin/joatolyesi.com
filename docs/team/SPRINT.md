# Aktif Sprint — 2026-11-16

Dal: `team/sprint-2026-11-16` (`team/sprint-2026-11-15` üstünden; o dal henüz merge edilmedi). Push, deploy ve prod erişimi yok, `.env` okunmaz.
Planlı sprint. Plan BACKLOG sırasını izler: B-41a kod. Planı orkestratör yazdı (kullanım tasarrufu).

## İş 1: B-41a kod — program seçimi + bokken programı + seed düzeltmesi — `developer` → `qa-reviewer`
Yalnız onaylı içerik: `docs/team/content/verified/2026-11-15-30-gun-bokken-programi.md`.
- `/programs` dizini: mevcut programları listeler (jo, bokken); kullanıcı birini başlatır. Aynı anda bir aktif program; istediği zaman değiştirebilir (eski ilerleme silinmez).
- Bokken 30 gün programı onaylı metinle (TR/EN) seed'e girer; jo programı ve `30-day-jo-suburi` davranışı bozulmaz.
- `app/seed.py` bokken `aiki-ken-suburi-3/5/6/7` metinleri onaylı belgenin 4. bölümündeki metinlerle değişir; `audit-log.md` satırı "düzeltildi" olur.
- B-33 kuralları: ≥10 tekrar ve "önce temel" yalnız tavsiye; sayaç/kilit yok. Kumitachi yok.
- Testler: yeni akış için test eklenir, tüm test paketi geçer.

## Başarı ölçütü
Deploy sonrası 4 hafta: bokken programına başlayan kullanıcı sayısı.

## Sonuç
İş 1: QA GEÇTİ (161 test geçti; migration 0013 upgrade/downgrade denendi). Aiki-ken suburi 3/5/6/7 EN çevirilerine fact-checker ONAY verdi. Commit `f706451`. Kapsam dışı kalanlar: suburi 2/4 ve shomen suburi metinleri belgeyle birebir değil; bokken için landing/dashboard kartı yok.
