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
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
import hashlib
import json
import os
import threading

# Désactive les avertissements de sécurité pour le HTTPS local
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# --- 1. INITIALISATION DE L'APPLICATION ---
app = Flask(__name__)

# Stockage temporaire en mémoire du rapport + verrou pour les audits planifiés
latest_report = None
report_event  = threading.Event()
audit_lock    = threading.Lock()   # Evite deux audits automatiques simultanés

# --- CONFIGURATION GLOBALE ---
SUBSCRIBERS_FILE  = os.path.join(os.path.dirname(__file__), 'subscribers.json')
SHUFFLE_WEBHOOK_URL = "https://127.0.0.1:3443/api/v1/hooks/webhook_b8ae0f49-ef46-487e-bbd8-b6674650e17b"
SENDER_EMAIL      = "girardjeremy8@gmail.com"
SENDER_PASSWORD   = "krmt jpos czyo vqip"

# Correspondance fréquence → paramètre cron APScheduler
FREQUENCY_CRON = {
    'daily':     {},
    'monday':    {'day_of_week': 'mon'},
    'tuesday':   {'day_of_week': 'tue'},
    'wednesday': {'day_of_week': 'wed'},
    'thursday':  {'day_of_week': 'thu'},
    'friday':    {'day_of_week': 'fri'},
}

FREQUENCY_LABEL = {
    'daily':     'tous les jours',
    'monday':    'chaque lundi',
    'tuesday':   'chaque mardi',
    'wednesday': 'chaque mercredi',
    'thursday':  'chaque jeudi',
    'friday':    'chaque vendredi',
}


# =========================================================
# --- FONCTIONS UTILITAIRES ---
# =========================================================

def _job_id(email, target):
    """Identifiant unique et stable pour un job APScheduler."""
    return "audit_" + hashlib.md5(f"{email}|{target}".encode()).hexdigest()[:12]


def load_subscribers():
    if os.path.exists(SUBSCRIBERS_FILE):
        with open(SUBSCRIBERS_FILE, 'r') as f:
            return json.load(f)
    return []


def save_subscribers(subscribers):
    with open(SUBSCRIBERS_FILE, 'w') as f:
        json.dump(subscribers, f, indent=2)


def compute_evaluation(report):
    """Calcule le score de vitalité et la note (A→F) à partir d'un rapport."""
    crit  = len(report['scoring_anssi'].get('Critique', []))
    maj   = len(report['scoring_anssi'].get('Majeur', []))
    imp   = len(report['scoring_anssi'].get('Important', []))
    min_  = len(report['scoring_anssi'].get('Mineur', []))

    score = max(0, 100 - (crit * 25) - (maj * 15) - (imp * 5) - (min_ * 1))

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

    return {
        'score': score, 'grade': grade, 'color': color, 'message': message,
        'crit': crit, 'maj': maj, 'imp': imp, 'min_': min_
    }


def generate_pdf_bytes(report, generation_date):
    """Génère le PDF en mémoire et retourne les bytes."""
    evaluation = compute_evaluation(report)
    crit, maj, imp, min_ = evaluation['crit'], evaluation['maj'], evaluation['imp'], evaluation['min_']

    pie_cfg = (
        f"{{type:'outlabeledPie',data:{{labels:['Banqueroute','Pari Risqué','Coup de Bluff','Petite Fuite'],"
        f"datasets:[{{data:[{crit},{maj},{imp},{min_}],"
        f"backgroundColor:['#ef4444','#f97316','#3b82f6','#10b981'],borderWidth:0}}]}},"
        f"options:{{plugins:{{legend:{{position:'bottom'}}}}}}}}"
    )
    pie_chart_url = "https://quickchart.io/chart?c=" + urllib.parse.quote(pie_cfg)

    rendered_html = render_template(
        'report_pdf.html',
        report=report,
        pie_chart_url=pie_chart_url,
        evaluation=evaluation,
        generation_date=generation_date
    )
    return HTML(string=rendered_html).write_pdf()


def send_email_with_pdf(recipient_email, pdf_bytes, subject, body_text, filename="Rapport_CyberSentinel.pdf"):
    """Envoie un email avec le PDF en pièce jointe."""
    msg = MIMEMultipart()
    msg['From']    = f"CyberSentinel <{SENDER_EMAIL}>"
    msg['To']      = recipient_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body_text, 'plain', 'utf-8'))

    pdf_attachment = MIMEApplication(pdf_bytes, _subtype="pdf")
    pdf_attachment.add_header('Content-Disposition', 'attachment', filename=filename)
    msg.attach(pdf_attachment)

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(SENDER_EMAIL, SENDER_PASSWORD)
    server.send_message(msg)
    server.quit()


