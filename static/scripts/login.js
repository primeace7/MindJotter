const form = document.getElementById('login-form');

form.addEventListener('submit', (e) => {
    e.preventDefault();

    const formData = new FormData(form);

    const endpoint = 'http://127.0.0.1:5000//api/v1/user/login';
    const url = new URL(endpoint);
    const request = new Request(url, {
        method: 'POST',
        mode: "cors",
        body: formData,
        redirect: "follow",
    });

    fetch(request)
    .then(resp => {
        if (!resp.ok) {
            msg = resp.status === 401 ? '401': 'There was an error';
            throw Error(msg);
        }
        return resp.json();
    })
    .then(resp => {
        localStorage.setItem('session', resp.session);
        window.location.replace('/journal-area.html');
    })
    .catch(err => {
        const alertErr = document.querySelector('.alert');
        if (err.message === '401') {
            alertErr.style.visibility = 'visible';
            setTimeout(() => alertErr.style.visibility = 'hidden', 5000);
        }
        else
            console.error(err.message)
    })
})
