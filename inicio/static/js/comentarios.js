
    // Mostrar ou ocultar o formulário de resposta
    const replyButtons = document.querySelectorAll('[href^="#resposta_"]');
    replyButtons.forEach(button => {
        button.addEventListener('click', function(event) {
            event.preventDefault();  // Previne o link de ser seguido
            const id = this.getAttribute('href').substring(9); // Extrai o ID do comentário
            const form = document.getElementById(`resposta_${id}`);
            if (form.style.display === "none" || form.style.display === "") {
                form.style.display = "block";
            } else {
                form.style.display = "none";
            }
        });
    });



    document.querySelectorAll('.btn-curtir').forEach(btn => {
        btn.addEventListener('click', function(e) {
            // Adiciona a classe 'active' para animar o ícone
            e.preventDefault();
            let icon = this.querySelector('i');
            icon.classList.add('active');
            
            // Redireciona após a animação
            setTimeout(() => {
                window.location.href = this.getAttribute('href');
            }, 300); // O tempo da animação
        });
    });



    function toggleReplyForm(commentId) {
        const form = document.getElementById('resposta_' + commentId);
        form.style.display = form.style.display === 'none' ? 'block' : 'none';
    }

