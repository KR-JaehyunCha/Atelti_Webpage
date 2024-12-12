document.getElementById('send-btn').addEventListener('click', () => {
    const inputField = document.getElementById('chat-input');
    const userMessage = inputField.value;

    if (userMessage.trim() === "") {
        displayMessage('Bot', 'Please enter a message.'); // 빈 메시지 처리
        return;
    }

    displayMessage('You', userMessage); // 사용자가 입력한 메시지 표시
    inputField.value = ""; // 입력 필드 초기화

    // CSRF 토큰 가져오기
    const csrfToken = document.getElementById('csrf-token').value;

    // OpenAI API와 통신
    fetch('/chatbot/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken  // CSRF 토큰 추가
        },
        body: JSON.stringify({ message: userMessage })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        const botResponse = data.response || 'Sorry, I could not understand that.';
        displayMessage('Bot', botResponse); // 봇 응답 표시
    })
    .catch(err => {
        displayMessage('Bot', `Error: ${err.message}`); // 에러 메시지 표시
    });
});

function displayMessage(sender, message) {
    const chatHistory = document.getElementById('chat-history');
    const messageElem = document.createElement('div');
    messageElem.textContent = `${sender}: ${message}`;
    chatHistory.appendChild(messageElem);
    chatHistory.scrollTop = chatHistory.scrollHeight; // 채팅창 자동 스크롤
}