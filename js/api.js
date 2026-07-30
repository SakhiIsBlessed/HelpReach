// Shared client-side API handlers for Login / Register / Donate
(function () {
    // Base backend URL — set by pages that need it (e.g. window.BACKEND_URL).
    const API_BASE = (window.BACKEND_URL || '');
    async function postJSON(url, data) {
        const fullUrl = url && (url.indexOf('://') !== -1) ? url : (API_BASE + url);
        const res = await fetch(fullUrl, {
            method: 'POST',
            credentials: 'include',
            headers: {
                'Accept': 'application/json',
                'X-Requested-With': 'XMLHttpRequest'
            },
            body: JSON.stringify(data)
        });
        return res.json();
    }

    async function postForm(url, formData) {
        const fullUrl = url && (url.indexOf('://') !== -1) ? url : (API_BASE + url);
        const res = await fetch(fullUrl, {
            method: 'POST',
            credentials: 'include',
            body: formData
        });
        return res.json();
    }

    // Login form
    const loginForm = document.getElementById('loginForm');
    if (loginForm) {
        loginForm.addEventListener('submit', async function (e) {
            e.preventDefault();
            const submitBtn = document.getElementById('submitBtn');
            const email = document.getElementById('email').value.trim();
            const password = document.getElementById('password').value || '';
            const emailError = document.getElementById('emailError');
            const pwError = document.getElementById('pwError');
            if (!email || !password) {
                if (emailError) { emailError.textContent = 'Please enter email.'; emailError.style.display = 'block' }
                if (pwError) { pwError.textContent = 'Please enter password.'; pwError.style.display = 'block' }
                return;
            }
            submitBtn.disabled = true; submitBtn.textContent = 'Signing in...';
            try {
                const fd = new FormData(); fd.append('email', email); fd.append('password', password);
                const res = await fetch(API_BASE + '/api/login', { method: 'POST', credentials: 'include', body: fd });
                const data = await res.json();
                if (res.ok && data.ok) {
                    window.location.href = 'dashboard.html';
                } else {
                    const msg = data.error || 'Login failed';
                    if (pwError) { pwError.textContent = msg; pwError.style.display = 'block' }
                    submitBtn.disabled = false; submitBtn.textContent = 'Login to Dashboard';
                }
            } catch (err) {
                if (pwError) { pwError.textContent = 'Network error'; pwError.style.display = 'block' }
                submitBtn.disabled = false; submitBtn.textContent = 'Login to Dashboard';
            }
        });
    }

    // Register form (modal or page)
    const registerForm = document.getElementById('registerForm');
    if (registerForm) {
        registerForm.addEventListener('submit', async function (e) {
            e.preventDefault();
            const orgName = document.getElementById('orgName').value.trim();
            const email = document.getElementById('regEmail').value.trim();
            const password = document.getElementById('regPassword').value || '';
            const confirm = document.getElementById('regPasswordConfirm').value || '';
            const phone = document.getElementById('regPhone').value || '';
            const submitBtn = document.getElementById('registerSubmitBtn');
            if (!orgName || !email || password.length < 8 || password !== confirm) {
                // let existing validators show errors
                return;
            }
            submitBtn.disabled = true; submitBtn.textContent = 'Creating...';
            try {
                const fd = new FormData(); fd.append('name', orgName); fd.append('email', email); fd.append('password', password);
                const res = await fetch(API_BASE + '/api/register', { method: 'POST', credentials: 'include', body: fd });
                const data = await res.json();
                if (res.ok && data.ok) {
                    // close modal if present
                    try { const modalEl = document.getElementById('registerModal'); if (modalEl) { const bs = bootstrap.Modal.getInstance(modalEl); if (bs) bs.hide(); } } catch (e) { }
                    registerForm.reset();
                    submitBtn.disabled = false; submitBtn.textContent = 'Create Account';
                    alert('Account created — signed in.');
                    window.location.href = 'dashboard.html';
                } else {
                    const msg = data.error || 'Registration failed';
                    alert(msg);
                    submitBtn.disabled = false; submitBtn.textContent = 'Create Account';
                }
            } catch (err) { alert('Network error'); submitBtn.disabled = false; submitBtn.textContent = 'Create Account'; }
        });
    }

    // Donate form handler intentionally disabled here — using the more detailed handler inside `donate.html` which handles file uploads and user session checks.
    // (Kept here for reference.)
    // If you want to re-enable this handler, remove this comment and ensure only one POST is made to avoid duplicate requests.


    // Optional: logout link handler
    const logoutLinks = document.querySelectorAll('[data-logout]');
    logoutLinks.forEach(a => a.addEventListener('click', async function (e) { e.preventDefault(); await fetch(API_BASE + '/api/logout', { method: 'POST', credentials: 'include' }); window.location.href = 'index.html'; }));

})();
