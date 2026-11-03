---
description: Joryu ekibinin bir sprintini baştan sona yürüt (PO → pazarlama/içerik → doğrulama → geliştirme → QA → rapor)
---

Joryu ekibinin bir sprintini yürüt. Çalışma düzeni `docs/team/README.md`'de;
kurallar orada ve `docs/team/CONTENT_STANDARDS.md`'de. Sen orkestratörsün:
işi alt agentlara (Agent tool, ilgili `subagent_type`) dağıt, çıktıları
birbirine aktar, kendin içerik uydurma.

1. **Hazırlık.** `git status` temiz değilse dur ve raporla (başkasının yarım işini ezme). `team/sprint-$(date +%F)` dalını aç: `main`'e merge edilmemiş bir önceki sprint dalı varsa onun üstünden, yoksa `main`'den (dallar zincirlenir; İlteriş en sonuncuyu merge edince hepsi gelir). Dal zaten varsa onu kullan.
2. **PO (`product-owner`).** Durumu teşhis etsin, BACKLOG'dan 1-3 iş seçip `docs/team/SPRINT.md`'yi yazsın. Önceki sprintin tamamlanmamış işleri varsa önce onlar.
3. **Uygulama.** SPRINT.md'deki işleri sahiplerine ver:
   - Pazarlama işleri → `growth-marketer`
   - İçerik işleri → `content-writer` → ardından **mutlaka** `fact-checker`
   - Kod işleri → `developer` (yalnız `content/verified/` içeriğiyle)
   Birbirinden bağımsız işleri paralel çalıştır.
4. **QA (`qa-reviewer`).** RED verirse bulguları `developer`'a geri ver ve en fazla 2 tur düzelt. Hâlâ RED ise o işi geri al (commit etme) ve rapora yaz.
5. **Commit.** Yalnız QA'dan GEÇTİ alan değişiklikleri ve `docs/team/` güncellemelerini anlamlı mesajlarla commit et. **Push etme, deploy etme.** `.env` asla commit edilmez.
6. **Rapor (`product-owner`).** `docs/team/reports/$(date +%F).md`: yapılanlar, dal adı, ölçülecek metrik, İlteriş'in onayı/aksiyonu gerekenler. BACKLOG'u güncelle. Bu raporu da commit et.
7. Son mesajında raporun 5 satırlık özetini ver.

$ARGUMENTS
