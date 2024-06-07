const chatMessages = document.querySelector('.chat-messages');
const chatInputForm = document.querySelector('.chat-input-form');
const chatInput = document.querySelector('.chat-input');
const chatContainer = document.querySelector('.chat-container');
const holder = [];

// Generate a templated journal entry HTML code to be added to the DOM
function newInputHtml (msg) { 
    msgDate = new Date(msg.created_at);
    const timestamp = msgDate.toLocaleString(navigator.language, { hour: 'numeric', minute: 'numeric', hour12: true });
    return `
    <div class="message ${msg.entry === undefined ? 'mindbot' : 'user'}" id='${msg.id}'>
    <div class="message-sender">${msg.entry !== undefined ? '' : 'MindBot'}</div>
    <div class="message-text">${msg.entry !== undefined ? msg.entry : msg.insight}</div>
    <div class="message-time">${timestamp}</div>
    </div>`;
}

// Create request object to fetch saved entries from database
const params = new URLSearchParams();
params.set('id', localStorage.getItem('session'));

const oldJournalsUrl = new URL('http://127.0.0.1:5000//api/v1/journal');
oldJournalsUrl.search = params;

const oldJournalsReq = new Request(oldJournalsUrl, {
    method: 'GET',
    mode: "cors",
    credentials: "include",
});

const today = new Date();
const lastEntry = ['dummy']; // keeps track of the user's last entry

// Fetch saved entries from database and append them to the DOM
fetch(oldJournalsReq)
.then(resp => resp.json())
.then(json => {
    Object.entries(json).forEach(([key, val]) => {
        const entryDay = new Date(key + ' ' + String(today.getFullYear()));
        const currentDayLabel = key;
        
        const newDiv = document.createElement('div');
        newDiv.setAttribute('class', 'message-date');
        newDiv.appendChild(document.createTextNode(`${currentDayLabel}`));
        chatMessages.appendChild(newDiv);
        
        val.forEach(elem => chatMessages.innerHTML += newInputHtml(elem));  
        lastEntry.push(val[val.length - 1]);
        lastEntry.shift();
    });
})
