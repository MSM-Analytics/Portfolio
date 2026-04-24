let cart = [];

// Elementos principais
const buttons = document.querySelectorAll('.add-to-cart');
const cartBox = document.querySelector('.cart');
const cartIcon = document.querySelector('.cart-icon');

const cartContainer = document.querySelector('.cart-items');
const totalElement = document.querySelector('.cart-total');
const countElement = document.querySelector('.cart-count');

// Adicionar ao carrinho
buttons.forEach(btn => {
    btn.addEventListener('click', (e) => {
        e.preventDefault();

        const name = btn.dataset.name;
        const price = parseFloat(btn.dataset.price);

        addToCart(name, price);
    });
});

function addToCart(name, price) {
    const existing = cart.find(item => item.name === name);

    if (existing) {
        existing.quantity++;
    } else {
        cart.push({ name, price, quantity: 1 });
    }

    updateCart();
}

function updateCart() {
    cartContainer.innerHTML = '';

    let total = 0;
    let totalItems = 0;

    cart.forEach((item, index) => {
        total += item.price * item.quantity;
        totalItems += item.quantity;

        const div = document.createElement('div');
        div.classList.add('cart-item');

        div.innerHTML = `
            <span>${item.name}</span>
            <span>${item.quantity}x</span>
            <span>R$ ${(item.price * item.quantity).toFixed(2)}</span>
            <button class="remove-item" data-index="${index}">❌</button>
        `;

        cartContainer.appendChild(div);
    });

    totalElement.innerText = `Total: R$ ${total.toFixed(2)}`;
    countElement.innerText = totalItems;
}

// Remover item
function removeItem(index) {
    cart.splice(index, 1);
    updateCart();
}

document.addEventListener('click', (e) => {
    if (e.target.classList.contains('remove-item')) {
        const index = e.target.dataset.index;
        removeItem(index);
    }
});

// Abrir/fechar carrinho
if (cartIcon) {
    cartIcon.addEventListener('click', () => {
        cartBox.classList.toggle('active');
    });
}