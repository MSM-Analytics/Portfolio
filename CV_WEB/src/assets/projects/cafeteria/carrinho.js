let cart = [];

const cartBox = document.getElementById('cart');
const cartIcon = document.querySelector('.cart-icon');
const cartWrapper = document.getElementById('cartWrapper');
const cartContainer = document.querySelector('.cart-items');
const totalSpan = document.querySelector('.cart-total span');
const countElement = document.querySelector('.cart-count');
const checkoutBtn = document.querySelector('.checkout-btn');
const buttons = document.querySelectorAll('.add-to-cart');

// ─── ADD TO CART ──────────────────────────────────────────────
function addToCart(name, price) {
    const existing = cart.find(item => item.name === name);
    if (existing) {
        existing.quantity++;
    } else {
        cart.push({ name, price, quantity: 1 });
    }
    updateCart();
}

// ─── UPDATE CART ──────────────────────────────────────────────
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
            <span>${item.quantity}×</span>
            <span>R$ ${(item.price * item.quantity).toFixed(2)}</span>
            <button class="remove-item" data-index="${index}" aria-label="Remover">✕</button>
        `;
        cartContainer.appendChild(div);
    });

    if (totalSpan) totalSpan.textContent = total.toFixed(2).replace('.', ',');
    if (countElement) {
        countElement.textContent = totalItems;
        // Pulse count badge
        countElement.classList.add('bump');
        setTimeout(() => countElement.classList.remove('bump'), 300);
    }

    if (checkoutBtn) checkoutBtn.disabled = cart.length === 0;
}

// ─── REMOVE ITEM ──────────────────────────────────────────────
document.addEventListener('click', (e) => {
    if (e.target.classList.contains('remove-item')) {
        const index = parseInt(e.target.dataset.index);
        const item = e.target.closest('.cart-item');
        if (item) {
            item.style.transform = 'translateX(20px)';
            item.style.opacity = '0';
            item.style.transition = 'all 0.3s ease';
            setTimeout(() => {
                cart.splice(index, 1);
                updateCart();
            }, 280);
        }
    }
});

// ─── OPEN / CLOSE CART ────────────────────────────────────────
if (cartWrapper) {
    cartWrapper.addEventListener('click', () => {
        cartBox.classList.toggle('active');
        document.body.style.overflow = cartBox.classList.contains('active') ? 'hidden' : '';
    });
}

// Close when clicking outside
document.addEventListener('click', (e) => {
    if (cartBox.classList.contains('active') &&
        !cartBox.contains(e.target) &&
        !cartWrapper.contains(e.target)) {
        cartBox.classList.remove('active');
        document.body.style.overflow = '';
    }
});

// ─── FLY TO CART ANIMATION ────────────────────────────────────
function flyToCart(imgElement) {
    const cartIconEl = document.querySelector('.cart-icon');
    if (!cartIconEl || !imgElement) return;

    const imgRect = imgElement.getBoundingClientRect();
    const cartRect = cartIconEl.getBoundingClientRect();

    const clone = document.createElement('div');
    clone.style.cssText = `
        position: fixed;
        top: ${imgRect.top + imgRect.height / 2}px;
        left: ${imgRect.left + imgRect.width / 2}px;
        width: 12px;
        height: 12px;
        background: var(--gold, #c9a96e);
        border-radius: 50%;
        pointer-events: none;
        z-index: 9999;
        transform: translate(-50%, -50%) scale(3);
        transition: all 0.7s cubic-bezier(0.55, 0, 0.3, 1);
        opacity: 1;
    `;
    document.body.appendChild(clone);

    // Force reflow
    clone.getBoundingClientRect();

    // Animate to cart
    clone.style.top = (cartRect.top + cartRect.height / 2) + 'px';
    clone.style.left = (cartRect.left + cartRect.width / 2) + 'px';
    clone.style.transform = 'translate(-50%, -50%) scale(0.5)';
    clone.style.opacity = '0';

    // Bump cart icon
    cartIconEl.classList.add('bump');
    setTimeout(() => cartIconEl.classList.remove('bump'), 400);

    setTimeout(() => clone.remove(), 750);
}

// ─── ADD TO CART CLICK HANDLER ────────────────────────────────
buttons.forEach(btn => {
    btn.addEventListener('click', (e) => {
        e.preventDefault();

        const name = btn.dataset.name;
        const price = parseFloat(btn.dataset.price);
        const box = btn.closest('.box');
        const img = box ? box.querySelector('img') : null;

        // Button feedback
        btn.style.transform = 'scale(0.95)';
        setTimeout(() => btn.style.transform = '', 200);

        flyToCart(img);
        addToCart(name, price);
    });
});

// ─── CHECKOUT BUTTON ──────────────────────────────────────────
if (checkoutBtn) {
    checkoutBtn.addEventListener('click', () => {
        if (cart.length === 0) return;
        alert('Redirecionando para pagamento...');
    });
}

// ─── SWIPE DOWN TO CLOSE (MOBILE) ────────────────────────────
let touchStartY = 0;
let isDragging = false;

cartBox.addEventListener('touchstart', (e) => {
    touchStartY = e.touches[0].clientY;
    isDragging = true;
    cartBox.style.transition = 'none';
}, { passive: true });

cartBox.addEventListener('touchmove', (e) => {
    if (!isDragging || !cartBox.classList.contains('active')) return;

    const diff = e.touches[0].clientY - touchStartY;

    if (diff > 0 && cartContainer.scrollTop === 0) {
        cartBox.style.transform = `translateY(${diff}px)`;
        e.preventDefault();
    }
}, { passive: false });

cartBox.addEventListener('touchend', (e) => {
    if (!isDragging) return;
    isDragging = false;
    const diff = e.changedTouches[0].clientY - touchStartY;
    cartBox.style.transition = '';
    cartBox.style.transform = '';

    if (diff > 100) {
        cartBox.classList.remove('active');
        document.body.style.overflow = '';
    }
});

// ─── INIT ─────────────────────────────────────────────────────
updateCart();
