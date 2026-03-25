const revealElements = document.querySelectorAll('.card, .section-heading, .page-header .container, .hero-visual, .cta-banner');

const revealObserver = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
        if (entry.isIntersecting) {
            entry.target.classList.add('is-visible');
        }
    });
}, { threshold: 0.16 });

revealElements.forEach((element) => {
    element.classList.add('reveal');
    revealObserver.observe(element);
});

const navLinks = document.querySelectorAll('.nav-links a:not(.button)');
const currentPath = window.location.pathname;

navLinks.forEach((link) => {
    const linkPath = new URL(link.href).pathname;
    if (currentPath === linkPath) {
        link.classList.add('active');
    }
});
