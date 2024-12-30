async function predictAtleticoWin(home, away, date) {
    const csrftoken = getCookie('csrftoken');  // CSRF 토큰 가져오기

    const response = await fetch('/predict', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken  // CSRF 토큰 추가
        },
        body: JSON.stringify({ homeTeam: home, awayTeam: away, matchDate: date })
    });

    const data = await response.json();
    alert(`아틀레티코 마드리드의 승리 확률: ${data.homeWinProbability}%`);
}

function openPredictionModal(home, away, date) {
    predictAtleticoWin(home, away, date);
}

// CSRF 토큰을 쿠키에서 가져오는 함수
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.startsWith(name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
