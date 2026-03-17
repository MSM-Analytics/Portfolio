let next = document.getElementById('next') // Seleciona o botão next
let prev = document.getElementById('prev') // seleciona o botão prev
let container = document.querySelector('.container') // seleciona o container de itens da página
let list = container.querySelector('.list') // seleciona a lista de itens
let item = container.querySelectorAll('.list .item') // seleciona todos os itens da página
let indicator = document.querySelector('.indicators') // seleciona o container de indicador
let dot = indicator.querySelectorAll('ul li') // seleciona todos os indicadores

let active = 0 // inicia a variável active em 0
let first = 0 // inicia a lista de conteúdo na primeira posição
let last = item.length - 1 // inicia a lista de conteúdo na última posição

// Seta numeração inicial do number em 01
const numberElement = document.querySelector('.number') // atribui .number a variável numberElement
numberElement.textContent = String(active + 1).padStart(2, '0') // atribui o valor inicial de number e formata o número

// Cria o evento click no botão prev
prev.onclick = () => {
    list.style.setProperty('--calculation', 1) // muda a direção da animação "da direita para a esquerda"

    let itemOld = container.querySelector('.list .item.active') // seleciona o item ativo
    let dotOld = indicator.querySelector('ul li.active') // seleciona o indicador ativo

    itemOld.classList.remove('active') // remove a classe active do ítem ativo
    dotOld.classList.remove('active') // remove a classe active do indicador ativo

    active = active + 1 > last ? first : active + 1 // calcula o novo valor de active após o click

    let number = active + 1 // calcua o novo valor de number após o click
    // atribui o novo valor de number e formata o número
    document.querySelector('.number').textContent = String(number).padStart(2, '0')

    item[active].classList.add('active') // seleciona o próximo item e atribui a classe active
    dot[active].classList.add('active') // seleciona o próximo indicador e atribui a classe active
}

// Cria o evento click no botão next
next.onclick = () => {
    list.style.setProperty('--calculation', -1) // muda a direção da animação "da esquerda para a direita"
    
    let itemOld = container.querySelector('.list .item.active') // seleciona o item ativo
    let dotOld = indicator.querySelector('ul li.active') // seleciona o indicador ativo

    itemOld.classList.remove('active') // remove a classe active do ítem ativo
    dotOld.classList.remove('active') // remove a classe active do indicador ativo

    active = active - 1 < first ? last : active - 1 // calcula o novo valor de active após o click

    let number = active + 1 // calcua o novo valor de number após o click
    // atribui o novo valor de number e formata o número
    document.querySelector('.number').textContent = String(number).padStart(2, '0')

    item[active].classList.add('active') // seleciona o item anterior e atribui a classe active
    dot[active].classList.add('active') // seleciona o indicador anterior e atribui a classe active
}