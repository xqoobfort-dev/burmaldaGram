const CACHE_NAME = 'burmaldagram-v1';

// Активуємо фоновий режим
self.addEventListener('install', (event) => {
    self.skipWaiting();
});

self.addEventListener('activate', (event) => {
    event.waitUntil(self.clients.claim());
});

// Обробка фонових push-сповіщень від сервера
self.addEventListener('push', (event) => {
    const data = event.data ? event.data.json() : { title: 'Нове повідомлення', body: 'Перевірте чат!' };
    
    const options = {
        body: data.body,
        icon: 'https://flaticon.com',
        badge: 'https://flaticon.com',
        vibrate: [100, 50, 100],
        data: { url: '/' }
    };

    event.waitUntil(
        self.registration.showNotification(data.title, options)
    );
});

// Клік по сповіщенню відкриває чат
self.addEventListener('notificationclick', (event) => {
    event.notification.close();
    event.waitUntil(
        clients.openWindow(event.notification.data.url)
    );
});

