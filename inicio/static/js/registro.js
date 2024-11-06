// Função para validar o preenchimento dos campos
function validateForm() {
    const inputs = document.querySelectorAll('#registroForm input');
    let allFilled = true;

    inputs.forEach(input => {
        if (input.value.trim() === '') {
            allFilled = false; // Se algum campo estiver vazio, define como falso
        }
    });

    // Habilita ou desabilita o botão de cadastro baseado no preenchimento
    const registerButton = document.getElementById('registerButton');
    registerButton.disabled = !allFilled; // Habilita o botão se todos os campos estiverem preenchidos
    registerButton.classList.toggle('disabled', !allFilled); // Adiciona/remover a classe 'disabled' para estilo
}

// Adiciona eventos de validação a todos os campos do formulário
const inputs = document.querySelectorAll('#registroForm input');
inputs.forEach(input => {
    input.addEventListener('input', validateForm); // Chama a função de validação em cada alteração
});

// Chama a função inicialmente para definir o estado do botão
validateForm();
