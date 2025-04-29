

document.addEventListener("DOMContentLoaded", function() {
  const popup = document.getElementById("popup");
  const closeButton = document.getElementById("closeButton");
  const alert = document.querySelector('.alert');

  // Exibir o popup se houver
  if (popup && closeButton) {
      popup.style.display = "block";

      closeButton.addEventListener("click", function() {
          popup.style.display = "none";
      });
  }

  // Fechar o alerta após 5 segundos
  if (alert) {
      setTimeout(function() {
          alert.classList.add('fade');
          alert.classList.remove('show');
      }, 5000); // Fecha o alerta após 5 segundos
  }

  // Fechar o alerta ao clicar no "X"
  const closeAlertButton = document.querySelector('.alert .close');
  if (closeAlertButton) {
      closeAlertButton.addEventListener("click", function() {
          alert.classList.add('fade');
          alert.classList.remove('show');
      });
  }
});


document.getElementById("foto-upload").addEventListener("change", function(event) {
    var reader = new FileReader();

    reader.onload = function() {
        // Atualiza a imagem com a nova foto selecionada
        document.getElementById("profile-img").src = reader.result;
    };

    // Lê o arquivo selecionado
    reader.readAsDataURL(event.target.files[0]);
});


function previewImage(event) {
    const reader = new FileReader();
    reader.onload = function () {
        document.getElementById('preview-img').src = reader.result;
    }
    reader.readAsDataURL(event.target.files[0]);
}



// Abre o modal programaticamente
var myModal = new bootstrap.Modal(document.getElementById('confirmDeleteModal'));
myModal.show();


setTimeout(function(){
    location.reload();
}, 5000); 
