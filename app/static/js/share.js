// Paylaşım: tıklama anında (senkron) navigator.share() çağrılır — öncesinde
// hiçbir await yok, aksi halde iOS Safari kullanıcı etkileşimini kaybedip
// share() çağrısını sessizce reddeder. Desteklenmiyorsa küçük bir açılır
// menüye (X/WhatsApp) düşer. İndirme linki ayrı ve JS'e bağımlı değildir.
(function () {
  // GA4 share_card: yalnız yöntem + bağlam gönderilir (URL/kullanıcı adı yok)
  function trackShare(method) {
    const context = location.pathname.startsWith("/u/") ? "profile" : "dashboard";
    if (typeof window.joryuTrack === "function") window.joryuTrack("share_card", { method, context });
  }

  document.querySelectorAll("[data-share]").forEach((btn) => {
    btn.addEventListener("click", (ev) => {
      ev.preventDefault();
      const url = btn.dataset.shareUrl;
      const title = btn.dataset.shareTitle || "Joryu";
      const text = btn.dataset.shareText || "";

      if (navigator.share) {
        trackShare("native");
        navigator.share({ title, text, url }).catch(() => {
          // Kullanıcı iptal etti ya da tarayıcı reddetti — sessiz geç
        });
        return;
      }
      const menu = btn.parentElement.querySelector(".share-menu");
      if (menu) menu.classList.toggle("share-menu--open");
    });
  });

  // X / WhatsApp / indir linkleri: delegasyonla (HTMX ile yenilenen panelde de çalışır)
  document.addEventListener("click", (ev) => {
    const link = ev.target.closest && ev.target.closest("[data-share-method]");
    if (link) trackShare(link.dataset.shareMethod);
  });

  document.addEventListener("click", (ev) => {
    document.querySelectorAll(".share-menu--open").forEach((menu) => {
      if (!menu.parentElement.contains(ev.target)) menu.classList.remove("share-menu--open");
    });
  });
})();
