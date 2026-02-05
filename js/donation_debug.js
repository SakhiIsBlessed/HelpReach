// Debug helper to force the donation flybox independently of main.js
(function () {
    function escapeHtml(str) { return String(str || '').replace(/[&<>"']/g, function (m) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": "&#39;" }[m]; }); }
    function showFlyBox(donation) {
        try {
            const el = document.createElement('div'); el.className = 'hr-flybox';
            const img = donation.photo_filename ? `<img src="/uploads/donations/${donation.photo_filename}" alt="img">` : `<div style="width:56px;height:56px;border-radius:8px;background:#f1f3f5;display:flex;align-items:center;justify-content:center;color:#999">📦</div>`;
            el.innerHTML = `${img}<div class="title">${escapeHtml(donation.title || 'New donation')}</div>`;
            document.body.appendChild(el);
            // animate after short delay (3s for debug)
            setTimeout(() => { el.classList.add('rising'); const heart = document.createElement('div'); heart.className = 'hr-heart'; heart.innerHTML = '❤'; document.body.appendChild(heart); setTimeout(() => heart.classList.add('show'), 40); setTimeout(() => { try { heart.remove(); } catch (e) { }; try { el.remove(); } catch (e) { } }, 1200); }, 3000);
        } catch (e) { console.error('donation_debug.showFlyBox error', e); }
    }
    try {
        if (typeof window.hr_forceDonationTest === 'function') {
            console.info('hr_forceDonationTest already provided by main script; leaving it intact');
        } else {
            // Define a simple helper that attempts to use the main flybox if available
            window.hr_forceDonationTest = function () {
                if (typeof window.hr_forceDonationTest === 'function' && window.hr_forceDonationTest !== arguments.callee) {
                    // Shouldn't happen; safety check
                }
                try {
                    // If main's showFlyBox exists in global scope (rare), call it
                    if (typeof window.showFlyBox === 'function') {
                        window.showFlyBox({ id: 'debug-manual', title: 'Manual test donation' });
                    } else {
                        // Fallback: create a visible flybox compatible with main.css
                        const s = document.createElement('div'); s.className = 'hr-flybox'; s.innerHTML = `<div class="title">Manual test donation</div>`; document.body.appendChild(s); setTimeout(() => s.classList.add('show'), 25);
                        setTimeout(() => { try { s.remove(); } catch (e) { } }, 10000);
                    }
                    console.info('hr_forceDonationTest executed (debug fallback)');
                } catch (err) { console.error('hr_forceDonationTest error', err); }
            };
        }
    } catch (e) { console.error('Failed to create hr_forceDonationTest', e); }
})();
