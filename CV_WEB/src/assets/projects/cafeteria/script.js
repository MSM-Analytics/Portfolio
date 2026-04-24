const toggle = document.querySelector('.menu-toggle');
const navbar = document.querySelector('.navbar');

toggle.addEventListener('click', () => {
    toggle.classList.toggle('active');
    navbar.classList.toggle('active');
});