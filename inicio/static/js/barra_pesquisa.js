
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