# =========================================================
# --- JOB INDIVIDUEL PAR ABONNÉ ---
# =========================================================

def run_audit_for_subscriber(email, target):
    """Déclenche un audit silencieux et envoie le rapport de vitalité par email."""
    global latest_report

    with audit_lock:  # Un seul audit automatique à la fois
        print(f"[CRON] Démarrage de l'audit pour '{target}' → '{email}'")

        latest_report = None
        report_event.clear()

        raw_url = target if target.startswith(('http://', 'https://')) else 'https://' + target
        parsed       = urlparse(raw_url)
        clean_target = parsed.hostname
        port_section = f":{parsed.port}" if parsed.port else ""
        full_url     = f"{parsed.scheme}://{clean_target}{port_section}"

        try:
            requests.post(SHUFFLE_WEBHOOK_URL, json={
                "clean_target": clean_target,
                "full_url":     full_url,
                "mode":         "simple"
            }, verify=False, timeout=5)
        except Exception as e:
            print(f"[CRON] Impossible de déclencher le scan pour '{target}': {e}")
            return

        # Attend le rapport de Shuffle (timeout : 10 minutes)
        if not report_event.wait(timeout=600):
            print(f"[CRON] Timeout — aucun rapport reçu pour '{target}'.")
            return

        report          = latest_report
        generation_date = datetime.now().strftime("%d/%m/%Y à %H:%M")
        evaluation      = compute_evaluation(report)
        score, grade    = evaluation['score'], evaluation['grade']

        if evaluation['crit'] > 0:
            alerte = f"⚠️  ALERTE : {evaluation['crit']} faille(s) CRITIQUE(s) détectée(s) ! Intervention urgente requise."
        elif evaluation['maj'] > 0:
            alerte = f"⚠️  {evaluation['maj']} faille(s) MAJEURE(s) détectée(s). Vérification recommandée."
        else:
            alerte = "✅  Aucune nouvelle infection critique détectée."

        body = f"""Bonjour,

Voici votre rapport de surveillance automatique CyberSentinel.

Cible auditée : {target}
Date          : {generation_date}

🛡️  Indice de Vitalité : {score}/100  (Note : {grade})
{alerte}

Le rapport complet est disponible en pièce jointe.

--
L'équipe CyberSentinel
"""
        subject = f"[CyberSentinel] Vitalité du {generation_date} — {score}/100 (Note {grade})"

        try:
            with app.app_context():
                pdf_bytes = generate_pdf_bytes(report, generation_date)
            send_email_with_pdf(email, pdf_bytes, subject, body)
            print(f"[CRON] ✅ Email envoyé à '{email}' (score: {score}/100, note: {grade})")
        except Exception as e:
            print(f"[CRON] ❌ Erreur lors de l'envoi à '{email}': {e}")


def schedule_subscriber_job(sub):
    """Crée ou remplace le job APScheduler pour un abonné."""
    email     = sub['email']
    target    = sub['target']
    frequency = sub.get('frequency', 'daily')
    hour      = sub.get('hour', 8)

    cron_extra = FREQUENCY_CRON.get(frequency, {})

    scheduler.add_job(
        run_audit_for_subscriber,
        'cron',
        hour=hour,
        minute=0,
        kwargs={'email': email, 'target': target},
        id=_job_id(email, target),
        replace_existing=True,
        **cron_extra
    )
    freq_label = FREQUENCY_LABEL.get(frequency, frequency)
    print(f"[SCHEDULER] Job planifié : '{email}' → '{target}' | {freq_label} à {hour:02d}:00")


# =========================================================
# --- ROUTES DE L'APPLICATION ---
# =========================================================

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/api/start-scan', methods=['POST'])
def start_scan():
    global latest_report
    latest_report = None
    report_event.clear()

    data    = request.json
    raw_url = data.get('url', '').strip()

    if not raw_url.startswith(('http://', 'https://')):
        raw_url = 'https://' + raw_url

    parsed       = urlparse(raw_url)
    clean_target = parsed.hostname
    port_section = f":{parsed.port}" if parsed.port else ""
    full_url     = f"{parsed.scheme}://{clean_target}{port_section}"
    scan_mode    = data.get('mode')

    try:
        requests.post(SHUFFLE_WEBHOOK_URL, json={
            "clean_target": clean_target,
            "full_url":     full_url,
            "mode":         scan_mode
        }, verify=False, timeout=5)
        print(f"Ordre envoyé -> Réseau: {clean_target} | Web: {full_url} | Mode: {scan_mode}")
    except Exception as e:
        print(f"Erreur de communication: {e}")

    return jsonify({"status": "started"}), 200


