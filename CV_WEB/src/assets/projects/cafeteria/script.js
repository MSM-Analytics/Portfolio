// ─── PAGE LOADER ──────────────────────────────────────────────
window.addEventListener('load', () => {
    setTimeout(() => {
        const loader = document.getElementById('pageLoader');
        loader.classList.add('hidden');
    }, 1200);
});

// ─── CUSTOM CURSOR ────────────────────────────────────────────
const cursor = document.getElementById('cursor');
const cursorRing = document.getElementById('cursorRing');

let mouseX = 0, mouseY = 0;
let ringX = 0, ringY = 0;

if (cursor && cursorRing) {
    document.addEventListener('mousemove', (e) => {
        mouseX = e.clientX;
        mouseY = e.clientY;
        cursor.style.left = mouseX + 'px';
        cursor.style.top = mouseY + 'px';
    });

    // Smooth ring follow with lerp
    function animateCursor() {
        ringX += (mouseX - ringX) * 0.12;
        ringY += (mouseY - ringY) * 0.12;
        cursorRing.style.left = ringX + 'px';
        cursorRing.style.top = ringY + 'px';
        requestAnimationFrame(animateCursor);
    }
    animateCursor();

    // Hover effect on interactive elements
    const hoverTargets = document.querySelectorAll('a, button, .cart-wrapper, .box, .menu-toggle, svg');
    hoverTargets.forEach(el => {
        el.addEventListener('mouseenter', () => {
            cursor.classList.add('hover');
            cursorRing.classList.add('hover');
        });
        el.addEventListener('mouseleave', () => {
            cursor.classList.remove('hover');
            cursorRing.classList.remove('hover');
        });
    });
}

// ─── SCROLL PROGRESS ──────────────────────────────────────────
const progressBar = document.getElementById('scrollProgress');

window.addEventListener('scroll', () => {
    const scrolled = window.scrollY;
    const total = document.documentElement.scrollHeight - window.innerHeight;
    const progress = (scrolled / total) * 100;
    if (progressBar) progressBar.style.width = progress + '%';
});

// ─── HEADER SCROLL STATE ──────────────────────────────────────
const header = document.getElementById('header');

window.addEventListener('scroll', () => {
    if (window.scrollY > 60) {
        header.classList.add('scrolled');
    } else {
        header.classList.remove('scrolled');
    }
}, { passive: true });

// ─── MOBILE NAV ───────────────────────────────────────────────
const toggle = document.getElementById('menuToggle');
const navbar = document.getElementById('navbar');

toggle.addEventListener('click', () => {
    toggle.classList.toggle('active');
    navbar.classList.toggle('active');
    document.body.style.overflow = navbar.classList.contains('active') ? 'hidden' : '';
});

// Close nav when clicking a link
navbar.querySelectorAll('a').forEach(link => {
    link.addEventListener('click', () => {
        toggle.classList.remove('active');
        navbar.classList.remove('active');
        document.body.style.overflow = '';
    });
});

// ─── INTERSECTION OBSERVER — SCROLL REVEAL ────────────────────
const revealObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('visible');
        }
    });
}, {
    threshold: 0.12,
    rootMargin: '0px 0px -40px 0px'
});

document.querySelectorAll('.reveal, .reveal-left, .reveal-right, .reveal-scale').forEach(el => {
    revealObserver.observe(el);
});

// ─── HERO PARALLAX ────────────────────────────────────────────
const heroParallax = document.querySelector('.hero-parallax');
const homeContainer = document.querySelector('.home-container');

if (heroParallax) {
    window.addEventListener('scroll', () => {
        const scrollY = window.scrollY;
        const heroBottom = homeContainer ? homeContainer.offsetHeight : window.innerHeight;

        if (scrollY < heroBottom) {
            heroParallax.style.transform = `translateY(${scrollY * 0.18}px)`;
            heroParallax.style.opacity = 1 - (scrollY / heroBottom) * 0.6;
        }
    }, { passive: true });
}

// ─── BACKGROUND PARALLAX on HERO IMAGE ────────────────────────
if (homeContainer) {
    window.addEventListener('scroll', () => {
        if (window.scrollY < window.innerHeight * 1.5) {
            homeContainer.style.backgroundPositionY = `calc(top + ${window.scrollY * 0.3}px)`;
        }
    }, { passive: true });
}

// ─── MAGNETIC BUTTONS ─────────────────────────────────────────
document.querySelectorAll('.btn').forEach(btn => {
    btn.addEventListener('mousemove', (e) => {
        const rect = btn.getBoundingClientRect();
        const x = e.clientX - rect.left - rect.width / 2;
        const y = e.clientY - rect.top - rect.height / 2;
        btn.style.transform = `translate(${x * 0.12}px, ${y * 0.18}px)`;
    });

    btn.addEventListener('mouseleave', () => {
        btn.style.transform = '';
    });
});

// ─── NUMBER COUNTER ANIMATION ─────────────────────────────────
function animateCounter(el, target, suffix = '') {
    const duration = 1600;
    const start = performance.now();
    const isFloat = String(target).includes('.');

    function update(now) {
        const elapsed = now - start;
        const progress = Math.min(elapsed / duration, 1);
        const eased = 1 - Math.pow(1 - progress, 3);
        const value = isFloat
            ? (eased * parseFloat(target)).toFixed(1)
            : Math.floor(eased * parseInt(target));
        el.textContent = value + suffix;
        if (progress < 1) requestAnimationFrame(update);
    }

    requestAnimationFrame(update);
}

const statsObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            const statNumbers = entry.target.querySelectorAll('.stat-number');
            const targets = ['8', '12', '98'];
            const suffixes = ['+', 'k', '%'];
            statNumbers.forEach((el, i) => {
                animateCounter(el, targets[i], suffixes[i]);
            });
            statsObserver.unobserve(entry.target);
        }
    });
}, { threshold: 0.5 });

const statsSection = document.querySelector('.about-stats');
if (statsSection) statsObserver.observe(statsSection);

// ─── SMOOTH ANCHOR SCROLL ─────────────────────────────────────
document.querySelectorAll('a[href^="#"]').forEach(link => {
    link.addEventListener('click', (e) => {
        const target = document.querySelector(link.getAttribute('href'));
        if (target) {
            e.preventDefault();
            const offset = 80;
            const top = target.getBoundingClientRect().top + window.scrollY - offset;
            window.scrollTo({ top, behavior: 'smooth' });
        }
    });
});
