// Ana ekrana ekleme banner'ı: Android/Chrome'da gerçek install prompt'unu
// tetikler; iOS Safari'de (beforeinstallprompt hiç yok) elle talimat
// gösterir. Kullanıcı kapatırsa bir daha gösterilmez (localStorage).
(function () {
  // GA4 pwa_install: yalnız tarayıcının "appinstalled" olayıyla, bir kez.
  // Banner kapatılmış olsa da (menüden yükleme) sayılsın diye en başta.
  // iOS Safari bu olayı hiç vermez; oradaki yüklemeler ölçülemez.
  window.addEventListener("appinstalled", () => {
    if (typeof window.joryuTrack === "function") window.joryuTrack("pwa_install");
  });

  const DISMISS_KEY = "joryu_install_dismissed";
  if (localStorage.getItem(DISMISS_KEY)) return;

  const isStandalone =
    window.matchMedia("(display-mode: standalone)").matches ||
    window.navigator.standalone === true;
  if (isStandalone) return;

  const isIOS = /iphone|ipad|ipod/i.test(navigator.userAgent);
  let deferredPrompt = null;

  function buildBanner(onInstall, message, showInstallButton) {
    const bar = document.createElement("div");
    bar.className = "install-bar";
    bar.innerHTML = `
      <span class="install-bar__text">${message}</span>
      ${showInstallButton ? '<button type="button" class="install-bar__install">Yükle</button>' : ""}
      <button type="button" class="install-bar__close" aria-label="Kapat">&times;</button>
    `;
    document.body.appendChild(bar);
    bar.querySelector(".install-bar__close").addEventListener("click", () => {
      localStorage.setItem(DISMISS_KEY, "1");
      bar.remove();
    });
    if (showInstallButton) {
      bar.querySelector(".install-bar__install").addEventListener("click", async () => {
        if (onInstall) await onInstall();
        localStorage.setItem(DISMISS_KEY, "1");
        bar.remove();
      });
    }
  }

  if (isIOS) {
    // iOS'ta programatik prompt yok — Safari paylaş menüsüne yönlendir
    buildBanner(
      null,
      "Bu uygulamayı ana ekranına eklemek için Paylaş (⬆) simgesine, sonra \"Ana Ekrana Ekle\"ye dokun.",
      false
    );
    return;
  }

  window.addEventListener("beforeinstallprompt", (event) => {
    event.preventDefault();
    deferredPrompt = event;
    buildBanner(
      async () => {
        if (!deferredPrompt) return;
        deferredPrompt.prompt();
        await deferredPrompt.userChoice;
        deferredPrompt = null;
      },
      "Joryu'yu ana ekranına ekle, normal bir uygulama gibi kullan.",
      true
    );
  });
})();
