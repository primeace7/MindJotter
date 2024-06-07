// Funcition to render new user entry and store in database

const sendMessage = (e) => {
    e.preventDefault();

    const timestamp = new Date().toLocaleString(navigator.language, { hour: 'numeric', minute: 'numeric', hour12: true });

    const message = {
        sender: '',
        text: chatInput.value,
        timestamp
    }

    const newEntry = {"entry": message.text};
    
    const params = new URLSearchParams();
    params.set('id', localStorage.getItem('session'));

    const endpoint = 'http://127.0.0.1:5000//api/v1/entries';
    const url = new URL(endpoint);
    url.search = params;
    console.log('final url: ', url.toString());

    const request = new Request(url, {
        method: 'POST',
        body: JSON.stringify(newEntry),
        headers: new Headers({'content-type': 'application/json'}),
        // credentials: "include",
        mode: "cors"
    });

    fetch(request)
    .then(msg => msg.json())
    .then(msg => console.log(msg));

    chatMessages.innerHTML += `
    <div class="message ${message.sender === 'mindbot' ? 'mindbot' : 'user'}">
    <div class="message-sender">${message.sender}</div>
    <div class="message-text">${message.text}</div>
    <div class="message-time">${message.timestamp}</div>
    </div>
    `;
    chatInputForm.reset();
    chatMessages.scrollTop = chatMessages.scrollHeight;
    chatInput.focus();
}

chatInputForm.addEventListener('submit', sendMessage);
