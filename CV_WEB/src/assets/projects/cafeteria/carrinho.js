let cart = [];

// Elementos principais
const buttons = document.querySelectorAll('.add-to-cart');
const cartBox = document.querySelector('.cart');
const cartIcon = document.querySelector('.cart-icon');

const cartContainer = document.querySelector('.cart-items');
const totalElement = document.querySelector('.cart-total');
const countElement = document.querySelector('.cart-count');
const checkoutBtn = document.querySelector('.checkout-btn');

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

        // 🔥 animação só quando cria
        div.classList.add('item-enter');

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

    if (checkoutBtn) {
        checkoutBtn.disabled = cart.length === 0;
    }
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

// Item voando parao carrinho

function flyToCart(imgElement) {

    const imgRect = imgElement.getBoundingClientRect();
    const cartRect = cartIcon.getBoundingClientRect();
    const clone = imgElement.cloneNode(true);

    clone.style.position = 'fixed';
    clone.style.top = imgRect.top + 'px';
    clone.style.left = imgRect.left + 'px';
    clone.style.width = imgRect.width + 'px';
    clone.style.height = imgRect.height + 'px';
    clone.style.zIndex = 9999;
    clone.style.pointerEvents = 'none';
    clone.style.transition = 'all 0.8s cubic-bezier(.65,-0.55,.25,1.55)';
    clone.style.borderRadius = '50%';

    document.body.appendChild(clone);

    // força render antes da animação
    clone.getBoundingClientRect();

    // 🔥 anima até o carrinho
    clone.style.top = cartRect.top + 'px';
    clone.style.left = cartRect.left + 'px';
    clone.style.width = '20px';
    clone.style.height = '20px';
    clone.style.opacity = '0.5';

    // 🔥 efeito bump no carrinho
    cartIcon.classList.add('bump');
    setTimeout(() => {
        cartIcon.classList.remove('bump');
    }, 300);

    // remove o clone após animação
    setTimeout(() => {
        clone.remove();
    }, 800);
}

buttons.forEach(btn => {
    btn.addEventListener('click', (e) => {
        e.preventDefault();

        const name = btn.dataset.name;
        const price = parseFloat(btn.dataset.price);

        const box = btn.closest('.box');
        const img = box.querySelector('img');

        flyToCart(img); // 🔥 AQUI

        addToCart(name, price);
    });
});

if (checkoutBtn) {
    checkoutBtn.addEventListener('click', () => {
        if (cart.length === 0) {
            alert('Seu carrinho está vazio!');
            return;
        }

        alert('Redirecionando para pagamento...');

        // integrar depois:
        // - Stripe
        // - Mercado Pago
        // - Checkout próprio
    });
}

updateCart();