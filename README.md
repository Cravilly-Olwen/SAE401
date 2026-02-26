# 🛡️ SAE 401 - Plateforme d'Audit de Cybersécurité (SaaS)

## 📖 Présentation du Projet
Ce dépôt contient le code source et la documentation de notre plateforme SaaS d'audit de sécurité automatisé, réalisée dans le cadre de la SAE 401. 

Notre objectif est de démocratiser la cybersécurité pour les non-experts. La plateforme orchestre des outils d'audit complexes en arrière-plan et restitue les résultats sous la forme d'un tableau de bord vulgarisé reprenant le modèle d'un **"Contrôle Technique Automobile" 🚗**, inspiré des rapports SEO type WooRank.

## ✨ Fonctionnalités Principales
* **Audit à 360° :** Analyse du nom de domaine, de l'hébergement serveur et de la couche applicative web.
* **Double Mode d'Exécution :**
  * **Mode Simple :** Scan rapide de surface (Reconnaissance et failles courantes).
  * **Mode Avancé :** Analyse profonde et recherche de vulnérabilités critiques (Fuzzing, DAST).
* **Moteur de Vulgarisation (Le Contrôle Technique) :** Traduction des données techniques brutes en alertes compréhensibles basées sur la matrice de l'ANSSI :
  * *Vignette globale* : Score de sécurité (Favorable / Contre-visite / Immobilisation).
  * *Freins Coupés (Critique)* : Danger imminent (ex: Faille SQLi, vol de données).
  * *Pneus Lisses (Majeur)* : Risque de sortie de route en cas d'attaque (ex: Certificat SSL obsolète).
  * *Anomalie Carrosserie (Mineur)* : Défaut d'entretien (ex: Headers manquants).
  * *Changement d'ampoule (Quick Wins)* : Corrections rapides de 5 minutes.
* **Rapports Automatisés :** Génération du rapport au format PDF et envoi direct par Email.
* **Surveillance Continue :** Possibilité de s'abonner à un audit quotidien automatisé (Cron à 8h00) avec alerte par mail en cas de nouvelle faille détectée.
* **Éthique & Légalité :** Mode "White Hat" strict avec temporisation des requêtes (anti-DDoS involontaire) pour garantir la disponibilité des services audités.

## 🛠️ Stack Technique & Outils Exclusifs
* **Frontend / Interface :** Python 3 (Flask), HTML/CSS, Jinja2.
* **Orchestrateur SOAR :** Shuffle (via Docker) gérant la parallélisation et l'asynchronisme.
* **Les 6 Outils d'Audit Intégrés :**
  1. `dig` : Reconnaissance DNS et zone.
  2. `Nmap` : Scan de ports et détection de services/OS.
  3. `testssl.sh` : Analyse de la robustesse cryptographique (HTTPS/TLS).
  4. `FFUF` : Fuzzing et découverte de contenus/fichiers cachés.
  5. `Nikto` : Scan des configurations serveur et des fichiers par défaut dangereux.
  6. `OWASP ZAP` : Scanner applicatif dynamique (DAST) pour les failles complexes (SQLi, XSS).

## 📁 Architecture du Dépôt
* 🌐 **`/frontend_flask`** : Interface web, routing, génération PDF et configuration email.
* ⚙️ **`/backend_orchestrator`** : Workflows Shuffle, scripts de parsing JSON.
* 🎯 **`/dummy_site`** : Environnement de test local vulnérable (laboratoire Grey Hat).
* 📚 **`/docs`** : Cahier des charges, architecture détaillée, matrice Excel ANSSI.

## 🚀 Installation & Lancement (Environnement de Dév)
*(Les instructions de lancement Docker et Flask seront documentées ici lors de la phase de déploiement).*
