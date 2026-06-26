 const battery = document.getElementById("battery");
const distance = document.getElementById("distance");

const forward = document.getElementById("forward");
const backward = document.getElementById("backward");
const left = document.getElementById("left");
const right = document.getElementById("right");

// 화면 갱신
function updateStatus(data) {
    battery.textContent = data.battery;
    distance.textContent = data.distance;
}

// 서버 요청
async function sendCommand(url) {
    const response = await fetch(url, {
        method: "POST",
        cache: "no-store"
    });

    const data = await response.json();
    updateStatus(data);
}

// 현재 상태 불러오기
async function loadStatus() {
    const response = await fetch("/api/status");
    const data = await response.json();
    updateStatus(data);
}

// 버튼 이벤트
forward.addEventListener("click", () => {
    sendCommand("/api/forward");
});

backward.addEventListener("click", () => {
    sendCommand("/api/backward");
});

left.addEventListener("click", () => {
    sendCommand("/api/left");
});

right.addEventListener("click", () => {
    sendCommand("/api/right");
});

// 프로그램 시작 시 상태 표시
loadStatus();
