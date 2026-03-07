from flask import Flask, render_template, request, jsonify, make_response
import requests
import urllib3
import urllib.parse
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from urllib.parse import urlparse
from weasyprint import HTML

# Désactive les avertissements de sécurité pour le HTTPS local
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# --- 1. INITIALISATION DE L'APPLICATION (La ligne qui manquait !) ---
app = Flask(__name__)

# Stockage temporaire en mémoire du rapport
latest_report = None

# --- 2. ROUTE DE LA PAGE D'ACCUEIL (qui manquait aussi) ---
@app.route('/')
def home():
    return render_template('index.html')

# --- 3. ROUTE DE DECLENCHEMENT DE L'AUDIT ---
@app.route('/api/start-scan', methods=['POST'])
def start_scan():
    global latest_report # <-- AJOUTER CECI
    latest_report = None # <-- ON VIDE L'ANCIEN RAPPORT AVANT DE LANCER LE NOUVEAU !

    data = request.json
    raw_url = data.get('url', '').strip()
    
    # 1. Ajout de https:// par défaut si l'utilisateur l'oublie
    if not raw_url.startswith(('http://', 'https://')):
        raw_url = 'https://' + raw_url
        
    # 2. Parsing intelligent de l'URL
    parsed_url = urlparse(raw_url)
    
    # VARIABLE 1 : Le domaine pur (pour Dig et Nmap)
    clean_target = parsed_url.hostname  
    
    # VARIABLE 2 : L'URL Web complète (pour Nikto, ZAP, FFUF)
    # On recompose l'URL avec le port SEULEMENT s'il a été tapé par l'utilisateur
    port_section = f":{parsed_url.port}" if parsed_url.port else ""
    full_url = f"{parsed_url.scheme}://{clean_target}{port_section}"

    scan_mode = data.get('mode')
    
    # L'URL de ton Webhook Shuffle
    shuffle_webhook_url = "https://127.0.0.1:3443/api/v1/hooks/webhook_b8ae0f49-ef46-487e-bbd8-b6674650e17b"
    
    try:
        # On envoie les deux variables distinctes à Shuffle !
        requests.post(shuffle_webhook_url, json={
            "clean_target": clean_target,
            "full_url": full_url,
            "mode": scan_mode
        }, verify=False, timeout=5)
        print(f"Ordre envoyé -> Réseau: {clean_target} | Web: {full_url} | Mode: {scan_mode}")
        
    except Exception as e:
        print(f"Erreur de communication: {e}")

    return jsonify({"status": "started"}), 200

# --- 4. ROUTE DE RECEPTION DU RAPPORT ---
@app.route('/api/report', methods=['POST'])
def receive_report():
    global latest_report
    latest_report = request.json 
    print("Nouveau rapport reçu de l'orchestrateur !")
    return jsonify({"status": "success"}), 200

# --- 5. ROUTE DU DASHBOARD ---
@app.route('/dashboard')
def dashboard():
    global latest_report
    if not latest_report:
         return "L'audit est en cours ou n'a pas été lancé...", 404
    return render_template('dashboard.html', report=latest_report)

# --- 6. ROUTE DE VERIFICATION DU STATUT ---
@app.route('/api/check-status', methods=['GET'])
def check_status():
    global latest_report
    if latest_report is not None:
        return jsonify({"ready": True})
    return jsonify({"ready": False})

# --- 7. ROUTE : GÉNÉRATION DU PDF ---
@app.route('/api/download-pdf', methods=['GET'])
def download_pdf():
    global latest_report
    if not latest_report:
        return "L'audit n'est pas terminé ou aucun rapport n'est disponible.", 404

    crit = len(latest_report['scoring_anssi'].get('Critique', []))
    maj = len(latest_report['scoring_anssi'].get('Majeur', []))
    imp = len(latest_report['scoring_anssi'].get('Important', []))
    min_ = len(latest_report['scoring_anssi'].get('Mineur', []))
    
    outils_stats = {}
    for gravite, failles in latest_report['scoring_anssi'].items():
        for f in failles:
            outil = f.get('outil', 'Inconnu')
            outils_stats[outil] = outils_stats.get(outil, 0) + 1

    # --- LE CALCUL DU SCORE EST ICI ---
    score = 100 - (crit * 25) - (maj * 15) - (imp * 5) - (min_ * 1)
    score = max(0, score)

    if score >= 90:
        grade, color, message = 'A', '#10b981', 'EXCELLENT (Situation saine, très bon niveau)'
    elif score >= 70:
        grade, color, message = 'B', '#3b82f6', 'BON (Quelques ajustements recommandés)'
    elif score >= 50:
        grade, color, message = 'C', '#eab308', 'MOYEN (Faiblesses importantes à corriger)'
    elif score >= 20:
        grade, color, message = 'D', '#f97316', 'DANGEREUX (Intervention rapide nécessaire)'
    else:
        grade, color, message = 'F', '#ef4444', 'CRITIQUE (Urgence absolue - Danger immédiat)'

    evaluation = {'score': score, 'grade': grade, 'color': color, 'message': message}
    # ----------------------------------

    pie_chart_config = f"{{type: 'outlabeledPie', data: {{labels: ['Banqueroute', 'Pari Risqué', 'Coup de Bluff', 'Petite Fuite'], datasets: [{{data: [{crit}, {maj}, {imp}, {min_}], backgroundColor: ['#ef4444', '#f97316', '#3b82f6', '#10b981']}}]}}, options: {{plugins: {{legend: {{position: 'bottom'}}}}}}}}"
    pie_chart_url = "https://quickchart.io/chart?c=" + urllib.parse.quote(pie_chart_config.strip())

    labels_outils = list(outils_stats.keys())
    data_outils = list(outils_stats.values())
    bar_chart_config = f"{{type: 'bar', data: {{labels: {labels_outils}, datasets: [{{label: 'Vulnérabilités', data: {data_outils}, backgroundColor: '#1e3a8a'}}]}}}}"
    bar_chart_url = "https://quickchart.io/chart?c=" + urllib.parse.quote(bar_chart_config.strip())

    # --- ON PASSE EVALUATION AU TEMPLATE ICI ---
    rendered_html = render_template('report_pdf.html', report=latest_report, pie_chart_url=pie_chart_url, bar_chart_url=bar_chart_url, evaluation=evaluation)
    
    pdf = HTML(string=rendered_html).write_pdf()

    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'attachment; filename=Rapport_CyberSentinel_Complet.pdf'
    
    return response

