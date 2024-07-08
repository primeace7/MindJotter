const insightsBtn = document.getElementById('generate-insights');

const generate = (e) => {
    e.preventDefault();
    const animation = document.querySelector('.loading-svg');
    const body = document.querySelector('body');

    animation.style.visibility = 'visible';
    
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
        const timestamp = new Date().toLocaleString(navigator.language, { hour: 'numeric', minute: 'numeric', hour12: true });
        const message = {
            sender: 'Mindbot',
            text: msg.generated_insight,
            timestamp
        }

        // console.log(message.text);
        const formattedText = message.text.replace(/\*\*(.+?)\*\*/g, "<h2>$1</h2>")
        .replace(/What you did well:/g, "<b>What you did well:</b>")
        .replace(/What you could improve:/g, "<b>What you could improve:</b>")
        .replace(/What you could do better:/g, "<b>What you could do better:</b>")
        .replace(/Observable patterns:/g, "<b>Observable patterns:</b>")
        .replace(/Observations:/g, "<b>Observations:</b>")
        .replace(/Suggestions:/g, "<b>Suggestions:</b>")
        .replace(/\*/g, "");

        chatMessages.innerHTML += `
        <div class="message ${message.sender === 'Mindbot' ? 'mindbot' : 'user'}">
        <div class="message-sender">${message.sender}</div>
        <div class="message-text">${formattedText}</div>
        <div class="message-time">${message.timestamp}</div>
        </div>
        `;
        chatMessages.scrollTop = chatMessages.scrollHeight;
        animation.style.visibility = 'hidden';
        return formattedText
    })
    .then(insight => {
        const update = new Request(url, {
            method: 'POST',
            mode: "cors",
            body: JSON.stringify({insight: insight}),
            headers: new Headers({'content-type': 'application/json'}),
        });
        
        fetch(update)
        .then(resp => {
            if (resp.status !== 200)
                alert('An error occured while saving the insight on the database');
        })
    })
    .catch(e => {
        animation.style.visibility = 'hidden';
        alert('There was an error. Please try again.');
    })

}

insightsBtn.addEventListener('click', generate);