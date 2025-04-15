let map;
let infowindow;
let userLocation;

// Função de inicialização do mapa
function initMap() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition((position) => {
            userLocation = new google.maps.LatLng(position.coords.latitude, position.coords.longitude);

            // Criar o mapa centrado na localização do usuário
            map = new google.maps.Map(document.getElementById("map"), {
                center: userLocation,
                zoom: 14,
            });

            infowindow = new google.maps.InfoWindow();

            // Criar marcador para a localização do usuário com ícone personalizado sem fundo
            const userMarker = new google.maps.Marker({
                map: map,
                position: userLocation,
                title: "Sua localização",
                icon: {
                    url: 'https://upload.wikimedia.org/wikipedia/commons/d/d7/Blue_heart_emoji.png',  // Ícone de coração azul sem fundo
                    scaledSize: new google.maps.Size(30, 30)  // Ajusta o tamanho do ícone
                }
            });

            // Exibe o marcador quando o usuário clica na sua localização
            google.maps.event.addListener(userMarker, "click", () => {
                infowindow.setContent('<h3>Sua Localização</h3>');
                infowindow.open(map, userMarker);
            });

            // Refatoração da busca: incluindo termos como SUS, SESMA, UTI, hospital
            const request = {
                location: userLocation,
                radius: 140000, // Raio de 140 km
                query: 'posto de saúde OR SUS OR SESMA OR UTI OR hospital' // Modificação para incluir termos relevantes
            };
            
            const service = new google.maps.places.PlacesService(map);
            service.findPlaceFromQuery(request, (results, status) => {
                if (status === google.maps.places.PlacesServiceStatus.OK) {
                    results.forEach((place) => {
                        createMarker(place);
                        addPostoToTable(place);  // Adiciona o posto à tabela
                    });
                } else {
                    console.error("Erro ao buscar postos de saúde:", status);
                }
            });
            
            
        }, (error) => {
            console.error("Erro ao obter a localização:", error.message);
        });
    } else {
        alert("Geolocalização não suportada pelo navegador.");
    }
}

// Função para criar o marcador de posto de saúde e a rota
function createMarker(place) {
    const marker = new google.maps.Marker({
        map: map,
        position: place.geometry.location,
        title: place.name,
        icon: {
            url: 'https://upload.wikimedia.org/wikipedia/commons/5/5e/Heart_symbol_red.png',  // Ícone de coração vermelho sem fundo
            scaledSize: new google.maps.Size(30, 30)  // Ajusta o tamanho do ícone
        }
    });

    // Quando o marcador for clicado, mostra as informações detalhadas
    google.maps.event.addListener(marker, "click", () => {
        infowindow.setContent(`
            <h3>${place.name}</h3>
            <p>Endereço: ${place.formatted_address}</p>
            <img src="${place.photos ? place.photos[0].getUrl({ maxWidth: 200, maxHeight: 200 }) : ''}" alt="Foto do local" />
            <a href="https://www.google.com/maps/dir/?api=1&destination=${place.geometry.location.lat()},${place.geometry.location.lng()}" target="_blank">Como chegar</a>
        `);
        infowindow.open(map, marker);
    });
}

// Função para adicionar o posto à tabela
function addPostoToTable(place) {
    const postosList = document.getElementById("postos-list");

    const row = document.createElement("tr");

    const nomeCell = document.createElement("td");
    nomeCell.textContent = place.name;

    const enderecoCell = document.createElement("td");
    enderecoCell.textContent = place.formatted_address;

    const distanciaCell = document.createElement("td");
    // Calcular a distância em km (opcional)
    const distancia = calculateDistance(userLocation.lat(), userLocation.lng(), place.geometry.location.lat(), place.geometry.location.lng());
    distanciaCell.textContent = `${distancia.toFixed(2)} km`;

    const acaoCell = document.createElement("td");
    const link = document.createElement("a");
    link.href = `https://www.google.com/maps/dir/?api=1&destination=${place.geometry.location.lat()},${place.geometry.location.lng()}`;
    link.target = "_blank";
    link.textContent = "Rota";
    acaoCell.appendChild(link);

    row.appendChild(nomeCell);
    row.appendChild(enderecoCell);
    row.appendChild(distanciaCell);
    row.appendChild(acaoCell);

    postosList.appendChild(row);
}

// Função para calcular a distância entre dois pontos (em km)
function calculateDistance(lat1, lon1, lat2, lon2) {
    const R = 6371; // Raio da Terra em km
    const dLat = (lat2 - lat1) * Math.PI / 180;
    const dLon = (lon2 - lon1) * Math.PI / 180;
    const a = Math.sin(dLat / 2) * Math.sin(dLat / 2) +
              Math.cos(lat1 * Math.PI / 180) * Math.cos(lat2 * Math.PI / 180) *
              Math.sin(dLon / 2) * Math.sin(dLon / 2);
    const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
    return R * c; // Distância em km
}
