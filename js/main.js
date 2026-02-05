(function ($) {
    "use strict";

    // Spinner
    var spinner = function () {
        setTimeout(function () {
            if ($('#spinner').length > 0) {
                $('#spinner').removeClass('show');
            }
        }, 1);
    };
    spinner();


    // Initiate the wowjs (guarded) — avoid runtime error if library missing
    if (typeof WOW !== 'undefined') {
        try { new WOW().init(); } catch (e) { console.debug('WOW init error', e); }
    } else {
        console.debug('WOW is not available; skipping init');
    }


    // Fixed Navbar
    $(window).scroll(function () {
        if ($(window).width() < 992) {
            if ($(this).scrollTop() > 45) {
                $('.fixed-top').addClass('bg-white shadow');
            } else {
                $('.fixed-top').removeClass('bg-white shadow');
            }
        } else {
            if ($(this).scrollTop() > 45) {
                $('.fixed-top').addClass('bg-white shadow').css('top', -45);
            } else {
                $('.fixed-top').removeClass('bg-white shadow').css('top', 0);
            }
        }
    });


    // Back to top button
    $(window).scroll(function () {
        if ($(this).scrollTop() > 300) {
            $('.back-to-top').fadeIn('slow');
        } else {
            $('.back-to-top').fadeOut('slow');
        }
    });
    $('.back-to-top').click(function () {
        $('html, body').animate({ scrollTop: 0 }, 1500, 'easeInOutExpo');
        return false;
    });


    // Testimonials carousel
    $(".testimonial-carousel").owlCarousel({
        autoplay: true,
        smartSpeed: 1000,
        margin: 25,
        loop: true,
        center: true,
        dots: false,
        nav: true,
        navText: [
            '<i class="bi bi-chevron-left"></i>',
            '<i class="bi bi-chevron-right"></i>'
        ],
        responsive: {
            0: {
                items: 1
            },
            768: {
                items: 2
            },
            992: {
                items: 3
            }
        }
    });

    // Set current year in footer
    document.addEventListener('DOMContentLoaded', function () {
        var yearElement = document.getElementById('year');
        if (yearElement) {
            yearElement.textContent = new Date().getFullYear();
        }
    });


})(jQuery);