# --- 8. ROUTE : ENVOI DU PDF PAR MAIL ---
@app.route('/api/send-email', methods=['POST'])
def send_email():
    global latest_report
    if not latest_report:
        return jsonify({"error": "Aucun rapport disponible."}), 400

    data = request.json
    recipient_email = data.get('email')
    
    if not recipient_email:
        return jsonify({"error": "Adresse email manquante."}), 400

    try:
        crit = len(latest_report['scoring_anssi'].get('Critique', []))
        maj = len(latest_report['scoring_anssi'].get('Majeur', []))
        imp = len(latest_report['scoring_anssi'].get('Important', []))
        min_ = len(latest_report['scoring_anssi'].get('Mineur', []))
        
        outils_stats = {}
        for gravite, failles in latest_report['scoring_anssi'].items():
            for f in failles:
                outil = f.get('outil', 'Inconnu')
                outils_stats[outil] = outils_stats.get(outil, 0) + 1

        # --- LE CALCUL DU SCORE EST AUSSI RECOPIÉ ICI ! ---
        score = 100 - (crit * 25) - (maj * 15) - (imp * 5) - (min_ * 1)
        score = max(0, score)

        if score >= 90:
            grade, color, message = 'A', '#10b981', 'EXCELLENT (Situation saine, très bon niveau)'
        elif score >= 70:
            grade, color, message = 'B', '#3b82f6', 'BON (Quelques ajustements recommandés)'
        elif score >= 50:
            grade, color, message = 'C', '#eab308', 'MOYEN (Faiblesses importantes à corriger)'
        elif score >= 20:
            grade, color, message = 'D', '#f97316', 'DANGEREUX (Intervention rapide nécessaire)'
        else:
            grade, color, message = 'F', '#ef4444', 'CRITIQUE (Urgence absolue - Danger immédiat)'

        evaluation = {'score': score, 'grade': grade, 'color': color, 'message': message}
        # --------------------------------------------------

        pie_chart_config = f"{{type: 'outlabeledPie', data: {{labels: ['Banqueroute', 'Pari Risqué', 'Coup de Bluff', 'Petite Fuite'], datasets: [{{data: [{crit}, {maj}, {imp}, {min_}], backgroundColor: ['#ef4444', '#f97316', '#3b82f6', '#10b981']}}]}}, options: {{plugins: {{legend: {{position: 'bottom'}}}}}}}}"
        pie_chart_url = "https://quickchart.io/chart?c=" + urllib.parse.quote(pie_chart_config.strip())

        labels_outils = list(outils_stats.keys())
        data_outils = list(outils_stats.values())
        bar_chart_config = f"{{type: 'bar', data: {{labels: {labels_outils}, datasets: [{{label: 'Vulnérabilités', data: {data_outils}, backgroundColor: '#1e3a8a'}}]}}}}"
        bar_chart_url = "https://quickchart.io/chart?c=" + urllib.parse.quote(bar_chart_config.strip())

        # --- ON PASSE EVALUATION AU TEMPLATE ICI AUSSI ---
        rendered_html = render_template('report_pdf.html', report=latest_report, pie_chart_url=pie_chart_url, bar_chart_url=bar_chart_url, evaluation=evaluation)
        
        pdf_bytes = HTML(string=rendered_html).write_pdf()

        # Reste de l'envoi de mail...
        SENDER_EMAIL = "girardjeremy8@gmail.com" 
        SENDER_PASSWORD = "krmt jpos czyo vqip" 
        
        msg = MIMEMultipart()
        msg['From'] = f"CyberSentinel <{SENDER_EMAIL}>"
        msg['To'] = recipient_email
        msg['Subject'] = "Votre Tirage de Sécurité - Rapport CyberSentinel"

        body = """Bonjour,

Veuillez trouver ci-joint le résultat de votre audit de sécurité sous forme de rapport PDF détaillé.

L'équipe CyberSentinel vous souhaite une excellente journée !"""
        msg.attach(MIMEText(body, 'plain', 'utf-8'))

        pdf_attachment = MIMEApplication(pdf_bytes, _subtype="pdf")
        pdf_attachment.add_header('Content-Disposition', 'attachment', filename="Rapport_CyberSentinel_Complet.pdf")
        msg.attach(pdf_attachment)

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.send_message(msg)
        server.quit()

        return jsonify({"status": "success"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# --- LANCEMENT DU SERVEUR ---
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)