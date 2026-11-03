# Joryu Ekibi — Çalışma Düzeni

Joryu'yu (joatolyesi.com) büyütmek için çalışan yapay zeka ekibi. Ekip
haftada iki kez bir "sprint" yürütür; her sprint küçük, ölçülebilir bir
adım atar ve İlteriş'e onaylayacağı bir rapor bırakır.

## Ekip

| Rol | Agent | Ne yapar |
|---|---|---|
| Product Owner | `product-owner` | Metriklere bakar, backlog'u önceliklendirir, sprint hedefini yazar |
| Büyüme / Pazarlama | `growth-marketer` | SEO anahtar kelime araştırması, içerik takvimi, Instagram/YouTube/Reddit taslakları |
| İçerik Yazarı | `content-writer` | Kata/teknik/rehber/blog taslakları — her iddia için kaynak |
| Doğruluk Denetçisi | `fact-checker` | Her iddiayı kaynaktan doğrular; doğrulanmayan yayına giremez |
| Geliştirici | `developer` | Onaylı içeriği ve özellikleri koda geçirir (CLAUDE.md kurallarıyla) |
| QA | `qa-reviewer` | Testleri çalıştırır, diff'i inceler, son kapı |

## Sprint akışı (`/sprint` komutu)

1. **PO** → `METRICS.md`, `BACKLOG.md`, son raporu okur; `SPRINT.md`'ye bu sprintin hedefini ve 1-3 işini yazar.
2. **Pazarlama + İçerik** → işe göre araştırma/taslak üretir (`docs/team/marketing/`, `docs/team/content/drafts/`).
3. **Doğruluk denetçisi** → her içerik taslağını denetler, `docs/team/content/verified/`'e taşır ya da reddeder.
4. **Geliştirici** → yalnızca doğrulanmış içeriği ve PO'nun onayladığı işleri koda geçirir.
5. **QA** → `pytest` + diff incelemesi; geçmezse geliştiriciye geri döner.
6. Değişiklikler `team/sprint-YYYY-MM-DD` dalına commit edilir. **Push ve deploy yok.**
7. `reports/YYYY-MM-DD.md` raporu yazılır: ne yapıldı, ne ölçülecek, **İlteriş'in onayı gerekenler**.

## İlteriş'in rolü (haftada ~30 dk)

- Haftada bir GA4 rakamlarını `METRICS.md`'ye yapıştır (ya da ekran görüntüsünü sprint oturumuna ver).
- `reports/` altındaki son raporu oku; dalı incele, beğendiysen `main`'e merge et ve deploy et.
- Pazarlama taslaklarını (Instagram, YouTube vb.) kendin paylaş — ekip hiçbir yere gönderi atmaz.
- "Doğrulanamadı" listesindeki teknik bilgileri hoca/kaynak bilgisiyle onayla.

## Değişmez kurallar

- **Uydurma yok.** Sahte kullanıcı, sahte yorum/referans, uydurma istatistik, sahte seri/aktivite yok. Topluluk boş görünüyorsa boş görünür; çözüm gerçek kullanıcı getirmektir.
- **Kaynaksız teknik bilgi yayına girmez** (bkz. `CONTENT_STANDARDS.md`).
- **Push, deploy, prod sunucusuna erişim, dışarıya mesaj/gönderi yok.** Bunlar İlteriş'in işi.
- `CLAUDE.md` ve `BRIEF.md` kuralları geçerli; kapsam dışı büyük işler önce PO raporunda öneri olarak gelir.
