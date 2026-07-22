/* Service worker: makes the map usable offline after the first visit.
   - App shell (same-origin) is precached on install.
   - Everything else (Leaflet/esri CDN, basemap tiles, the live FMZ boundary
     service) is cached on first use with a stale-while-revalidate strategy,
     so a previously loaded map keeps working without a connection.
   Note: service workers only run over http(s) (e.g. GitHub Pages), not from a
   file:// path. */
const CACHE = 'onfish-v0.77';
const SHELL = ['./', './index.html', './manifest.json', './icon-192.png', './icon-512.png'];

self.addEventListener('install', e => {
  e.waitUntil(caches.open(CACHE).then(c => c.addAll(SHELL)).then(() => self.skipWaiting()));
});

self.addEventListener('activate', e => {
  e.waitUntil(
    caches.keys()
      .then(keys => Promise.all(keys.filter(k => k !== CACHE).map(k => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', e => {
  if (e.request.method !== 'GET') return;
  e.respondWith(caches.open(CACHE).then(async cache => {
    const cached = await cache.match(e.request);
    const network = fetch(e.request)
      .then(resp => {
        if (resp && (resp.ok || resp.type === 'opaque')) cache.put(e.request, resp.clone());
        return resp;
      })
      .catch(() => cached);
    return cached || network;   // serve cache first, refresh in background
  }));
});
