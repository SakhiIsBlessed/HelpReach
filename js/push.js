// Registers service worker, requests permission, subscribes for push, and sends subscription to backend
(function(){
    function urlBase64ToUint8Array(base64String) {
        const padding = '='.repeat((4 - base64String.length % 4) % 4);
        const base64 = (base64String + padding).replace(/-/g, '+').replace(/_/g, '/');
        const rawData = window.atob(base64);
        const outputArray = new Uint8Array(rawData.length);
        for (let i = 0; i < rawData.length; ++i) {
            outputArray[i] = rawData.charCodeAt(i);
        }
        return outputArray;
    }

    // backend origin — ensure requests go to Flask backend, not Live Server origin
    const BACKEND = window.BACKEND_URL || 'https://helpreach-production-0562.up.railway.app';

    if (!('serviceWorker' in navigator) || !('PushManager' in window)) {
        console.log('Push messaging not supported');
        return;
    }

    navigator.serviceWorker.register('/sw.js').then(async function(reg){
        console.log('Service Worker registered', reg);

        try {
            const res = await fetch(BACKEND + '/api/vapid_public_key');
            const data = await res.json();
            if (!data.publicKey) {
                console.warn('VAPID public key not available from server');
                return;
            }

            const permission = await Notification.requestPermission();
            if (permission !== 'granted') {
                console.log('Notification permission not granted');
                return;
            }

            const sub = await reg.pushManager.subscribe({
                userVisibleOnly: true,
                applicationServerKey: urlBase64ToUint8Array(data.publicKey)
            });

            // send subscription to server
            await fetch(BACKEND + '/api/subscribe', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(sub)
            });

            console.log('Push subscription successful');
        } catch (err) {
            console.error('Push subscription error', err);
        }
    }).catch(function(err){ console.error('SW register failed', err); });
})();
