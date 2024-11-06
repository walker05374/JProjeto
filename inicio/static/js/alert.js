document.addEventListener("DOMContentLoaded", function() {
  const popup = document.getElementById("popup");
  const closeButton = document.getElementById("closeButton");

  if (popup && closeButton) {
    popup.style.display = "block";

    closeButton.addEventListener("click", function() {
      popup.style.display = "none";
    });
  }
});