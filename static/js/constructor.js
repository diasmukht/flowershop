function updateItem(type, id, action) {
    fetch('/constructor/update_item/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({ type, id, action })
    })
    .then(res => res.json())
    .then(data => {
        if (data.success) {
            refreshSummary();  // 🔄 только часть страницы
        }
    });
}

function refreshSummary() {
    fetch('/constructor/summary/partial/')  // 📥 новый endpoint, см. ниже
        .then(res => res.text())
        .then(html => {
            document.getElementById('constructor-summary').innerHTML = html;
        });
}

function getCookie(name) {
    let cookieValue = null;
    const cookies = document.cookie.split(';');
    for (let cookie of cookies) {
        cookie = cookie.trim();
        if (cookie.startsWith(name + '=')) {
            cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
            break;
        }
    }
    return cookieValue;
}
