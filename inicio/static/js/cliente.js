
    function previewImage(event) {
        var input = event.target;
        var reader = new FileReader();

        reader.onload = function () {
            var img = document.getElementById("preview-img");
            img.src = reader.result;  // Atualiza a imagem na tela
        };

        reader.readAsDataURL(input.files[0]);  // Converte a imagem para visualização
    }
