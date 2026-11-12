// GA4 olay yardımcısı. GA yüklenmediyse (adblock, admin sayfası) sessizce
// hiçbir şey yapmaz — konsola hata düşmez. Parametrelerde kişisel veri
// (e-posta, kullanıcı adı, id, not) gönderilmez; çağıranlar yalnız
// branş/dakika/kaynak gibi değerler verir.
(function () {
  function track(name, params) {
    if (typeof gtag !== "function") return;
    try {
      gtag("event", name, params || {});
    } catch (e) {
      // Analitik asla sayfayı bozmasın
    }
  }
  window.joryuTrack = track;

  // Dashboard pratik kaydı: sunucu başarılı POST'ta HX-Trigger başlığıyla
  // bu olayı tetikler (app/routers/practice.py)
  document.addEventListener("joryu:practice-logged", (ev) => {
    const d = ev.detail || {};
    track("practice_logged", { discipline: d.discipline, minutes: d.minutes, source: d.source });
  });

  // Basit tıklama olayı: data-track="olay_adı" taşıyan bağlantılar (ör. ipucu kartı)
  document.addEventListener("click", (ev) => {
    const el = ev.target.closest && ev.target.closest("[data-track]");
    if (el) track(el.getAttribute("data-track"));
  });
})();
