const CACHE = "joryu-v3";
const SHELL = [
  "/static/css/style.css",
  "/static/img/icon.svg",
  "/static/img/icon-192.png",
  "/static/img/icon-512.png",
  "/static/manifest.webmanifest",
  "/static/offline.html",
];

self.addEventListener("install", (event) => {
  event.waitUntil(caches.open(CACHE).then((cache) => cache.addAll(SHELL)));
  self.skipWaiting();
});

self.addEventListener("activate", (event) => {
  event.waitUntil(
    caches.keys().then((keys) =>
      Promise.all(keys.filter((k) => k !== CACHE).map((k) => caches.delete(k)))
    )
  );
  self.clients.claim();
});

// Sayfa gezintileri: her zaman network — ama bağlantı yoksa çıplak tarayıcı
// hatası yerine basit bir offline.html göster.
self.addEventListener("fetch", (event) => {
  if (event.request.mode === "navigate") {
    event.respondWith(
      fetch(event.request).catch(() => caches.match("/static/offline.html"))
    );
    return;
  }

  // Statik dosyalar: stale-while-revalidate — önce cache'ten sun, arkada
  // tazele. CSS/ikon güncellemeleri bir sonraki açılışta kendiliğinden gelir.
  const url = new URL(event.request.url);
  if (url.origin !== location.origin || !url.pathname.startsWith("/static/")) {
    return;
  }
  event.respondWith(
    caches.open(CACHE).then(async (cache) => {
      const cached = await cache.match(event.request);
      const network = fetch(event.request)
        .then((response) => {
          if (response.ok) cache.put(event.request, response.clone());
          return response;
        })
        .catch(() => cached);
      return cached || network;
    })
  );
});

// Web Push bildirimi
self.addEventListener("push", (event) => {
  let data = { title: "Joryu", body: "Bugünün pratiği seni bekliyor.", url: "/app" };
  try {
    if (event.data) data = { ...data, ...event.data.json() };
  } catch (e) { /* düz metinse varsayılanı kullan */ }
  event.waitUntil(
    self.registration.showNotification(data.title, {
      body: data.body,
      icon: "/static/img/icon-192.png",
      badge: "/static/img/icon-192.png",
      data: { url: data.url },
    })
  );
});

self.addEventListener("notificationclick", (event) => {
  event.notification.close();
  const url = event.notification.data && event.notification.data.url || "/app";
  event.waitUntil(
    clients.matchAll({ type: "window" }).then((list) => {
      for (const c of list) {
        if (c.url.includes(url) && "focus" in c) return c.focus();
      }
      if (clients.openWindow) return clients.openWindow(url);
    })
  );
});
