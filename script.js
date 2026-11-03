document.addEventListener('DOMContentLoaded', () => {
    
    // --- 1. ANIMACIONES SCROLL (Reveal) ---
    const reveals = document.querySelectorAll('.reveal');

    const observerOptions = {
        threshold: 0.15 
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('active');
            }
        });
    }, observerOptions);

    reveals.forEach(reveal => observer.observe(reveal));

    // --- 2. EFECTO BORDE EN TARJETAS ---
    const cards = document.querySelectorAll('.card');
    cards.forEach(card => {
        card.addEventListener('mousemove', (e) => {
            const rect = card.getBoundingClientRect();
            card.style.border = '1px solid rgba(255, 255, 255, 0.08)';
        });

        card.addEventListener('mouseleave', () => {
            card.style.border = 'none';
        });
    });

    console.log("Sistema RC Team listo.");
});