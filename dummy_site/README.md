# 🎯 Dummy Site (Environnement de Test Contrôlé)

Afin de respecter le cadre légal des tests d'intrusion (loi Godfrain) et l'exigence de bienveillance ("White Hat") de ce projet, ce dossier contient notre propre site cible intentionnellement vulnérable.

## ⚠️ Avertissement de Sécurité
**CE SITE NE DOIT JAMAIS ÊTRE DÉPLOYÉ SUR UN RÉSEAU PUBLIC.** Il est conçu pour tourner exclusivement en local (`127.0.0.1`) ou dans un conteneur Docker isolé.

## 🎯 Objectifs
1. **Validation QA :** Vérifier que nos 6 outils détectent correctement les failles (SQLi, XSS, headers manquants, répertoires cachés).
2. **Démonstration "Grey Hat" :** Lors de la soutenance, cet environnement nous permettra de passer de la simple détection (théorie) à l'exploitation contrôlée (pratique) d'une faille critique (ex: afficher une alerte XSS en direct) pour prouver l'efficacité de notre plateforme.
