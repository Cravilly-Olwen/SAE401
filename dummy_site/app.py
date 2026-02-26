from flask import Flask, request
import ssl

app = Flask(__name__)

# 🎯 FAILLE 1 : Faille XSS (Cross-Site Scripting) pour OWASP ZAP
@app.route('/')
def home():
    # L'entrée utilisateur n'est pas sécurisée (pas d'échappement)
    query = request.args.get('search', '')
    
    html = f"""
    <!DOCTYPE html>
    <html>
    <head><title>Banque Sécurisée - Intranet</title></head>
    <body style="font-family: Arial, sans-serif; margin: 40px;">
        <h1>Intranet de la Banque</h1>
        <p>Rechercher un dossier client :</p>
        <form method="GET" action="/">
            <input type="text" name="search" placeholder="Nom du client..." value="{query}">
            <input type="submit" value="Rechercher">
        </form>
        <hr>
        <p>Résultats de recherche pour : <strong>{query}</strong></p> 
    </body>
    </html>
    """
    return html

# 🎯 FAILLE 2 : Divulgation d'informations et dossier caché pour FFUF / Dirb
@app.route('/backup')
def backup():
    return "Fichier de configuration de la base de données : DB_USER=admin | DB_PASS=SuperSecretPassword2026!"

if __name__ == '__main__':
    # 🎯 FAILLE 3 : Lancement en HTTPS avec un certificat auto-signé ("adhoc") pour faire réagir testssl.sh
    app.run(host='0.0.0.0', port=443, ssl_context='adhoc')
