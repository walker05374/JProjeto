let heartIcon, gestanteIcon, map;

function initMap() {
  const defaultCenter = { lat: -23.5505, lng: -46.6333 }; // fallback

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

        // Aqui é onde tudo acontece
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
}

function buscarPostosGoogle(lat, lng) {
  fetch(`/proxy-google-amplo/?lat=${lat}&lng=${lng}`)
    .then(response => response.json())
    .then(data => {
      const apiKey = document.getElementById("map").dataset.apiKey;

      const select = document.getElementById("id_posto");
      select.innerHTML = '<option value="">Selecione um posto</option>';

      data.results.forEach(posto => {
        const name = posto.name;
        const address = posto.formatted_address;
        const location = posto.geometry.location;

        // Preenche o <select>
        const option = document.createElement("option");
        option.value = `${name} - ${address}`;
        option.textContent = `${name} - ${address}`;
        select.appendChild(option);

        // Mostra marcador no mapa
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
        });
      });
    })
    .catch(error => {
      console.error("Erro ao buscar postos:", error);
    });
}

// Mostrar campo "Outro exame" dinamicamente
document.addEventListener("DOMContentLoaded", () => {
  const exameSelect = document.getElementById("exame");
  const outroContainer = document.getElementById("outro-exame-container");

  exameSelect.addEventListener("change", () => {
    outroContainer.style.display = exameSelect.value === "Outro" ? "block" : "none";
  });
});

window.initMap = initMap;
