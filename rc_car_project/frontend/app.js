const battery = document.getElementById("battery");
const distance = document.getElementById("distance");

const forward = document.getElementById("forward");
const backward = document.getElementById("backward");
const left = document.getElementById("left");
const right = document.getElementById("right");

const car = document.getElementById("car");

let x = 300;
let y = 300;
let angle = 0;
const step = 8;

let keys = {};

// 자동차 그리기
function drawCar() {
    car.style.left = x + "px";
    car.style.top = y + "px";
    car.style.transform = `rotate(${angle}deg)`;
}

// 상태 표시
function updateStatus(data) {
    battery.textContent = data.battery;
    distance.textContent = data.distance;
}

// 서버 명령
async function sendCommand(url) {

    const response = await fetch(url, {
        method: "POST"
    });

    const data = await response.json();

    updateStatus(data);
}

// 현재 상태
async function loadStatus() {

    const response = await fetch("/api/status");

    const data = await response.json();

    updateStatus(data);
}

// 이동
function moveCar() {

    if (keys["ArrowLeft"]) {
        angle -= 4;
        sendCommand("/api/left");
    }

    if (keys["ArrowRight"]) {
        angle += 4;
        sendCommand("/api/right");
    }

    const rad = angle * Math.PI / 180;

    if (keys["ArrowUp"]) {

        x += Math.sin(rad) * step;
        y -= Math.cos(rad) * step;

        sendCommand("/api/forward");
    }

    if (keys["ArrowDown"]) {

        x -= Math.sin(rad) * step;
        y += Math.cos(rad) * step;

        sendCommand("/api/backward");
    }

    drawCar();

    requestAnimationFrame(moveCar);
}

// 키보드
document.addEventListener("keydown", (e) => {
    keys[e.key] = true;
});

document.addEventListener("keyup", (e) => {
    keys[e.key] = false;
});

// 버튼
forward.onclick = () => keys["ArrowUp"] = true;
backward.onclick = () => keys["ArrowDown"] = true;
left.onclick = () => keys["ArrowLeft"] = true;
right.onclick = () => keys["ArrowRight"] = true;

forward.onmouseup = () => keys["ArrowUp"] = false;
backward.onmouseup = () => keys["ArrowDown"] = false;
left.onmouseup = () => keys["ArrowLeft"] = false;
right.onmouseup = () => keys["ArrowRight"] = false;

forward.onmouseleave = () => keys["ArrowUp"] = false;
backward.onmouseleave = () => keys["ArrowDown"] = false;
left.onmouseleave = () => keys["ArrowLeft"] = false;
right.onmouseleave = () => keys["ArrowRight"] = false;

drawCar();
loadStatus();
moveCar();
