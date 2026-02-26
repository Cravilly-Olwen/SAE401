# ⚙️ Backend Orchestrateur (Shuffle & Scripts)

Ce module est le "moteur" de notre plateforme d'audit. Il centralise les flux de travail automatisés.

## 🎯 Rôle
* Lancer en parallèle les 6 outils de cybersécurité de la plateforme.
* Assurer la conformité **White Hat** : Les workflows intègrent des nœuds de "Delay" (temporisation) entre les exécutions de `FFUF` et `ZAP` pour prévenir tout risque de déni de service (DDoS) involontaire sur la cible.
* Parser les sorties brutes (CLI) des outils pour les normaliser en un format **JSON** exploitable par Flask.

## 🧰 Outils Pilotés
* **Phase Reconnaissance :** `dig`, `Nmap`, `testssl.sh`
* **Phase Vulnérabilité :** `Nikto`, `FFUF`, `OWASP ZAP`
