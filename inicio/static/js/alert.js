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

// CORREÇÃO: Verifica se o elemento "foto-upload" existe antes de adicionar o evento
const fotoUpload = document.getElementById("foto-upload");
if (fotoUpload) {
    fotoUpload.addEventListener("change", function(event) {
        var reader = new FileReader();

        reader.onload = function() {
            // Atualiza a imagem com a nova foto selecionada
            const profileImg = document.getElementById("profile-img");
            if (profileImg) {
                profileImg.src = reader.result;
            }
        };

        // Lê o arquivo selecionado
        reader.readAsDataURL(event.target.files[0]);
    });
}

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

// CORREÇÃO: Verifica se o modal existe antes de tentar abri-lo
const deleteModalElement = document.getElementById('confirmDeleteModal');
if (deleteModalElement) {
    var myModal = new bootstrap.Modal(deleteModalElement);
    // Atenção: Esta linha abaixo faz o modal abrir automaticamente assim que a página carrega.
    // Se essa não for a intenção, remova ou comente a linha 'myModal.show()'.
    myModal.show();
}