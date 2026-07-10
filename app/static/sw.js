const CACHE = "joryu-v2";
const SHELL = [
  "/static/css/style.css",
  "/static/img/icon.svg",
  "/static/img/icon-192.png",
  "/static/img/icon-512.png",
  "/static/manifest.webmanifest",
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

// Statik dosyalar: stale-while-revalidate — önce cache'ten sun, arkada
// tazele. CSS/ikon güncellemeleri bir sonraki açılışta kendiliğinden gelir.
// Sayfalar: network, dokunma.
self.addEventListener("fetch", (event) => {
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
