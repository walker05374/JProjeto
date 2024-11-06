function findCEP2(){
    let cep = document.getElementById('id_cep').value;
    console.log(cep);
    let url = "https://viacep.com.br/ws/"+cep+"/json/";
    console.log(url);
    fetch(url)
        .then((response)=>response.json())
        .then((data)=>{
            console.log(data);
            document.getElementById('id_endereco').value=data.logradouro;
            document.getElementById('id_bairro').value=data.bairro;
            document.getElementById('id_cidade').value=data.localidade;
            document.getElementById('id_uf').value=data.uf;
        })
        .catch((error)=>console.log("deu erro "+error));
}

function findCEP(){
    let cep = document.getElementById('cep').value;
    console.log(cep);
    let url = "https://viacep.com.br/ws/"+cep+"/json/";
    console.log(url);
    fetch(url)
        .then((response)=>response.json())
        .then((data)=>{
            console.log(data);
            document.getElementById('result').innerText=data.localidade})
        .catch((error)=>console.log("deu erro "+error));
}
