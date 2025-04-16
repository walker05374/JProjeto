// Quando o gráfico de peso for enviado via e-mail, ele usa esse script
document.querySelectorAll('.btn-enviar-email').forEach(btn => {
    btn.addEventListener('click', function(e) {
        e.preventDefault();
        let icon = this.querySelector('i');
        icon.classList.add('active');
        
        setTimeout(() => {
            window.location.href = this.getAttribute('href');
        }, 300); // tempo da animação
    });
});
