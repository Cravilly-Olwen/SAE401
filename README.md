# 🛡️ SAE 401 - Plateforme d'Audit de Cybersécurité (SaaS)

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![Status](https://img.shields.io/badge/status-En%20d%C3%A9veloppement-orange)
![OS](https://img.shields.io/badge/OS-Kali%20Linux-black)

## 📖 Présentation du Projet
[cite_start]Ce dépôt contient le code source et la documentation de notre plateforme SaaS d'audit de sécurité automatisé, réalisée dans le cadre de la SAE 401[cite: 1, 2]. 

Notre objectif est de démocratiser la cybersécurité pour les non-experts. [cite_start]La plateforme orchestre des outils d'audit complexes en arrière-plan et restitue les résultats sous la forme d'un tableau de bord vulgarisé (modèle "Feu Tricolore" 🚦), inspiré des rapports SEO type WooRank[cite: 89, 100, 255].

## ✨ Fonctionnalités Principales
* [cite_start]**Audit à 360° :** Analyse du nom de domaine, de l'hébergement serveur et de la couche applicative web[cite: 246, 247, 248, 249].
* **Double Mode d'Exécution :**
  * [cite_start]*Mode Simple :* Scan rapide de surface (Reconnaissance et failles courantes)[cite: 267].
  * [cite_start]*Mode Avancé :* Analyse profonde et recherche de vulnérabilités critiques (Fuzzing, DAST)[cite: 267].
* [cite_start]**Moteur de Vulgarisation :** Traduction des données techniques brutes en alertes simples (Rouge/Orange/Vert) basées sur la matrice d'évaluation des risques de l'ANSSI[cite: 290, 291].
* **Rapports Automatisés :** Génération du rapport au format PDF et envoi direct par Email.
* **Surveillance Continue :** Possibilité de s'abonner à un audit quotidien automatisé (Cron à 8h00) avec alerte par mail en cas de nouvelle faille détectée.
* [cite_start]**Éthique & Légalité :** Mode "White Hat" strict avec temporisation des requêtes (anti-DDoS involontaire) pour garantir la disponibilité des services audités[cite: 259, 260].

## 🛠️ Stack Technique & Outils Exclusifs
* **Frontend / Interface :** Python 3 (Flask), HTML/CSS, Jinja2.
* **Orchestrateur SOAR :** Shuffle (via Docker) gérant la parallélisation et l'asynchronisme.
* **Les 6 Outils d'Audit Intégrés :**
  1. [cite_start]`dig` : Reconnaissance DNS et zone[cite: 279].
  2. [cite_start]`Nmap` : Scan de ports et détection de services/OS[cite: 289].
  3. [cite_start]`testssl.sh` : Analyse de la robustesse cryptographique (HTTPS/TLS)[cite: 286].
  4. `FFUF` : Fuzzing et découverte de contenus/fichiers cachés.
  5. [cite_start]`Nikto` : Scan des configurations serveur et des fichiers par défaut dangereux[cite: 281].
  6. `OWASP ZAP` : Scanner applicatif dynamique (DAST) pour les failles complexes (SQLi, XSS).

## 📁 Architecture du Dépôt

* 🌐 [`/frontend_flask`](./frontend_flask) : Interface web, routing, génération PDF et configuration email.
* ⚙️ [`/backend_orchestrator`](./backend_orchestrator) : Workflows Shuffle, scripts de parsing JSON.
* 🎯 [`/dummy_site`](./dummy_site) : Environnement de test local vulnérable (laboratoire Grey Hat).
* [cite_start]📚 [`/docs`](./docs) : Cahier des charges, architecture détaillée, matrice Excel ANSSI[cite: 290, 291].

## 🚀 Installation & Lancement (Environnement de Dév)
*(Les instructions de lancement Docker et Flask seront documentées ici lors de la phase de déploiement).*
