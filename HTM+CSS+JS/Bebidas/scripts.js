// criar lista de itens
let list = document.querySelectorAll('.item')

// Selecionar os botões
let next = document.getElementById('next')
let prev = document.getElementById('prev')

// Contar quantos itens a lista contem
let count = list.length

// Item ativo
let active = 0

//########################################//
// Trocar de item ao clicar no botão next //
//########################################//
// Capturar click no botão next
next.onclick = () => {
    // Localizar item ativo 
    let activeOld = document.querySelector('.active')
    // Remover a classe active
    activeOld.classList.remove('active')
    // Trocar para o próximo item 
    // ( Validando se active está no último item da lista
    // e retornando para o primeiro item)
    active = active >= count -1 ? 0 : active + 1 
    // Adicionar a classe active no próximo item
    list[active].classList.add('active')
}

//########################################//
// Trocar de item ao clicar no botão prev //
//########################################//
// Capturar click no botão prev
prev.onclick = () => {
    // Localizar item ativo 
    let activeOld = document.querySelector('.active')
    // Remover a classe active
    activeOld.classList.remove('active')
    // Trocar para o item anterior 
    // ( Validando se active está no primeiro item da lista
    // e retornando para o último item)
    active = active <= 0 ? count - 1 : active - 1 
    // Adicionar a classe active no próximo item
    list[active].classList.add('active')
}
