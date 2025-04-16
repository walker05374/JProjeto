document.getElementById("weekForm").addEventListener("submit", function(event) {
    event.preventDefault();

    const week = document.getElementById("week").value;
    displayDevelopmentInfo(week);
    generateBabyImage(week);
});

function displayDevelopmentInfo(week) {
    const infoElement = document.getElementById("development-info");
    
    let developmentInfo = "";

    if (week >= 1 && week <= 4) {
        developmentInfo = "Seu bebê é do tamanho de um grão de arroz, começando a formar os primeiros brotos que irão se tornar braços e pernas.";
    } else if (week >= 5 && week <= 8) {
        developmentInfo = "O coração do bebê começa a bater, e as mãos e dedos começam a se formar.";
    } else if (week >= 9 && week <= 12) {
        developmentInfo = "O rosto do bebê já está quase completo, com os olhos formados e o início do cérebro funcionando.";
    } else if (week >= 13 && week <= 16) {
        developmentInfo = "O bebê começa a mover os braços e pernas, e a pele ainda é transparente.";
    } else if (week >= 17 && week <= 20) {
        developmentInfo = "O bebê pode ouvir sons e tem movimentos mais intensos, especialmente à noite.";
    } else if (week >= 21 && week <= 24) {
        developmentInfo = "O bebê já começa a piscar os olhos, e seu corpo está cobrindo-se com o vérnix.";
    } else if (week >= 25 && week <= 28) {
        developmentInfo = "O bebê tem mais de 30 cm e já pode perceber luz e sombras.";
    } else if (week >= 29 && week <= 32) {
        developmentInfo = "O bebê já está se posicionando para o nascimento e seus ossos estão se tornando mais fortes.";
    } else if (week >= 33 && week <= 36) {
        developmentInfo = "O bebê está ganhando peso rapidamente e se preparando para nascer.";
    } else if (week >= 37 && week <= 40) {
        developmentInfo = "O bebê está totalmente formado, mas precisa de mais tempo para amadurecer antes do nascimento.";
    } else {
        developmentInfo = "Por favor, insira uma semana válida de gestação (1 a 40).";
    }

    infoElement.textContent = developmentInfo;
}

function generateBabyImage(week) {
    const babyModel = document.getElementById("babyModel");

    // Definindo as imagens do desenvolvimento
    const babyImages = {
        1: "/static/images/formacaobebe/fetus_week_1.png",
        2: "/static/images/formacaobebe/fetus_week_2.png",
        3: "/static/images/formacaobebe/fetus_week_3.png",
        4: "/static/images/formacaobebe/fetus_week_4.png",
        5: "/static/images/formacaobebe/fetus_week_5.png",
        6: "/static/images/formacaobebe/fetus_week_6.png",
        7: "/static/images/formacaobebe/fetus_week_7.png",
        8: "/static/images/formacaobebe/fetus_week_8.png",
        9: "/static/images/formacaobebe/fetus_week_9.png",
        10: "/static/images/formacaobebe/fetus_week_10.png",
        11: "/static/images/formacaobebe/fetus_week_11.png",
        12: "/static/images/formacaobebe/fetus_week_12.png",
        13: "/static/images/formacaobebe/fetus_week_13.png",
        14: "/static/images/formacaobebe/fetus_week_14.png",
        15: "/static/images/formacaobebe/fetus_week_15.png",
        16: "/static/images/formacaobebe/fetus_week_16.png",
        17: "/static/images/formacaobebe/fetus_week_17.png",
        18: "/static/images/formacaobebe/fetus_week_18.png",
        19: "/static/images/formacaobebe/fetus_week_19.png",
        20: "/static/images/formacaobebe/fetus_week_20.png",
        21: "/static/images/formacaobebe/fetus_week_21.png",
        22: "/static/images/formacaobebe/fetus_week_22.png",
        23: "/static/images/formacaobebe/fetus_week_23.png",
        24: "/static/images/formacaobebe/fetus_week_24.png",
        25: "/static/images/formacaobebe/fetus_week_25.png",
        26: "/static/images/formacaobebe/fetus_week_26.png",
        27: "/static/images/formacaobebe/fetus_week_27.png",
        28: "/static/images/formacaobebe/fetus_week_28.png",
        29: "/static/images/formacaobebe/fetus_week_29.png",
        30: "/static/images/formacaobebe/fetus_week_30.png",
        31: "/static/images/formacaobebe/fetus_week_31.png",
        32: "/static/images/formacaobebe/fetus_week_32.png",
        33: "/static/images/formacaobebe/fetus_week_33.png",
        34: "/static/images/formacaobebe/fetus_week_34.png",
        35: "/static/images/formacaobebe/fetus_week_35.png",
        36: "/static/images/formacaobebe/fetus_week_36.png",
        37: "/static/images/formacaobebe/fetus_week_37.png",
        38: "/static/images/formacaobebe/fetus_week_38.png",
        39: "/static/images/formacaobebe/fetus_week_39.png",
        40: "/static/images/formacaobebe/fetus_week_40.png"
        
    };

    // Alterando a imagem com base na semana inserida
    if (babyImages[week]) {
        babyModel.innerHTML = `<img src="${babyImages[week]}" alt="Desenvolvimento do Bebê" width="100%" height="100%">`;
    } else {
        babyModel.innerHTML = "<p>Semana inválida! Insira uma semana entre 1 e 40.</p>";
    }
}



