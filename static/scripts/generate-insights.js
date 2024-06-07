const insightsBtn = document.getElementById('generate-insights');

const generate = (e) => {
    e.preventDefault();
    const animation = document.querySelector('.loading-svg');
    animation.style.visibility = 'visible';

    const timestamp = new Date().toLocaleString(navigator.language, { hour: 'numeric', minute: 'numeric', hour12: true });
    
    const params = new URLSearchParams();
    params.set('id', localStorage.getItem('session'));

    const endpoint = 'http://127.0.0.1:5000//api/v1/insights';
    const url = new URL(endpoint);
    url.search = params;

    const request = new Request(url, {
        method: 'GET',
        mode: "cors",
        headers: { 'Accept': 'text/plain' }
    });

    fetch(request)
    .then(msg => msg.json())
    .then(msg => {
        const message = {
            sender: 'Mindbot',
            text: msg.generated_insight,
            timestamp
        }

        console.log(message.text);
        const formattedText = message.text.replace(/\*\*(.+?)\*\*/g, "<h3>$1</h3>")
        .replace(/What you did well:/g, "<br><strong>What you did well:</strong>")
        .replace(/What you could improve:/g, "<br><strong>What you could improve:</strong>")
        .replace(/Observable patterns:/g, "<br><strong>Observable patterns:</strong>")
        .replace(/Observations:/g, "<br><strong>Observations:</strong>")
        .replace(/Suggestions:/g, "<br><strong>Suggestions:</strong>");


        chatMessages.innerHTML += `
        <div class="message ${message.sender === 'Mindbot' ? 'mindbot' : 'user'}">
        <div class="message-sender">${message.sender}</div>
        <div class="message-text">${formattedText}</div>
        <div class="message-time">${message.timestamp}</div>
        </div>
        `;
        chatMessages.scrollTop = chatMessages.scrollHeight;
        animation.style.visibility = 'hidden';
    });

}

insightsBtn.addEventListener('click', generate);