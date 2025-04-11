let heartIcon, gestanteIcon, map;
let postosDisponiveis = [];

window.initMap = function () {
    const defaultCenter = { lat: -23.5505, lng: -46.6333 };

    heartIcon = {
        url: "https://cdn-icons-png.flaticon.com/512/833/833472.png",
        scaledSize: new google.maps.Size(32, 32),
    };

    gestanteIcon = {
        url: "https://cdn-icons-png.flaticon.com/512/2922/2922561.png",
        scaledSize: new google.maps.Size(36, 36),
    };

    map = new google.maps.Map(document.getElementById("map"), {
        center: defaultCenter,
        zoom: 13,
    });

    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(
            pos => {
                const lat = pos.coords.latitude;
                const lng = pos.coords.longitude;

                new google.maps.Marker({
                    position: { lat, lng },
                    map: map,
                    title: "Você está aqui",
                    icon: gestanteIcon,
                });

                map.setCenter({ lat, lng });
                buscarPostosGoogle(lat, lng);
            },
            error => {
                console.error("Erro ao obter localização:", error);
                alert("Não foi possível obter sua localização.");
            },
            {
                enableHighAccuracy: true,
                timeout: 10000,
                maximumAge: 0,
            }
        );
    }
};

function buscarPostosGoogle(lat, lng) {
    fetch(`/proxy-google-amplo/?lat=${lat}&lng=${lng}`)
        .then(response => response.json())
        .then(data => {
            postosDisponiveis = []; // Limpa antes de popular novamente
            const select = document.getElementById("id_posto");
            select.innerHTML = '<option value="">Selecione um posto</option>';

            data.results.forEach((posto, index) => {
                const name = posto.name;
                const address = posto.formatted_address;
                const location = posto.geometry.location;

                // Armazena no array
                postosDisponiveis.push({
                    nome: name,
                    endereco: address,
                    localizacao: {
                        lat: location.lat,
                        lng: location.lng
                    }
                });

                // Cria opção no select
                const option = document.createElement("option");
                option.value = index;
                option.textContent = `${name} - ${address}`;
                select.appendChild(option);

                // Cria marcador no mapa
                const marker = new google.maps.Marker({
                    position: location,
                    map: map,
                    title: name,
                    icon: heartIcon,
                });

                const infoWindow = new google.maps.InfoWindow({
                    content: `<strong>${name}</strong><br>${address}`,
                });

                marker.addListener("click", () => {
                    infoWindow.open(map, marker);
                    select.value = index; // Seleciona o posto ao clicar no mapa
                });
            });

            console.log("Postos disponíveis:", obterPostosComoJSON());
        })
        .catch(error => {
            console.error("Erro ao buscar postos:", error);
        });
}

// JSON dos postos
function obterPostosComoJSON() {
    return JSON.stringify(postosDisponiveis, null, 2);
}

// Exibe campo "outro exame"
document.addEventListener("DOMContentLoaded", () => {
    const exameSelect = document.getElementById("id_exame") || document.getElementById("exame");
    const outroContainer = document.getElementById("outro-exame-container");

    if (exameSelect) {
        exameSelect.addEventListener("change", () => {
            outroContainer.style.display = exameSelect.value === "Outro" ? "block" : "none";
        });
    }
});
