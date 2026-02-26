# 🌐 Frontend Flask & Interface Utilisateur

Ce module contient la vitrine de notre plateforme SaaS. Il est développé en Python avec le micro-framework **Flask**.

## 🎯 Rôle
* Fournir le formulaire de recueil d'informations (URL cible, choix du mode simple/avancé).
* Servir de passerelle entre l'utilisateur et l'orchestrateur Shuffle (via Webhooks/API).
* Appliquer le système de scoring (Matrice ANSSI) aux résultats JSON bruts renvoyés par l'orchestrateur.
* Afficher le tableau de bord vulgarisé (Métaphore du "Feu Tricolore").

## ⚙️ Fonctionnalités Avancées Intégrées
* **Génération PDF :** Utilisation de `pdfkit` (ou équivalent) pour transformer le rapport HTML en un document téléchargeable.
* **Serveur Mail (`smtplib`) :** Envoi du rapport final directement sur la boîte mail du client.
* **Job Scheduler (`APScheduler`) :** Automatisation d'une tâche (Cronjob) permettant de relancer l'audit de base tous les jours à 8h00 et d'avertir le client.
