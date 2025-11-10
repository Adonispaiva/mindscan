// ===============================================================
//  SERVICE WORKER — MINDSCAN SYNMIND MI v2.0
//  Autor: Leo Vinci (GPT Inovexa)
//  Data: 07/11/2025
//  Função: Cache inteligente, modo offline e atualização automática
// ===============================================================

const CACHE_NAME = "mindscan-cache-v2.0";
const APP_SHELL = [
  "/",
  "/index.html",
  "/favicon.ico",
  "/manifest.json",
  "/assets/",
  "/src/",
];

// ---------------------------------------------------------------
// INSTALAÇÃO — Cria cache inicial (app shell)
// ---------------------------------------------------------------
self.addEventListener("install", (event) => {
  event.waitUntil(
    caches
      .open(CACHE_NAME)
      .then((cache) => cache.addAll(APP_SHELL))
      .then(() => self.skipWaiting())
  );
  console.log("[MindScan SW] Instalado e cache inicial criado.");
});

// ---------------------------------------------------------------
// ATIVAÇÃO — Limpa caches antigos
// ---------------------------------------------------------------
self.addEventListener("activate", (event) => {
  event.waitUntil(
    caches.keys().then((keys) =>
      Promise.all(
        keys.map((key) => {
          if (key !== CACHE_NAME) {
            console.log("[MindScan SW] Removendo cache antigo:", key);
            return caches.delete(key);
          }
        })
      )
    )
  );
  self.clients.claim();
  console.log("[MindScan SW] Ativo e pronto.");
});

// ---------------------------------------------------------------
// FETCH — Estratégia cache-first com fallback à rede
// ---------------------------------------------------------------
self.addEventListener("fetch", (event) => {
  if (event.request.method !== "GET") return;

  event.respondWith(
    caches.match(event.request).then((cachedResponse) => {
      const fetchPromise = fetch(event.request)
        .then((networkResponse) => {
          if (!networkResponse || networkResponse.status !== 200) {
            return networkResponse;
          }

          caches.open(CACHE_NAME).then((cache) =>
            cache.put(event.request, networkResponse.clone())
          );

          return networkResponse;
        })
        .catch(() => cachedResponse || new Response("Offline", { status: 503 }));

      return cachedResponse || fetchPromise;
    })
  );
});

// ---------------------------------------------------------------
// MENSAGENS — Força atualização quando nova versão é detectada
// ---------------------------------------------------------------
self.addEventListener("message", (event) => {
  if (event.data && event.data.type === "SKIP_WAITING") {
    self.skipWaiting();
    console.log("[MindScan SW] Atualização forçada via mensagem.");
  }
});
