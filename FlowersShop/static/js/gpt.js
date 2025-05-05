function toggleGPT() {
    const box = document.getElementById('gptBox');
    box.style.display = box.style.display === 'none' || box.style.display === '' ? 'flex' : 'none';
}

function getCSRFToken() {
    const cookies = document.cookie.split(';');
    for (let cookie of cookies) {
        if (cookie.trim().startsWith('csrftoken=')) {
            return cookie.trim().split('=')[1];
        }
    }
    return '';
}

function sendGPT() {
    const input = document.getElementById('gptInput');
    const messages = document.getElementById('gptMessages');
    const text = input.value.trim();
    if (!text) return;

    const userMsg = document.createElement('div');
    userMsg.className = 'gpt-message user';
    userMsg.textContent = text;
    messages.appendChild(userMsg);

    input.value = '';

    const botMsg = document.createElement('div');
    botMsg.className = 'gpt-message bot';
    botMsg.textContent = '🤖 Печатает...';
    messages.appendChild(botMsg);
    messages.scrollTop = messages.scrollHeight;

    fetch('/gpt-response/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken(),
        },
        body: JSON.stringify({ message: text })
    })
    .then(response => response.json())
    .then(data => {
        botMsg.textContent = data.response || '❌ Ошибка в ответе GPT';
        messages.scrollTop = messages.scrollHeight;
    })
    .catch(() => {
        botMsg.textContent = '❌ Ошибка при запросе';
    });
}
