document.addEventListener("DOMContentLoaded", function() {
  // === Lógica dos Alertas e Popups ===
  const popup = document.getElementById("popup");
  const closeButton = document.getElementById("closeButton");
  const alert = document.querySelector('.alert');

  if (popup && closeButton) {
      popup.style.display = "block";
      closeButton.addEventListener("click", function() {
          popup.style.display = "none";
      });
  }

  if (alert) {
      setTimeout(function() {
          alert.classList.add('fade');
          alert.classList.remove('show');
      }, 5000);
      
      const closeAlertButton = document.querySelector('.alert .close');
      if (closeAlertButton) {
          closeAlertButton.addEventListener("click", function() {
              alert.classList.add('fade');
              alert.classList.remove('show');
          });
      }
  }

  // === Lógica de Upload de Foto ===
  const fotoUpload = document.getElementById("foto-upload");
  if (fotoUpload) {
      fotoUpload.addEventListener("change", function(event) {
          var reader = new FileReader();
          reader.onload = function() {
              const profileImg = document.getElementById("profile-img");
              if (profileImg) {
                  profileImg.src = reader.result;
              }
          };
          reader.readAsDataURL(event.target.files[0]);
      });
  }

  // === CORREÇÃO DO ERRO BOOTSTRAP ===
  // Movemos a lógica do modal para DENTRO do DOMContentLoaded
  // e verificamos se o 'bootstrap' existe antes de usar.
  const confirmDeleteModal = document.getElementById('confirmDeleteModal');
  
  if (confirmDeleteModal && typeof bootstrap !== 'undefined') {
      // Apenas inicializa se o modal existir na página
      // Nota: Não chamamos .show() automaticamente aqui, a menos que seja a intenção abrir ao carregar a página.
      // Se a intenção era abrir ao clicar no botão de excluir, o Bootstrap já faz isso via data-bs-toggle no HTML.
      var myModal = new bootstrap.Modal(confirmDeleteModal);
      
      // Se você queria que o modal abrisse automaticamente ao carregar a página em algum caso específico, descomente abaixo:
      // myModal.show();
  }
});

function previewImage(event) {
    const reader = new FileReader();
    reader.onload = function () {
        const previewImg = document.getElementById('preview-img');
        if (previewImg) {
            previewImg.src = reader.result;
        }
    }
    reader.readAsDataURL(event.target.files[0]);
}