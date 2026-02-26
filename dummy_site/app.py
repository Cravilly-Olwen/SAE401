from flask import Flask, request, make_response, render_template_string
import ssl

app = Flask(__name__)

# 🎨 DESIGN HTML COMPLET (Style Universitaire)
TEMPLATE = """
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>Université Côte d'Azur - Espace Étudiant</title>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 0; background-color: #f4f7f6; }
        header { background-color: #004b87; color: white; padding: 20px; display: flex; justify-content: space-between; align-items: center; }
        .logo { font-size: 24px; font-weight: bold; }
        nav a { color: white; text-decoration: none; margin: 0 15px; font-weight: 500; }
        .hero { background: url('https://images.unsplash.com/photo-1541339907198-e08756dedf3f?ixlib=rb-1.2.1&auto=format&fit=crop&w=1350&q=80') center/cover; height: 300px; display: flex; align-items: center; justify-content: center; color: white; text-shadow: 2px 2px 4px #000; }
        .container { max-width: 1000px; margin: 40px auto; padding: 20px; background: white; box-shadow: 0 4px 8px rgba(0,0,0,0.1); border-radius: 8px; }
        .search-box { padding: 20px; background: #e9ecef; border-radius: 8px; margin-bottom: 20px; }
        input[type="text"] { width: 70%; padding: 10px; border: 1px solid #ccc; border-radius: 4px; }
        button { padding: 10px 20px; background-color: #004b87; color: white; border: none; border-radius: 4px; cursor: pointer; }
        footer { background-color: #333; color: white; text-align: center; padding: 10px; position: fixed; bottom: 0; width: 100%; }
        .alert { color: #856404; background-color: #fff3cd; padding: 10px; border: 1px solid #ffeeba; border-radius: 4px; margin-top: 20px; }
    </style>
</head>
<body>
    <header>
        <div class="logo">🎓 Université - Espace Numérique</div>
        <nav>
            <a href="/">Accueil</a>
            <a href="#">Formations</a>
            <a href="#">Recherche</a>
            <a href="#">Intranet (Personnel)</a>
        </nav>
    </header>
    
    <div class="hero">
        <h1>Bienvenue sur le portail des étudiants</h1>
    </div>

    <div class="container">
        <h2>Recherche de formations & Annuaire</h2>
        <div class="search-box">
            <form method="GET" action="/">
                <input type="text" name="q" placeholder="Rechercher un cours, un étudiant..." value="{{ query }}">
                <button type="submit">Rechercher</button>
            </form>
        </div>
        
        {% if query %}
        <div class="alert">
            <p>Résultats de la recherche pour : <strong>{{ query | safe }}</strong></p>
            <p><i>Aucun résultat trouvé pour cette requête dans l'annuaire de l'Université.</i></p>
        </div>
        {% else %}
        <p>Veuillez utiliser la barre de recherche ci-dessus pour consulter le catalogue 2025-2026.</p>
        {% endif %}
    </div>

    <footer>
        &copy; 2026 Espace Universitaire - Tous droits réservés. (Site à but pédagogique - SAE 401)
    </footer>
</body>
</html>
"""

@app.route('/')
def home():
    query = request.args.get('q', '')
    html = render_template_string(TEMPLATE, query=query)
    
    # 🎯 FAILLE NIKTO : On forge une réponse avec de mauvais headers pour alerter Nikto
    resp = make_response(html)
    resp.headers['Server'] = 'Apache/2.2.14 (Ubuntu)' # Fausse version obsolète
    resp.headers['X-Powered-By'] = 'PHP/5.3.3' # Version vulnérable exposée
    # Absence volontaire de X-Frame-Options et X-Content-Type-Options
    return resp

# 🎯 FAILLE FFUF / DIRB : Le robots.txt qui indique les dossiers cachés
@app.route('/robots.txt')
def robots():
    resp = make_response("User-agent: *\nDisallow: /admin_portal\nDisallow: /config.bak\nDisallow: /backup.zip")
    resp.headers['Content-Type'] = 'text/plain'
    return resp

# 🎯 FAILLE FFUF : Le fichier sensible exposé
@app.route('/config.bak')
def config_bak():
    resp = make_response("DB_HOST=127.0.0.1\nDB_USER=admin_univ\nDB_PASS=P@ssw0rd_Univ_2026!")
    resp.headers['Content-Type'] = 'text/plain'
    return resp

if __name__ == '__main__':
    # 🎯 FAILLE TESTSSL : Certificat auto-signé sur le port 443
    app.run(host='0.0.0.0', port=443, ssl_context='adhoc')
