// Bildirim aç/kapa butonu: izin iste, PushManager'a abone ol, sunucuya kaydet.
// Her adımda kullanıcıya görünür geri bildirim verir — sessizce hiçbir şey
// yapmadan durmaz (VAPID yapılandırılmamışsa, izin reddedilirse vb.).
(function () {
  const btn = document.querySelector("[data-push-enable]");
  const status = document.querySelector("[data-push-status]");
  if (!btn) return;

  function setStatus(text) {
    if (status) status.textContent = text;
  }

  if (!("serviceWorker" in navigator) || !("PushManager" in window)) {
    btn.disabled = true;
    setStatus(btn.dataset.msgUnsupported);
    return;
  }

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
    const res = await fetch(path, { method: "POST", body });
    return res.ok;
  }

  async function subscribe() {
    if (Notification.permission === "denied") {
      setStatus(btn.dataset.msgDenied);
      return null;
    }
    const permission = await Notification.requestPermission();
    if (permission !== "granted") {
      setStatus(btn.dataset.msgDenied);
      return null;
    }

    const res = await fetch("/push/vapid-public-key");
    const { key } = await res.json();
    if (!key) {
      setStatus(btn.dataset.msgUnconfigured);
      return null;
    }

    const reg = await navigator.serviceWorker.ready;
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
    setStatus("");
    btn.disabled = true;
    try {
      const reg = await navigator.serviceWorker.ready;
      const existing = await reg.pushManager.getSubscription();
      if (existing) {
        await post("/push/unsubscribe", { endpoint: existing.endpoint });
        await existing.unsubscribe();
        setStatus(btn.dataset.msgOff);
      } else {
        const sub = await subscribe();
        if (sub) {
          const json = sub.toJSON();
          const ok = await post("/push/subscribe", {
            endpoint: json.endpoint,
            p256dh: json.keys.p256dh,
            auth: json.keys.auth,
          });
          setStatus(ok ? btn.dataset.msgOn : btn.dataset.msgError);
        }
      }
    } catch (e) {
      setStatus(btn.dataset.msgError);
    }
    btn.disabled = false;
    refreshButtonState();
  });

  refreshButtonState();

  // Bağlamsal "yumuşak soru" kartı: sunucu yalnız ilk pratik kaydından sonra
  // (gizli olarak) render eder. İzin penceresi YALNIZ "Hatırlatmayı aç"
  // tıklamasında açılır (mevcut butonun akışı tetiklenir); sayfa açılışında
  // Notification.requestPermission çağrılmaz.
  const prompt = document.querySelector("[data-push-prompt]");
  if (!prompt) return;
  const DISMISS_KEY = "joryu_push_prompt_dismissed";

  function track(name) {
    if (typeof window.joryuTrack === "function") window.joryuTrack(name, {});
  }
  function storage(fn) {
    try {
      return fn(window.localStorage);
    } catch (e) {
      return null; // localStorage kapalıysa kart her açılışta çıkabilir; ısrar riski yok sayılır
    }
  }
  function hidePrompt(remember) {
    prompt.hidden = true;
    if (remember) storage((ls) => ls.setItem(DISMISS_KEY, "1"));
  }

  (async function maybeShowPrompt() {
    if (!("Notification" in window) || Notification.permission !== "default") return;
    if (storage((ls) => ls.getItem(DISMISS_KEY))) return;
    try {
      const reg = await navigator.serviceWorker.ready;
      if (await reg.pushManager.getSubscription()) return;
    } catch (e) {
      return;
    }
    prompt.hidden = false;
    track("push_prompt_shown");
  })();

  const accept = prompt.querySelector("[data-push-prompt-accept]");
  const dismiss = prompt.querySelector("[data-push-prompt-dismiss]");
  if (accept) {
    accept.addEventListener("click", () => {
      track("push_prompt_accept");
      hidePrompt(true);
      btn.click(); // kullanıcı tıklaması içinde: izin penceresi burada açılır
    });
  }
  if (dismiss) {
    dismiss.addEventListener("click", () => {
      track("push_prompt_dismiss");
      hidePrompt(true);
    });
  }
})();
