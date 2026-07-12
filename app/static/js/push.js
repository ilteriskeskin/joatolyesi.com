// Bildirim aç/kapa butonu: izin iste, PushManager'a abone ol, sunucuya kaydet.
(function () {
  const btn = document.querySelector("[data-push-enable]");
  if (!btn || !("serviceWorker" in navigator) || !("PushManager" in window)) return;

  function urlBase64ToUint8Array(base64) {
    const padding = "=".repeat((4 - (base64.length % 4)) % 4);
    const base64Safe = (base64 + padding).replace(/-/g, "+").replace(/_/g, "/");
    const raw = atob(base64Safe);
    return Uint8Array.from([...raw].map((c) => c.charCodeAt(0)));
  }

  function csrfToken() {
    return document.cookie.split("; ").find((c) => c.startsWith("csrf="))?.split("=")[1] || "";
  }

  async function post(path, params) {
    const body = new URLSearchParams({ ...params, csrf_token: csrfToken() });
    await fetch(path, { method: "POST", body });
  }

  async function subscribe() {
    const reg = await navigator.serviceWorker.ready;
    const existing = await reg.pushManager.getSubscription();
    if (existing) return existing;

    const permission = await Notification.requestPermission();
    if (permission !== "granted") return null;

    const res = await fetch("/push/vapid-public-key");
    const { key } = await res.json();
    if (!key) return null;

    return reg.pushManager.subscribe({
      userVisibleOnly: true,
      applicationServerKey: urlBase64ToUint8Array(key),
    });
  }

  async function refreshButtonState() {
    const reg = await navigator.serviceWorker.ready;
    const sub = await reg.pushManager.getSubscription();
    btn.textContent = sub ? btn.dataset.labelOn : btn.dataset.labelOff;
    btn.classList.toggle("push-btn--active", !!sub);
  }

  btn.addEventListener("click", async () => {
    const reg = await navigator.serviceWorker.ready;
    const existing = await reg.pushManager.getSubscription();
    if (existing) {
      await post("/push/unsubscribe", { endpoint: existing.endpoint });
      await existing.unsubscribe();
    } else {
      const sub = await subscribe();
      if (sub) {
        const json = sub.toJSON();
        await post("/push/subscribe", {
          endpoint: json.endpoint,
          p256dh: json.keys.p256dh,
          auth: json.keys.auth,
        });
      }
    }
    refreshButtonState();
  });

  refreshButtonState();
})();
