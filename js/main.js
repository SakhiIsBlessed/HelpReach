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
        .hr-flybox{position:fixed;left:18px;bottom:76px;background:#fff;border-radius:20px;box-shadow:0 6px 18px rgba(0,0,0,0.12);padding:8px 14px;display:inline-flex;align-items:center;gap:10px;z-index:999999;transition:transform 0.28s ease,opacity 0.28s ease;opacity:0;transform:translateY(6px);min-width:120px;max-width:320px}
        .hr-flybox.show{opacity:1;transform:translateY(0)}
        .hr-flybox .title{font-weight:800;color:#0d6efd;font-size:0.95rem}
        .hr-flybox.hide{opacity:0;transform:translateY(6px)}
        `;
        const s = document.createElement('style'); s.setAttribute('data-generated','donation-flybox'); s.textContent = css; document.head.appendChild(s);
    }

    function escapeHtml(str){ return String(str).replace(/[&<>"']/g, function(m){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":"&#39;"}[m];}); }

    function showFlyBox(donation){
        if (!donation) { console.debug('[donation-flybox] showFlyBox no donation'); return; }
        injectStyles();
        const el = document.createElement('div'); el.className = 'hr-flybox';
        el.setAttribute('role','status'); el.setAttribute('aria-live','polite');
        el.innerHTML = `<div class="title">${escapeHtml(donation.title || 'New donation')}</div>`;
        // Ensure it is positioned and visible even if CSS fails
        el.style.position = 'fixed'; el.style.left = '18px'; el.style.bottom = '76px'; el.style.zIndex = '1000000';
        document.body.appendChild(el);
        // trigger entrance animation
        setTimeout(()=>{ el.classList.add('show'); console.info('[donation-flybox] show class added, size=', el.offsetWidth, 'x', el.offsetHeight); }, 25);
        console.info('[donation-flybox] flybox inserted for', donation.id || 'debug');

        // Allow user to click to dismiss immediately
        el.addEventListener('click', () => { try { el.remove(); } catch(e){} });

        // Auto-hide after 3 minutes (per original requirement)
        const AUTO_HIDE_MS = 3 * 60 * 1000; // 3 minutes
        const hideTimer = setTimeout(()=>{
            try{ el.classList.add('hide'); setTimeout(()=>{ try{ el.remove(); }catch(e){} }, 300); }catch(e){}
        }, AUTO_HIDE_MS);

        // Return a small handle to allow clearing hide timer if needed
        return { element: el, hideTimer };

    }

    // Expose a simple test helper for manual triggering
    try { window.hr_forceDonationTest = function(){ console.info('[donation-flybox] hr_forceDonationTest called'); showFlyBox({ id: 'manual-test', title: 'Manual test donation' }); }; } catch (e) { console.debug('[donation-flybox] could not set global test function', e); }


    // Poll for active donations and show flybox for unseen ones
    (function(){
        const BACKEND = window.BACKEND_URL || 'http://127.0.0.1:5000';
        const POLL_INTERVAL_MS = 15 * 1000;

        function getShownIds(){ try{ const raw = sessionStorage.getItem('donation_shown_ids'); return raw? JSON.parse(raw): []; } catch(e){ return []; } }
        function markShown(id){ try{ const arr = getShownIds(); if (!arr.includes(id)) { arr.push(id); sessionStorage.setItem('donation_shown_ids', JSON.stringify(arr)); } } catch(e){}
        }

        async function fetchLatestDonation(){
            try{
                const res = await fetch(BACKEND + '/api/active-donations');
                if (!res.ok) return null;
                const data = await res.json();
                if (!Array.isArray(data) || data.length === 0) return null;
                return data[0];
            }catch(e){ console.debug('[donation-flybox] fetchLatestDonation error', e); return null; }
        }

        async function pollOnce(){
            try{
                const d = await fetchLatestDonation();
                if (!d) return;
                const id = d.id || 'latest';
                const closedKey = `donation_closed_${id}`;
                if (sessionStorage.getItem(closedKey)) return;
                const shown = getShownIds();
                if (shown.includes(id)) return;
                // show flybox and mark
                showFlyBox(d);
                markShown(id);
            }catch(e){ console.debug('[donation-flybox] poll error', e); }
        }

        // start polling
        try{ pollOnce(); setInterval(pollOnce, POLL_INTERVAL_MS); } catch(e){ console.debug('[donation-flybox] could not start poll', e); }
    })();
})();

