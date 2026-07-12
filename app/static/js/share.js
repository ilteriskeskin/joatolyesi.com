// Paylaşım: tıklama anında (senkron) navigator.share() çağrılır — öncesinde
// hiçbir await yok, aksi halde iOS Safari kullanıcı etkileşimini kaybedip
// share() çağrısını sessizce reddeder. Desteklenmiyorsa küçük bir açılır
// menüye (X/WhatsApp) düşer. İndirme linki ayrı ve JS'e bağımlı değildir.
(function () {
  document.querySelectorAll("[data-share]").forEach((btn) => {
    btn.addEventListener("click", (ev) => {
      ev.preventDefault();
      const url = btn.dataset.shareUrl;
      const title = btn.dataset.shareTitle || "Joryu";
      const text = btn.dataset.shareText || "";

      if (navigator.share) {
        navigator.share({ title, text, url }).catch(() => {
          // Kullanıcı iptal etti ya da tarayıcı reddetti — sessiz geç
        });
        return;
      }
      const menu = btn.parentElement.querySelector(".share-menu");
      if (menu) menu.classList.toggle("share-menu--open");
    });
  });

  document.addEventListener("click", (ev) => {
    document.querySelectorAll(".share-menu--open").forEach((menu) => {
      if (!menu.parentElement.contains(ev.target)) menu.classList.remove("share-menu--open");
    });
  });
})();
