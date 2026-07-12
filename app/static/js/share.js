// Paylaşım: Web Share API (mobilde native paylaşım sayfası, görsel dahil)
// desteklenmiyorsa doğrudan platform linklerine düşer.
(function () {
  document.querySelectorAll("[data-share]").forEach((el) => {
    el.addEventListener("click", async (ev) => {
      ev.preventDefault();
      const url = el.dataset.shareUrl;
      const title = el.dataset.shareTitle || "Joryu";
      const text = el.dataset.shareText || "";
      const imageUrl = el.dataset.shareImage;

      if (navigator.share) {
        try {
          const shareData = { title, text, url };
          if (imageUrl && navigator.canShare) {
            try {
              const resp = await fetch(imageUrl);
              const blob = await resp.blob();
              const file = new File([blob], "joryu-card.png", { type: blob.type });
              if (navigator.canShare({ files: [file] })) shareData.files = [file];
            } catch (e) { /* görsel çekilemedi, linkle paylaş */ }
          }
          await navigator.share(shareData);
          return;
        } catch (e) {
          if (e.name === "AbortError") return; // kullanıcı iptal etti
        }
      }
      const menu = el.nextElementSibling;
      if (menu && menu.classList.contains("share-menu")) {
        menu.classList.toggle("share-menu--open");
      }
    });
  });
})();
