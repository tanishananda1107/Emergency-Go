let selectedType = "Ambulance Service";

let map = L.map('map').setView([12.9716, 77.5946], 13);

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png')
.addTo(map);

let marker = L.marker([12.9716, 77.5946]).addTo(map);

function selectType(card, type){
    document.querySelectorAll(".service")
        .forEach(s => s.classList.remove("active"));

    card.classList.add("active");
    selectedType = type;
}

async function requestHelp(){

    const location = document.getElementById("location").value;

    const res = await fetch("http://127.0.0.1:8000/request-help", {
        method:"POST",
        headers:{"Content-Type":"application/json"},
        body:JSON.stringify({
            emergency_type:selectedType,
            location:location
        })
    });

    const data = await res.json();

    document.getElementById("status").innerText =
        `${data.type} dispatched • ETA ${data.eta}`;

    startTracking(data.id);
}

function startTracking(id){

    const ws = new WebSocket(`ws://127.0.0.1:8000/track/${id}`);

    ws.onmessage = (event)=>{
        const pos = JSON.parse(event.data);

        marker.setLatLng([pos.lat,pos.lon]);
        map.panTo([pos.lat,pos.lon]);
    };
}

