/* Service Worker: listens for push events and shows notifications */
self.addEventListener('push', function(event) {
    let data = {};
    try { data = event.data ? event.data.json() : {}; } catch (e) { data = { body: event.data ? event.data.text() : '' }; }

    const title = data.title || 'HelpReach';
    const options = {
        body: data.body || '',
        icon: '/img/handmade.avif',
        data: { url: data.url || '/' }
    };

    event.waitUntil(self.registration.showNotification(title, options));
});

self.addEventListener('notificationclick', function(event) {
    event.notification.close();
    const url = event.notification.data && event.notification.data.url ? event.notification.data.url : '/';
    event.waitUntil(clients.matchAll({ type: 'window' }).then(windowClients => {
        for (let client of windowClients) {
            if (client.url === url && 'focus' in client) return client.focus();
        }
        if (clients.openWindow) return clients.openWindow(url);
    }));
});
