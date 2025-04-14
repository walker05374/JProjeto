let map;
let infowindow;

// Função de inicialização do mapa
function initMap() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition((position) => {
            const userLocation = new google.maps.LatLng(position.coords.latitude, position.coords.longitude);

            // Criar o mapa centrado na localização do usuário
            map = new google.maps.Map(document.getElementById("map"), {
                center: userLocation,
                zoom: 14,
            });

            infowindow = new google.maps.InfoWindow();

            // Criação do request para busca de postos de saúde ao redor da localização
            const request = {
                location: userLocation,
                radius: 5000, // Raio de 5km para buscar postos de saúde
                query: 'posto de saúde'
            };

            // Usar o novo serviço Places para fazer a busca de postos de saúde
            const service = new google.maps.places.PlacesService(map);
            service.textSearch(request, (results, status) => {
                if (status === google.maps.places.PlacesServiceStatus.OK) {
                    results.forEach((place) => {
                        createMarker(place);
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

// Função para criar um marcador no mapa para cada posto de saúde
function createMarker(place) {
    const marker = new google.maps.Marker({
        map: map,
        position: place.geometry.location,
        title: place.name
    });

    // Quando o marcador for clicado, mostra as informações detalhadas
    google.maps.event.addListener(marker, "click", () => {
        infowindow.setContent(`
            <h3>${place.name}</h3>
            <p>Endereço: ${place.formatted_address}</p>
            <a href="https://www.google.com/maps/dir/?api=1&destination=${place.geometry.location.lat()},${place.geometry.location.lng()}" target="_blank">Como chegar</a>
        `);
        infowindow.open(map, marker);
    });
}
