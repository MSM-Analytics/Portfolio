let next = document.getElementById('next')
let prev = document.getElementById('prev')
let container = document.querySelector('.container')
let list = container.querySelector('.list')
let item = container.querySelectorAll('.list .item')
let indicator = document.querySelector('.indicators')
let dot = indicator.querySelectorAll('ul li')

let active = 0
let first = 0
let last = item.length - 1

// Número inicial
const numberElement = document.querySelector('.number')
numberElement.textContent = String(active + 1).padStart(2, '0')


// ================= FUNÇÃO DE RESET =================
function resetDescription() {
    document.querySelectorAll('.description').forEach(d => d.classList.remove('show'))
    document.querySelectorAll('.arrow-icon').forEach(a => a.classList.remove('rotate'))
}


// ================= AUTO OPEN =================
function autoOpenDescription() {
    const activeItem = document.querySelector('.item.active')
    if (!activeItem) return

    const desc = activeItem.querySelector('.description')
    const arrow = activeItem.querySelector('.arrow-icon')

    setTimeout(() => {
        desc.classList.add('show')
        arrow.classList.add('rotate')
    }, 1200)
}


// ================= PREV =================
prev.onclick = () => {

    resetDescription() // 🔥 FECHA antes de trocar

    list.style.setProperty('--calculation', 1)

    let itemOld = container.querySelector('.list .item.active')
    let dotOld = indicator.querySelector('ul li.active')

    itemOld.classList.remove('active')
    dotOld.classList.remove('active')

    active = active + 1 > last ? first : active + 1

    let number = active + 1
    document.querySelector('.number').textContent = String(number).padStart(2, '0')

    item[active].classList.add('active')
    dot[active].classList.add('active')

    autoOpenDescription() // 🔥 ABRE depois
}


// ================= NEXT =================
next.onclick = () => {

    resetDescription() // 🔥 FECHA antes de trocar

    list.style.setProperty('--calculation', -1)

    let itemOld = container.querySelector('.list .item.active')
    let dotOld = indicator.querySelector('ul li.active')

    itemOld.classList.remove('active')
    dotOld.classList.remove('active')

    active = active - 1 < first ? last : active - 1

    let number = active + 1
    document.querySelector('.number').textContent = String(number).padStart(2, '0')

    item[active].classList.add('active')
    dot[active].classList.add('active')

    autoOpenDescription() // 🔥 ABRE depois
}


// ================= TOGGLE MANUAL =================
function toggleDescricao(btn) {
    const item = btn.closest('.item.active')
    if (!item) return

    const desc = item.querySelector('.description')
    const icon = btn.querySelector('.arrow-icon')

    if (!desc) return

    desc.classList.toggle('show')
    icon.classList.toggle('rotate')
}


// ================= LOAD INICIAL =================

window.addEventListener('DOMContentLoaded', () => {

    document.body.classList.add('loaded')

    const firstItem = document.querySelector('.item.active')
    if (!firstItem) return

    // força estado inicial IGUAL ao slide fora da tela
    list.style.setProperty('--calculation', 1)

    // tira active temporariamente
    firstItem.classList.remove('active')

    // força reflow REAL
    firstItem.offsetHeight

    // reaplica active → dispara animação
    firstItem.classList.add('active')

    // descrição depois da animação
    autoOpenDescription()
})

function toggleMenu() {
    const menu = document.querySelector('.menu')
    const btn = document.querySelector('.menu-mobile-btn')

    if (!menu || !btn) return

    menu.classList.toggle('open')
    btn.classList.toggle('active')
}