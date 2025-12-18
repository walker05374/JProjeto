// sw.js -PWABuilder
const CACHE_NAME = "jornada-maternal-v1";
const urlsToCache = [
  "/",
  "/static/images/inicio.png",
  "/offline/" // rota simples de fallback
];

self.addEventListener("install", (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      return cache.addAll(urlsToCache);
    })
  );
});

self.addEventListener("fetch", (event) => {
  event.respondWith(
    caches.match(event.request).then((response) => {
      return response || fetch(event.request);
    })
  );
});