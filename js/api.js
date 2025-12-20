// Shared client-side API handlers for Login / Register / Donate
(function(){
    async function postJSON(url, data){
        const res = await fetch(url, {
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

    async function postForm(url, formData){
        const res = await fetch(url, {
            method: 'POST',
            credentials: 'include',
            body: formData
        });
        return res.json();
    }

    // Login form
    const loginForm = document.getElementById('loginForm');
    if (loginForm){
        loginForm.addEventListener('submit', async function(e){
            e.preventDefault();
            const submitBtn = document.getElementById('submitBtn');
            const email = document.getElementById('email').value.trim();
            const password = document.getElementById('password').value || '';
            const emailError = document.getElementById('emailError');
            const pwError = document.getElementById('pwError');
            if (!email || !password){
                if (emailError){ emailError.textContent = 'Please enter email.'; emailError.style.display='block' }
                if (pwError){ pwError.textContent = 'Please enter password.'; pwError.style.display='block' }
                return;
            }
            submitBtn.disabled = true; submitBtn.textContent = 'Signing in...';
            try{
                const fd = new FormData(); fd.append('email', email); fd.append('password', password);
                const res = await fetch('/api/login', { method:'POST', credentials:'include', body: fd });
                const data = await res.json();
                if (res.ok && data.ok){
                    window.location.href = 'dashboard.html';
                } else {
                    const msg = data.error || 'Login failed';
                    if (pwError){ pwError.textContent = msg; pwError.style.display='block' }
                    submitBtn.disabled = false; submitBtn.textContent = 'Login to Dashboard';
                }
            }catch(err){
                if (pwError){ pwError.textContent = 'Network error'; pwError.style.display='block' }
                submitBtn.disabled = false; submitBtn.textContent = 'Login to Dashboard';
            }
        });
    }

    // Register form (modal or page)
    const registerForm = document.getElementById('registerForm');
    if (registerForm){
        registerForm.addEventListener('submit', async function(e){
            e.preventDefault();
            const orgName = document.getElementById('orgName').value.trim();
            const email = document.getElementById('regEmail').value.trim();
            const password = document.getElementById('regPassword').value || '';
            const confirm = document.getElementById('regPasswordConfirm').value || '';
            const phone = document.getElementById('regPhone').value || '';
            const submitBtn = document.getElementById('registerSubmitBtn');
            if (!orgName || !email || password.length < 8 || password !== confirm){
                // let existing validators show errors
                return;
            }
            submitBtn.disabled = true; submitBtn.textContent = 'Creating...';
            try{
                const fd = new FormData(); fd.append('name', orgName); fd.append('email', email); fd.append('password', password);
                const res = await fetch('/api/register', { method:'POST', credentials:'include', body: fd });
                const data = await res.json();
                if (res.ok && data.ok){
                    // close modal if present
                    try{ const modalEl = document.getElementById('registerModal'); if (modalEl){ const bs = bootstrap.Modal.getInstance(modalEl); if (bs) bs.hide(); } }catch(e){}
                    registerForm.reset();
                    submitBtn.disabled = false; submitBtn.textContent = 'Create Account';
                    alert('Account created — signed in.');
                    window.location.href = 'dashboard.html';
                } else {
                    const msg = data.error || 'Registration failed';
                    alert(msg);
                    submitBtn.disabled = false; submitBtn.textContent = 'Create Account';
                }
            }catch(err){ alert('Network error'); submitBtn.disabled = false; submitBtn.textContent = 'Create Account'; }
        });
    }

    // Donate form
    const donateForm = document.getElementById('donateForm');
    if (donateForm){
        donateForm.addEventListener('submit', async function(e){
            e.preventDefault();
            const btn = donateForm.querySelector('.btn-submit-donation');
            const donType = document.getElementById('donType').value || '';
            const itemType = donateForm.querySelector('input[name="item_type"]').value || '';
            const quantity = donateForm.querySelector('input[name="quantity"]').value || 0;
            const address = donateForm.querySelector('input[name="address"]').value || '';
            const date = donateForm.querySelector('input[name="date"]').value || '';
            const time = donateForm.querySelector('input[name="time"]').value || '';
            const photos = document.getElementById('photos');

            if (!donType || !itemType || !quantity || !address){
                const el = document.getElementById('donMsg'); el.className='alert alert-danger'; el.style.display='block'; el.textContent='Please complete required fields.'; return;
            }
            btn.disabled = true; btn.textContent = 'Submitting...';
            try{
                const fd = new FormData();
                fd.append('title', itemType);
                fd.append('description', 'Type: '+donType+'; Pickup date: '+date+' '+time);
                fd.append('quantity', quantity);
                fd.append('pickup_info', address+' | '+date+' '+time);
                if (photos && photos.files && photos.files.length){
                    for (let i=0;i<photos.files.length;i++){ fd.append('photos', photos.files[i]); }
                }
                const res = await fetch('/api/donations', { method:'POST', credentials:'include', body: fd });
                const data = await res.json();
                const el = document.getElementById('donMsg');
                if (res.ok && data.ok){
                    el.className='alert alert-success'; el.style.display='block'; el.textContent='Donation submitted — thank you!';
                    donateForm.reset();
                } else if (res.status === 401){
                    el.className='alert alert-warning'; el.style.display='block'; el.textContent='You must be logged in to submit donations.';
                } else {
                    el.className='alert alert-danger'; el.style.display='block'; el.textContent=(data.error||'Submission failed');
                }
            }catch(err){ const el = document.getElementById('donMsg'); el.className='alert alert-danger'; el.style.display='block'; el.textContent='Network error'; }
            btn.disabled = false; btn.textContent = 'Submit Donation';
        });
    }

    // Optional: logout link handler
    const logoutLinks = document.querySelectorAll('[data-logout]');
    logoutLinks.forEach(a => a.addEventListener('click', async function(e){ e.preventDefault(); await fetch('/api/logout',{method:'POST',credentials:'include'}); window.location.href = 'index.html'; }));

})();
