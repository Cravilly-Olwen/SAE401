async function startScan() {
    const url = document.getElementById('urlInput').value;
    const mode = document.getElementById('scanMode').value;
    
    if(!url) return alert("Veuillez entrer une URL cible.");

    // UI Updates
    document.getElementById('scanBtn').disabled = true;
    document.getElementById('scanBtn').innerHTML = '<i class="fas fa-spinner fa-spin text-lg"></i> INITIALISATION...';
    document.getElementById('scanStatus').classList.remove('hidden');

    // Définition des étapes en fonction du mode choisi
    const simpleSteps = [
        { threshold: 0, text: "Initialisation de l'orchestrateur..." },
        { threshold: 10, text: "Dig : Reconnaissance du domaine..." },
        { threshold: 40, text: "Nmap : Scan rapide des ports..." },
        { threshold: 70, text: "Nikto : Analyse des failles web basiques..." },
        { threshold: 90, text: "Génération du scoring ANSSI..." }
    ];

    const avanceSteps = [
        { threshold: 0, text: "Initialisation de l'orchestrateur..." },
        { threshold: 10, text: "Dig : Reconnaissance du domaine..." },
        { threshold: 25, text: "Nmap : Scan exhaustif des ports..." },
        { threshold: 40, text: "TestSSL : Analyse de la cryptographie TLS..." },
        { threshold: 55, text: "FFUF : Recherche de répertoires cachés..." },
        { threshold: 70, text: "Nikto : Scan approfondi du serveur..." },
        { threshold: 85, text: "OWASP ZAP : Fuzzing et détection active..." },
        { threshold: 95, text: "Génération du scoring ANSSI..." }
    ];

    try {
        await fetch('/api/start-scan', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ url: url, mode: mode })
        });

        let progress = 0;
        const progressBar = document.getElementById('progressBar');
        const progressPercent = document.getElementById('progressPercent');
        const statusLabel = document.getElementById('statusLabel');

        const currentSteps = mode === 'simple' ? simpleSteps : avanceSteps;

        const simInterval = setInterval(() => {
            if (progress < 99) {
                // Le mode avancé est virtuellement un peu plus long à charger
                progress += Math.random() * (mode === 'simple' ? 5 : 3); 
                if(progress > 99) progress = 99;
                
                progressBar.style.width = progress + '%';
                progressPercent.innerText = Math.round(progress) + '%';

                // Mise à jour du texte selon la progression
                const currentStep = currentSteps.slice().reverse().find(s => progress >= s.threshold);
                if (currentStep) {
                    statusLabel.innerText = currentStep.text;
                }
            }
        }, 800);

        // Vérification de la réponse du serveur Flask
        const checkInterval = setInterval(async () => {
            const res = await fetch('/api/check-status');
            const data = await res.json();
            
            if (data.ready) {
                clearInterval(checkInterval);
                clearInterval(simInterval);
                progressBar.style.width = '100%';
                progressPercent.innerText = '100%';
                statusLabel.innerText = "Audit terminé. Redirection...";
                setTimeout(() => { window.location.href = '/dashboard'; }, 800);
            }
        }, 3000); 

    } catch (error) {
        alert("Erreur lors de la communication avec le serveur.");
        document.getElementById('scanBtn').disabled = false;
        document.getElementById('scanBtn').innerHTML = '<i class="fas fa-shield-alt text-lg"></i> LANCER L\'ANALYSE';
    }
}