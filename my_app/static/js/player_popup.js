// 팝업 띄우기
async function showPlayerPopup(playerId) {
    const popup = document.getElementById("playerPopup");
    const playerDetails = document.getElementById("playerDetails");

    try {
        // 서버에서 특정 선수의 데이터를 가져옵니다.
        const response = await fetch(`/player/${playerId}/`);
        const data = await response.json();

        // 에러 처리
        if (data.error) {
            playerDetails.innerHTML = `<p>Error: ${data.error}</p>`;
        } else {
            // 선수 데이터 표시
            playerDetails.innerHTML = `
                <img src="${data.image_url}" alt="${data.name}" style="width: 100px; height: 100px;">
                <h2>${data.name}</h2>
                <p><strong>Position:</strong> ${data.position}</p>
                <p><strong>Nationality:</strong> ${data.nationality}</p>
                <p><strong>Birth Date:</strong> ${data.birth_date}</p>
                <p><strong>Goals:</strong> ${data.goals}</p>
                <p><strong>Assists:</strong> ${data.assists}</p>
            `;
        }

        // 팝업 표시
        popup.style.display = "flex";
    } catch (error) {
        playerDetails.innerHTML = `<p>Error loading player data.</p>`;
        console.error("Error fetching player data:", error);
    }
}

// 팝업 닫기
function closePopup() {
    const popup = document.getElementById("playerPopup");
    popup.style.display = "none";
}
