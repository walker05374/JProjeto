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
