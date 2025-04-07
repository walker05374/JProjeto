function findCEP2() {
    let cep = document.getElementById('id_cep').value.trim();
    let errorDiv = document.getElementById('cep-error');
    errorDiv.innerText = "";

    if (cep.length !== 8 || isNaN(cep)) {
        errorDiv.innerText = "❌ CEP inválido. Digite apenas os 8 números.";
        return;
    }

    let url = "https://viacep.com.br/ws/" + cep + "/json/";

    fetch(url)
        .then(response => response.json())
        .then(data => {
            if (data.erro) {
                errorDiv.innerText = "❌ CEP não encontrado.";
            } else {
                document.getElementById('id_endereco').value = data.logradouro;
                document.getElementById('id_bairro').value = data.bairro;
                document.getElementById('id_cidade').value = data.localidade;
                document.getElementById('id_uf').value = data.uf;
            }
        })
        .catch(error => {
            console.log("Erro na requisição:", error);
            errorDiv.innerText = "❌ Erro ao buscar o CEP. Tente novamente.";
        });
}