@app.route('/api/report', methods=['POST'])
def receive_report():
    global latest_report
    latest_report = request.json
    report_event.set()   # Débloque run_audit_for_subscriber si en attente
    print("Nouveau rapport reçu de l'orchestrateur !")
    return jsonify({"status": "success"}), 200


@app.route('/dashboard')
def dashboard():
    global latest_report
    if not latest_report:
        return "L'audit est en cours ou n'a pas été lancé...", 404
    return render_template('dashboard.html', report=latest_report)


@app.route('/api/check-status', methods=['GET'])
def check_status():
    global latest_report
    return jsonify({"ready": latest_report is not None})


@app.route('/api/download-pdf', methods=['GET'])
def download_pdf():
    global latest_report
    if not latest_report:
        return "L'audit n'est pas terminé ou aucun rapport n'est disponible.", 404

    generation_date = datetime.now().strftime("%d/%m/%Y à %H:%M")
    pdf = generate_pdf_bytes(latest_report, generation_date)

    response = make_response(pdf)
    response.headers['Content-Type']        = 'application/pdf'
    response.headers['Content-Disposition'] = 'attachment; filename=Rapport_CyberSentinel_Complet.pdf'
    return response


@app.route('/api/send-email', methods=['POST'])
def send_email():
    global latest_report
    if not latest_report:
        return jsonify({"error": "Aucun rapport disponible."}), 400

    data            = request.json
    recipient_email = data.get('email')
    if not recipient_email:
        return jsonify({"error": "Adresse email manquante."}), 400

    try:
        generation_date = datetime.now().strftime("%d/%m/%Y à %H:%M")
        pdf_bytes = generate_pdf_bytes(latest_report, generation_date)

        body = """Bonjour,

Veuillez trouver ci-joint le résultat de votre audit de sécurité sous forme de rapport PDF détaillé.

L'équipe CyberSentinel vous souhaite une excellente journée !"""

        send_email_with_pdf(
            recipient_email, pdf_bytes,
            subject="Votre Tirage de Sécurité - Rapport CyberSentinel",
            body_text=body,
            filename="Rapport_CyberSentinel_Complet.pdf"
        )
        return jsonify({"status": "success"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/subscribe', methods=['POST'])
def subscribe():
    data      = request.json
    email     = data.get('email', '').strip()
    target    = data.get('target', '').strip()
    frequency = data.get('frequency', 'daily')
    hour      = int(data.get('hour', 8))

    if not email or not target:
        return jsonify({"error": "Email et cible requis."}), 400
    if frequency not in FREQUENCY_CRON:
        return jsonify({"error": "Fréquence invalide."}), 400
    if not (0 <= hour <= 23):
        return jsonify({"error": "Heure invalide (0-23)."}), 400

    subscribers = load_subscribers()

    # Mise à jour si déjà abonné pour ce couple email+target
    for sub in subscribers:
        if sub['email'] == email and sub['target'] == target:
            sub['frequency'] = frequency
            sub['hour']      = hour
            save_subscribers(subscribers)
            schedule_subscriber_job(sub)
            freq_label = FREQUENCY_LABEL.get(frequency, frequency)
            return jsonify({
                "status":  "updated",
                "message": f"Surveillance mise à jour : {freq_label} à {hour:02d}:00."
            }), 200

    new_sub = {'email': email, 'target': target, 'frequency': frequency, 'hour': hour}
    subscribers.append(new_sub)
    save_subscribers(subscribers)
    schedule_subscriber_job(new_sub)

    freq_label = FREQUENCY_LABEL.get(frequency, frequency)
    return jsonify({
        "status":  "subscribed",
        "message": f"Surveillance activée : {freq_label} à {hour:02d}:00 pour {target}."
    }), 201


@app.route('/api/unsubscribe', methods=['POST'])
def unsubscribe():
    data   = request.json
    email  = data.get('email', '').strip()
    target = data.get('target', '').strip()

    subscribers = load_subscribers()
    updated     = [s for s in subscribers if not (s['email'] == email and s['target'] == target)]

    if len(updated) == len(subscribers):
        return jsonify({"error": "Abonnement introuvable."}), 404

    save_subscribers(updated)

    job_id = _job_id(email, target)
    if scheduler.get_job(job_id):
        scheduler.remove_job(job_id)

    print(f"[UNSUBSCRIBE] Désabonné : {email} → {target}")
    return jsonify({"status": "unsubscribed"}), 200


# =========================================================
# --- DÉMARRAGE DU SCHEDULER ---
# =========================================================

scheduler = BackgroundScheduler(timezone="Europe/Paris")

# Recharge tous les jobs existants au démarrage
for sub in load_subscribers():
    schedule_subscriber_job(sub)

scheduler.start()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
