const battery = document.getElementById("battery");
const distance = document.getElementById("distance");

const forward = document.getElementById("forward");
const backward = document.getElementById("backward");
const left = document.getElementById("left");
const right = document.getElementById("right");

const car = document.getElementById("car");

let x = 120;
let y = 120;
let angle = 0;

function drawCar(){
    car.style.left = x + "px";
    car.style.top = y + "px";
    car.style.transform = `rotate(${angle}deg)`;
}

function updateStatus(data){
    battery.textContent = data.battery;
    distance.textContent = data.distance;
}

async function sendCommand(url){

    const response = await fetch(url,{
        method:"POST"
    });

    const data = await response.json();

    updateStatus(data);

    switch(url){

        case "/api/forward":
            y -= 20;
            break;

        case "/api/backward":
            y += 20;
            break;

        case "/api/left":
            angle -= 15;
            break;

        case "/api/right":
            angle += 15;
            break;
    }

    drawCar();
}

async function loadStatus(){

    const response = await fetch("/api/status");

    const data = await response.json();

    updateStatus(data);
}

forward.onclick=()=>sendCommand("/api/forward");

backward.onclick=()=>sendCommand("/api/backward");

left.onclick=()=>sendCommand("/api/left");

right.onclick=()=>sendCommand("/api/right");

drawCar();

loadStatus();