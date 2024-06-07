// Delete user cookie at the backend and log user out
const logoutEndpoint = 'http://127.0.0.1:5000//api/v1/logout';
const logoutUrl = new URL(logoutEndpoint);
const logoutRequest = new Request(logoutUrl, {
    method: 'DELETE',
    // credentials: "include",
    mode: "cors"
});

function logout () {
    fetch(logoutRequest)
    .then(resp => {
        if (!resp.ok)
            throw Error('There was an error');
        return resp;
    })
    .then(resp => window.location.replace('http://127.0.0.1/login.html'))
    .catch(err => console.log(err.message));
}

const logoutBtn = document.getElementById('logout');
logoutBtn.addEventListener('click', logout);