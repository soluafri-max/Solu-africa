const revealElements = document.querySelectorAll('.card, .section-heading, .page-header .container');

const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
        if (entry.isIntersecting) {
            entry.target.classList.add('is-visible');
        }
    });
}, { threshold: 0.15 });

revealElements.forEach((element) => {
    element.classList.add('reveal');
    observer.observe(element);
});
