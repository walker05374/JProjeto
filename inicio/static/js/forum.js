document.querySelectorAll('.comment-btn').forEach(button => {
    button.addEventListener('click', function() {
        const id = this.dataset.id;
        const isLiked = this.classList.contains('liked'); // Verificar se já foi curtido

        // Enviar o status de curtir ou descurtir
        fetch(`/curtir/${id}/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': document.querySelector('[name="csrfmiddlewaretoken"]').value,
                'Content-Type': 'application/json',  // Enviar como JSON
            },
            body: JSON.stringify({ like: !isLiked }) // Envia 'like: true' ou 'false'
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                this.classList.toggle('liked'); // Alterna a classe 'liked'
                const count = this.querySelector('.curtidas-num');
                let currentCount = parseInt(count.innerText) || 0;
                count.innerText = isLiked ? currentCount - 1 : currentCount + 1; // Atualiza o contador
            }
        })
        .catch(err => console.log(err));
    });
});
