document.addEventListener("DOMContentLoaded", () => {
    gsap.registerPlugin(ScrollTrigger);

    // 1. Initialisation de Lenis (Scroll fluide)
    const lenis = new Lenis();
    lenis.on("scroll", ScrollTrigger.update);
    gsap.ticker.add((time) => { lenis.raf(time * 1000); });
    gsap.ticker.lagSmoothing(0);

    // 2. Animation exacte du paquet de 4 cartes
    const cards = gsap.utils.toArray(".intro-card");
    const totalScrollHeight = window.innerHeight * 2.5; 
    const positions = [14, 38, 62, 86];
    const rotations = [-15, -7.5, 7.5, 15];

    ScrollTrigger.create({
        trigger: ".intro-cards-section",
        start: "top top",
        end: () => `+=${totalScrollHeight}`,
        pin: true,
        pinSpacing: true,
    });

    cards.forEach((card, index) => {
        gsap.to(card, {
            left: `${positions[index]}%`,
            rotation: `${rotations[index]}`,
            ease: "none",
            scrollTrigger: {
                trigger: ".intro-cards-section",
                start: "top top",
                end: () => `+=${window.innerHeight}`,
                scrub: 0.5,
            },
        });
    });

    cards.forEach((card, index) => {
        const frontEl = card.querySelector(".intro-dos");
        const backEl = card.querySelector(".intro-avant");

        const staggerOffset = index * 0.05;
        const startOffset = 1 / 3 + staggerOffset;
        const endOffset = 2 / 3 + staggerOffset;

        ScrollTrigger.create({
            trigger: ".intro-cards-section",
            start: "top top",
            end: () => `+=${totalScrollHeight}`,
            scrub: 1,
            onUpdate: (self) => {
                const progress = self.progress;
                if (progress >= startOffset && progress <= endOffset) {
                    const animationProgress = (progress - startOffset) / (1 / 3);
                    const frontRotation = -180 * animationProgress;
                    const backRotation = 180 - 180 * animationProgress;
                    const cardRotation = rotations[index] * (1 - animationProgress);

                    frontEl.style.transform = `rotateY(${frontRotation}deg)`;
                    backEl.style.transform = `rotateY(${backRotation}deg)`;
                    card.style.transform = `translate(-50%, -50%) rotate(${cardRotation}deg)`;
                }
            },
        });
    });

    // 3. Animation de la Roulette du Casino
    const rData = document.getElementById('roulette-data');
    if (rData) {
        const crit = parseInt(rData.dataset.crit);
        const maj = parseInt(rData.dataset.maj);
        const imp = parseInt(rData.dataset.imp);
        const min = parseInt(rData.dataset.min);
        const total = parseInt(rData.dataset.total);

        const wheel = document.getElementById('roulette-wheel');
        
        let gradientStr = "";
        if (total === 0) {
            gradientStr = "conic-gradient(#10b981 0deg 360deg)";
        } else {
            const pCrit = (crit / total) * 360;
            const pMaj = (maj / total) * 360;
            const pImp = (imp / total) * 360;
            const pMin = (min / total) * 360;

            let angle = 0;
            gradientStr = `conic-gradient(`;
            if (crit > 0) { gradientStr += `#ef4444 ${angle}deg ${angle + pCrit}deg, `; angle += pCrit; }
            if (maj > 0) { gradientStr += `#f97316 ${angle}deg ${angle + pMaj}deg, `; angle += pMaj; }
            if (imp > 0) { gradientStr += `#3b82f6 ${angle}deg ${angle + pImp}deg, `; angle += pImp; }
            if (min > 0) { gradientStr += `#10b981 ${angle}deg ${angle + pMin}deg, `; angle += pMin; }
            gradientStr = gradientStr.slice(0, -2) + `)`; 
        }

        wheel.style.background = gradientStr;

        ScrollTrigger.create({
            trigger: "#roulette-section",
            start: "top 75%", 
            once: true, 
            onEnter: () => {
                gsap.fromTo(wheel, 
                    { rotation: 0 }, 
                    { rotation: 360 * 4 + Math.random() * 360, duration: 4.5, ease: "power3.out" }
                );
                gsap.fromTo("#roulette-ball-container",
                    { rotation: 0 },
                    { rotation: -(360 * 6 + Math.random() * 360), duration: 4.5, ease: "power4.out" }
                );
            }
        });
    }
});

// ==========================================
// 4. FONCTIONS POUR LE FORMULAIRE MAIL
// ==========================================

// Afficher/Cacher la petite fenêtre avec le champ email
function toggleEmailForm() {
    const form = document.getElementById('email-form-container');
    form.classList.toggle('hidden');
}

// Fonction pour envoyer l'ordre d'email à Flask
async function sendEmail() {
    const email = document.getElementById('email-input').value;
    const statusText = document.getElementById('email-status');
    const btn = document.getElementById('send-mail-btn');

    if (!email.includes('@')) {
        statusText.textContent = "Email invalide.";
        statusText.className = "text-xs font-bold mt-2 text-red-400 block";
        return;
    }

    btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i>';
    statusText.textContent = "Envoi en cours...";
    statusText.className = "text-xs font-bold mt-2 text-blue-400 block";

    try {
        const response = await fetch('/api/send-email', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email: email })
        });

        if (response.ok) {
            statusText.textContent = "Rapport envoyé avec succès !";
            statusText.className = "text-xs font-bold mt-2 text-green-400 block";
            btn.innerHTML = '<i class="fas fa-check"></i>';
        } else {
            throw new Error("Erreur serveur");
        }
    } catch (error) {
        statusText.textContent = "Échec de l'envoi.";
        statusText.className = "text-xs font-bold mt-2 text-red-400 block";
        btn.innerHTML = '<i class="fas fa-paper-plane"></i>';
    }
}