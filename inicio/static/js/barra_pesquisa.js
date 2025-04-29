
    document.addEventListener("DOMContentLoaded", function() {
        const searchButton = document.getElementById("search-button");
        const searchInput = document.getElementById("search-input");

        searchButton.addEventListener("click", function() {
            const searchTerm = searchInput.value;
            if (searchTerm.trim() !== "") {
                window.location.href = `/search/?q=${encodeURIComponent(searchTerm)}`;
            }
        });
    });


setTimeout(function(){
        location.reload();
    }, 5000);  // 5000 milissegundos (5 segundos) - você pode ajustar o tempo
 
    