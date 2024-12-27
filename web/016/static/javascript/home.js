


// esquema para troca de menu atraves do botão configurações

const btn_config = document.getElementById('btn_config');
const menu_lateral_esquerdo_1 = document.getElementsByClassName('menu_lateral_esquerdo_1')[0];
const menu_lateral_esquerdo_2 = document.getElementsByClassName('menu_lateral_esquerdo_2')[0];
const btn_voltar_config = document.getElementById('btn_voltar_config');


btn_config.addEventListener('click', function() {
    menu_lateral_esquerdo_1.style.display = 'none';
    menu_lateral_esquerdo_2.style.display = 'block';
})


btn_voltar_config.addEventListener('click', function(){
    menu_lateral_esquerdo_1.style.display = 'block';
    menu_lateral_esquerdo_2.style.display = 'none';
})
