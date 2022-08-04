const CACHE_NAME = "wq-cache-v1";

// App Version 0.0.0

const cacheUrls = ["/../input/test.js"];

self.addEventListener("install", event => {
    event.waitUntil(
        caches
            .open(CACHE_NAME)
            .then(cache =>
                cache.addAll(
                    cacheUrls.map(
                        url => new Request(url, { cache: "no-cache" })
                    )
                )
            )
            .then(() => self.skipWaiting())
    );
});

self.addEventListener("fetch", event => {
    if (!cacheUrls.includes(new URL(event.request.url).pathname)) {
        return;
    }
    event.respondWith(
        new Promise((resolve, reject) => {
            const timeout = setTimeout(reject, 400);
            fetch(event.request, { cache: "no-cache" }).then(response => {
                clearTimeout(timeout);
                const cacheResponse = response.clone();
                caches
                    .open(CACHE_NAME)
                    .then(cache => cache.put(event.request, cacheResponse));
                resolve(response);
            }, reject);
        }).catch(() => {
            return caches
                .open(CACHE_NAME)
                .then(cache => cache.match(event.request, { ignoreVary: true }))
                .then(response => response || Promise.reject("no-match"));
        })
    );
});