// Active donation popup: fetch latest donation and show animated popup
(function () {
    // Minimal flybox-only implementation.
    function injectStyles() {
        const css = `
        .hr-flybox{position:fixed;left:18px;bottom:76px;background:#fff;border-radius:20px;box-shadow:0 6px 18px rgba(0,0,0,0.12);padding:8px 14px;display:inline-flex;align-items:center;gap:10px;z-index:999999;transition:transform 0.28s ease,opacity 0.28s ease;opacity:0;transform:translateX(-18px) translateY(8px);min-width:120px;max-width:360px}
        .hr-flybox.show{opacity:1;transform:translateX(0) translateY(0);animation:hr-slide-in 900ms cubic-bezier(.2,.9,.2,1)}
        .hr-flybox.from-right{transform:translateX(18px) translateY(8px)}
        .hr-flybox.from-right.show{opacity:1;transform:translateX(0) translateY(0);animation:hr-slide-in-right 900ms cubic-bezier(.2,.9,.2,1)}
        .hr-flybox .thumb{width:56px;height:56px;border-radius:8px;object-fit:cover;flex-shrink:0;background:#f1f3f5;display:flex;align-items:center;justify-content:center;color:#999;font-size:20px}
        .hr-flybox .title{font-weight:800;color:#0d6efd;font-size:0.95rem;margin-left:6px}
        .hr-flybox.hide{opacity:0;transform:translateY(6px)}

        @keyframes hr-slide-in{0%{transform:translateX(-28px) translateY(8px);opacity:0}60%{transform:translateX(6px) translateY(-6px);opacity:1}100%{transform:translateX(0) translateY(0);opacity:1}}
        @keyframes hr-slide-in-right{0%{transform:translateX(28px) translateY(8px);opacity:0}60%{transform:translateX(-6px) translateY(-6px);opacity:1}100%{transform:translateX(0) translateY(0);opacity:1}}

        /* Heart rise animation */
        .hr-heart{position:fixed;width:40px;height:40px;border-radius:20px;background:linear-gradient(135deg,#ff6b6b,#ff3b6b);display:flex;align-items:center;justify-content:center;color:#fff;font-weight:700;font-size:18px;z-index:1000001;opacity:0;transform:translateY(0) scale(0.8)}
        .hr-heart.show{animation:hr-rise 1.2s forwards}
        @keyframes hr-rise{0%{transform:translateY(0) scale(0.8);opacity:1}60%{transform:translateY(-120px) scale(1.2);opacity:1}100%{transform:translateY(-160px) scale(1.4);opacity:0}}
        `;
        const s = document.createElement('style'); s.setAttribute('data-generated', 'donation-flybox'); s.textContent = css; document.head.appendChild(s);
    }

    function escapeHtml(str) { return String(str).replace(/[&<>"']/g, function (m) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": "&#39;" }[m]; }); }

    const MAX_VISIBLE_FLYBOXES = 3;
    const FLYBOX_BASE_BOTTOM = 76; // px
    const FLYBOX_SPACING = 12; // px gap between stacked flyboxes
    function positionFlyboxes() {
        try {
            // Keep DOM order: oldest first, newest appended last — newest will be above previous
            const els = Array.from(document.querySelectorAll('.hr-flybox'));
            const gap = FLYBOX_SPACING;
            els.forEach((el, idx) => {
                // compute bottom offset so boxes stack upward without overlap (newer items have larger idx => higher bottom)
                const base = FLYBOX_BASE_BOTTOM + idx * (el.offsetHeight + gap);
                el.style.bottom = base + 'px';
                // give newer boxes higher z-index
                const z = 1000000 + idx;
                el.style.zIndex = String(z);
            });
        } catch (e) { console.debug('[donation-flybox] position error', e); }
    }

    function showFlyBox(donation, type) {
        if (!donation) { console.debug('[donation-flybox] showFlyBox no donation'); return; }
        injectStyles();
        // If there are already too many visible, remove the oldest to make room
        try {
            const existing = Array.from(document.querySelectorAll('.hr-flybox'));
            if (existing.length >= MAX_VISIBLE_FLYBOXES) {
                try { existing[0].remove(); positionFlyboxes(); } catch (e) { }
            }
        } catch (e) { }

        const el = document.createElement('div'); el.className = 'hr-flybox';
        el.setAttribute('role', 'status'); el.setAttribute('aria-live', 'polite');

        // Alternate slide direction per notification (persist in session so it alternates across loads)
        try {
            const last = sessionStorage.getItem('donation_last_direction') || 'right';
            const dir = last === 'right' ? 'left' : 'right';
            sessionStorage.setItem('donation_last_direction', dir);
            if (dir === 'right') el.classList.add('from-right');
            console.debug('[donation-flybox] slide direction:', dir);
        } catch (e) { }

        // small status badge — show 'Pending' for claimed, 'New'/'Yesterday'/'Active' for active based on age
        function getAgeLabel(d) {
            try {
                const t = d.created_at || d.createdAt || d.claimed_at || d.claimedAt || null;
                if (!t) return 'Active';
                const dt = new Date(t);
                if (isNaN(dt.getTime())) return 'Active';
                const diff = Date.now() - dt.getTime();
                const day = 24 * 60 * 60 * 1000;
                if (diff < day) return 'New';
                if (diff < 2 * day) return 'Yesterday';
                return 'Active';
            } catch (e) { return 'Active'; }
        }
        const statusLabel = type === 'claimed' ? 'Pending' : getAgeLabel(donation);
        const statusTitle = (donation.created_at || donation.createdAt || donation.claimed_at || donation.claimedAt) ? new Date(donation.created_at || donation.createdAt || donation.claimed_at || donation.claimedAt).toLocaleString() : '';
        const statusBadge = `<span title="${statusTitle}" style="font-size:12px;padding:4px 8px;border-radius:12px;background:#fff;border:1px solid ${type === 'claimed' ? '#ffc107' : '#0d6efd'};color:${type === 'claimed' ? '#8a6d00' : '#0d6efd'};margin-right:8px">${statusLabel}</span>`;
        const base = window.BACKEND_URL || '';
        const photoURL = donation && donation.photo_filename ? (base + '/uploads/donations/' + encodeURIComponent(donation.photo_filename)) : '';
        const photoHTML = photoURL
            ? `<img class="thumb" src="${photoURL}" alt="Donation photo" onerror="this.style.display='none'" />`
            : `<div class="thumb">📦</div>`;

        el.innerHTML = `${photoHTML}<div style="display:flex;flex-direction:column"><div style="display:flex;align-items:center">${statusBadge}<div class="title">${escapeHtml(donation.title || 'New donation')}</div></div></div>`;

        // Ensure it is positioned and visible even if CSS fails
        el.style.position = 'fixed'; el.style.left = '18px'; el.style.bottom = '76px'; el.style.zIndex = '1000000';
        document.body.appendChild(el);
        // position immediately and shortly after so stacking doesn't overlap during entrance
        try { positionFlyboxes(); } catch (e) { }
        // trigger entrance animation
        setTimeout(() => { el.classList.add('show'); console.info('[donation-flybox] show class added, size=', el.offsetWidth, 'x', el.offsetHeight); positionFlyboxes(); }, 25);
        // position stacked flyboxes again after animation start
        setTimeout(positionFlyboxes, 300);
        console.info('[donation-flybox] flybox inserted for', donation.id || 'debug', 'type=' + (type || 'active'));

        // Allow user to click to dismiss immediately (clears scheduled heart)
        let heartTimer = null;
        el.addEventListener('click', () => { try { if (heartTimer) clearTimeout(heartTimer); el.remove(); positionFlyboxes(); } catch (e) { } });

        // Auto-hide after 30 seconds with heart rise animation
        const HEART_DELAY_MS = 30 * 1000; // 30 seconds
        heartTimer = setTimeout(() => {
            try {
                const heart = document.createElement('div');
                heart.className = 'hr-heart';
                heart.textContent = '❤';
                document.body.appendChild(heart);
                // position heart centered above the flybox
                const rect = el.getBoundingClientRect();
                heart.style.left = (rect.left + rect.width / 2 - 20) + 'px';
                heart.style.bottom = (window.innerHeight - rect.bottom + 10) + 'px';
                setTimeout(() => { heart.classList.add('show'); }, 40);
                // remove heart after animation completes
                setTimeout(() => { try { heart.remove(); } catch (e) { } }, 1400);
                // hide flybox shortly after heart appears
                setTimeout(() => { try { el.classList.add('hide'); setTimeout(() => { try { el.remove(); positionFlyboxes(); } catch (e) { } }, 300); } catch (e) { } }, 400);
            } catch (e) { console.debug('[donation-flybox] heart animation error', e); }
        }, HEART_DELAY_MS);

        // Return a small handle to allow clearing hide timer if needed
        return { element: el, heartTimer };

    }

    // Expose a simple test helper for manual triggering
    try { window.hr_forceDonationTest = function () { console.info('[donation-flybox] hr_forceDonationTest called'); showFlyBox({ id: 'manual-test', title: 'Manual test donation' }); }; } catch (e) { console.debug('[donation-flybox] could not set global test function', e); }


    // Poll for active donations and show flybox for unseen ones
    (function () {
        const BACKEND = window.BACKEND_URL || 'http://127.0.0.1:5000';
        const POLL_INTERVAL_MS = 15 * 1000;

        function getShownIds() { try { const raw = sessionStorage.getItem('donation_shown_ids'); return raw ? JSON.parse(raw) : []; } catch (e) { return []; } }
        function markShown(type, id) {
            try { const key = `${type}:${id}`; const arr = getShownIds(); if (!arr.includes(key)) { arr.push(key); sessionStorage.setItem('donation_shown_ids', JSON.stringify(arr)); } } catch (e) { }
        }

        async function fetchActive() {
            try {
                const res = await fetch(BACKEND + '/api/active-donations');
                if (!res.ok) return [];
                const data = await res.json();
                return Array.isArray(data) ? data : [];
            } catch (e) { console.debug('[donation-flybox] fetchActive error', e); return []; }
        }

        async function fetchClaimedForNgo(ngoId) {
            try {
                if (!ngoId) return [];
                const res = await fetch(`${BACKEND}/api/ngo/${ngoId}/claimed-donations`);
                if (!res.ok) return [];
                const data = await res.json();
                return Array.isArray(data) ? data : [];
            } catch (e) { console.debug('[donation-flybox] fetchClaimedForNgo error', e); return []; }
        }

        async function pollOnce() {
            try {
                // fetch active (unclaimed)
                const actives = await fetchActive();
                // fetch claimed (pending) if we have an NGO context
                const ngoId = window.currentNgoId || window.CURRENT_NGO_ID || null;
                const claimed = ngoId ? await fetchClaimedForNgo(ngoId) : [];

                // Normalize entries with a common timestamp field for sorting
                const normalized = [];
                actives.forEach(a => normalized.push({ type: 'active', id: a.id, time: a.created_at || a.createdAt || 0, raw: a }));
                claimed.forEach(c => normalized.push({ type: 'claimed', id: c.id, time: c.claimed_at || c.claimedAt || c.created_at || 0, raw: c }));

                if (normalized.length === 0) return;
                // sort newest first
                normalized.sort((x, y) => new Date(y.time) - new Date(x.time));

                // pick first unseen and not closed
                const shown = getShownIds();

                // If every item is either closed or already shown, schedule/reset shown list so notifications can restart later
                const allSeen = normalized.every(item => {
                    const closedKey = `donation_closed_${item.type}_${item.id}`;
                    const shownKey = `${item.type}:${item.id}`;
                    return sessionStorage.getItem(closedKey) || shown.includes(shownKey);
                });

                const RESET_COOLDOWN_MS = 2 * 60 * 1000; // 2 minutes
                const PENDING_RESET_KEY = 'donation_shown_pending_reset_ts';

                if (allSeen) {
                    const pending = sessionStorage.getItem(PENDING_RESET_KEY);
                    if (!pending) {
                        sessionStorage.setItem(PENDING_RESET_KEY, String(Date.now()));
                        console.info('[donation-flybox] all notifications seen — scheduling reset in 10min');
                    } else if (Date.now() - parseInt(pending, 10) > RESET_COOLDOWN_MS) {
                        // perform reset of only shown ids (keep closed markers)
                        try { sessionStorage.removeItem('donation_shown_ids'); sessionStorage.removeItem(PENDING_RESET_KEY); sessionStorage.setItem('donation_shown_last_reset', String(Date.now())); console.info('[donation-flybox] all notifications seen — shown list reset'); } catch (e) { }
                    }
                    // nothing to show right now
                    return;
                } else {
                    // if new/unseen item appears, clear any pending reset
                    try { sessionStorage.removeItem(PENDING_RESET_KEY); } catch (e) { }
                }

                for (const item of normalized) {
                    const closedKey = `donation_closed_${item.type}_${item.id}`;
                    const shownKey = `${item.type}:${item.id}`;
                    if (sessionStorage.getItem(closedKey)) continue;
                    if (shown.includes(shownKey)) continue;
                    // show and mark
                    showFlyBox(item.raw, item.type);
                    markShown(item.type, item.id);
                    break;
                }

            } catch (e) { console.debug('[donation-flybox] poll error', e); }
        }

        // start polling
        try { pollOnce(); setInterval(pollOnce, POLL_INTERVAL_MS); } catch (e) { console.debug('[donation-flybox] could not start poll', e); }
    })();
})();

