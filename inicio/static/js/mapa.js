let map;
let infowindow;
let userLocation;

// Função de inicialização do mapa
function initMap() {
  // Define uma localização padrão caso a geolocalização falhe
  const defaultLocation = { lat: -23.55052, lng: -46.633308 }; // São Paulo, Brasil

  // Cria o mapa
  map = new google.maps.Map(document.getElementById("map"), {
    center: defaultLocation,
    zoom: 14,
  });

  // Inicializa a janela de informações
  infowindow = new google.maps.InfoWindow();

  // Verifica se a geolocalização é suportada
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition((position) => {
      // Obtém a localização do usuário
      userLocation = new google.maps.LatLng(position.coords.latitude, position.coords.longitude);

      // Centraliza o mapa na localização do usuário
      map.setCenter(userLocation);
      map.setZoom(14);

      // Criar marcador para a localização do usuário com ícone personalizado PNG
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

      // Buscar os postos de saúde mais próximos
      const service = new google.maps.places.PlacesService(map);
      const request = {
        location: userLocation,  // Aqui garantimos que a localização do usuário é passada corretamente
        radius: 140000, // Raio de 140 km
        query: 'posto de saúde OR SUS OR SESMA OR UTI OR hospital' // Modificação para incluir termos relevantes
      };

      // Usando google.maps.places.Place para buscar os postos de saúde
      service.textSearch(request, (results, status) => {
        if (status === google.maps.places.PlacesServiceStatus.OK) {
          results.forEach((place) => {
            createMarker(place);  // Criar o marcador para cada posto de saúde
            addPostoToTable(place);  // Adiciona o posto à tabela
          });
        } else {
          console.error("Erro ao buscar postos de saúde:", status);
        }
      });
    }, (error) => {
      // Caso de erro, usa a localização padrão
      console.error("Erro ao obter a localização:", error.message);
      alert("Não foi possível obter sua localização. O mapa será centralizado em São Paulo.");
      map.setCenter(defaultLocation);  // Centraliza o mapa em São Paulo
    });
  } else {
    // Caso a geolocalização não seja suportada, usa a localização padrão
    alert("Geolocalização não suportada pelo navegador. O mapa será centralizado em São Paulo.");
    map.setCenter(defaultLocation);  // Centraliza o mapa em São Paulo
  }

  // Adiciona o evento de clique no botão de localização atual
  document.getElementById("current-location-btn").addEventListener("click", function() {
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition((position) => {
        const currentLocation = new google.maps.LatLng(position.coords.latitude, position.coords.longitude);
        map.setCenter(currentLocation);
        map.setZoom(14);  // Ajuste o nível de zoom conforme necessário
        const userMarker = new google.maps.Marker({
          map: map,
          position: currentLocation,
          title: "Sua Localização",
          icon: {
            url: 'https://upload.wikimedia.org/wikipedia/commons/d/d7/Blue_heart_emoji.png',
            scaledSize: new google.maps.Size(30, 30)  // Ajusta o tamanho do ícone
          }
        });
      });
    }
  });
}

// Função para criar o marcador de posto de saúde e a rota
function createMarker(place) {
  const marker = new google.maps.Marker({
    map: map,
    position: place.geometry.location,
    title: place.name,
    icon: {
      url: 'https://i.ibb.co/zVvxwZLz/pngegg.png',  // Ícone personalizado para os postos
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
