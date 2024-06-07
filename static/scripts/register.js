const form = document.getElementById('registration-form');

form.addEventListener('submit', (e) => {
    e.preventDefault();

    const formData = new FormData(form);

    const endpoint = 'http://127.0.0.1:5000//api/v1/user';
    const url = new URL(endpoint);
    const request = new Request(url, {
        method: 'POST',
        body: formData
    });

    if (formData.get('password') !== formData.get('confirm-password')) {
        const passwordErr = document.querySelector('.alert-pwd');
        passwordErr.style.visibility = 'visible';
        setTimeout(() => passwordErr.style.visibility = 'hidden', 5000);
    } else {
        fetch(request)
    .then(resp => {
        if (!resp.ok) {
            msg = resp.status === 409 ? '409': 'There was an error';
            throw Error(msg);
        }
        return resp.json();
    })
    .then(resp => {
            const successful = document.querySelector('.alert-success');
            successful.style.visibility = 'visible';
            setTimeout(() => document.location = 'http://127.0.0.1/login.html', 6000)
        })
    .catch(err => {
        const alertErr = document.querySelector('.alert');
        if (err.message === '409') {
            alertErr.style.visibility = 'visible';
            setTimeout(() => alertErr.style.visibility = 'hidden', 6000);
        }
        else
            console.error(err.message)
        })
    }
})
// fetch(request)
//     .then(resp => {
//         if (!resp.ok) {
//             msg = resp.status === 409 ? '409': 'There was an error';
//             throw Error(msg);
//         }
//         return resp.json();
//     })
//     .then(resp => {
//             document.location = 'http://127.0.0.1/login.html'
//             console.log(resp.message);
//     })
//     .catch(err => {
//         const alertErr = document.querySelector('.alert');
//         if (err.message === '409') {
//             alertErr.style.visibility = 'visible';
//             setTimeout(() => alertErr.style.visibility = 'hidden', 6000);
//         }
//         else
//             console.error(err.message)
//     })