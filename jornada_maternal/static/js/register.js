
  document.addEventListener('DOMContentLoaded', function () {
    // Verifique se o usuário está sendo redirecionado da página de cadastro
    const redirectFromRegister = window.location.href.includes('?registered=true');

    // Se o usuário estiver vindo da página de cadastro, exiba o alerta
    if (redirectFromRegister) {
      document.getElementById('success-alert').style.display = 'block';
    }
  });

