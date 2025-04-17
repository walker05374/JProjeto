$(document).ready(function() {
    // Inicialmente o spinner estará oculto
    $('#loading-spinner').hide();
  
    // Quando o formulário for submetido
    $('#login-form').on('submit', function(e) {
      // Exibe o ícone de carregamento
      $('#loading-spinner').show();
      // Oculta o botão de enviar para evitar múltiplos cliques
      $('#submit-btn').hide();
  
      // Impede o envio do formulário para realizar o processo assíncrono (ajax)
      e.preventDefault();
  
      // Simula um delay para fins de demonstração (substitua pela sua lógica de envio)
      setTimeout(function() {
        // Após a simulação de envio, envie o formulário normalmente
        $('#login-form')[0].submit(); // Submete o formulário de maneira tradicional
      }, 1000);  // 1 segundo para fins de simulação (você pode remover isso na produção)
    });
  });
  