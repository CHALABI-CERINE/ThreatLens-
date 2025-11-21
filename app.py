from flask import Flask, render_template, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import feedparser
import random
import logging

# --- CONFIGURATION ---
logging.basicConfig(level=logging.INFO)
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///threatlens.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# --- DATABASE MODEL (THREATS) ---
class Threat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    source = db.Column(db.String(50))      # e.g., NVD, HackerNews
    title = db.Column(db.String(255))
    link = db.Column(db.String(500))
    published_date = db.Column(db.String(50))
    summary = db.Column(db.Text)
    
    # NLP Classified Fields
    threat_type = db.Column(db.String(50)) # Malware, CVE, Phishing, DDoS
    severity = db.Column(db.String(20))    # Critical, High, Medium, Low
    threat_score = db.Column(db.Integer)   # 0 to 100
    target_sector = db.Column(db.String(50)) # Finance, Gov, Health, General

# --- DATA SOURCES (Real Cyber Feeds) ---
FEEDS = {
    'TheHackerNews': 'https://feeds.feedburner.com/TheHackersNews',
    'BleepingComputer': 'https://www.bleepingcomputer.com/feed/',
    'CISA Alerts': 'https://www.cisa.gov/uscert/ncas/alerts.xml',
    'ThreatPost': 'https://threatpost.com/feed/'
}

# --- NLP & CLASSIFICATION ENGINE ---
def analyze_threat(title, summary):
    text = (title + " " + summary).lower()
    
    # 1. IDENTIFY TYPE
    t_type = "General"
    if 'ransomware' in text: t_type = "Ransomware"
    elif 'phishing' in text: t_type = "Phishing"
    elif 'ddos' in text: t_type = "DDoS"
    elif 'cve' in text or 'vulnerability' in text: t_type = "Vulnerability (CVE)"
    elif 'botnet' in text: t_type = "Botnet"
    elif 'leak' in text or 'breach' in text: t_type = "Data Breach"

    # 2. CALCULATE SEVERITY & SCORE
    score = random.randint(10, 40) # Base noise
    severity = "Low"
    
    # Keywords that boost score
    critical_words = ['zero-day', 'rce', 'critical', 'exploit', 'active attack', 'unpatched']
    high_words = ['malware', 'backdoor', 'root', 'admin', 'bank', 'password']
    
    if any(w in text for w in critical_words):
        score += 50
        severity = "Critical"
    elif any(w in text for w in high_words):
        score += 30
        severity = "High"
    elif 'update' in text or 'patch' in text:
        score += 10
        severity = "Medium"
        
    # Cap score at 100
    if score > 100: score = 100
    
    # 3. IDENTIFY SECTOR
    sector = "General"
    if 'bank' in text or 'finance' in text: sector = "Finance"
    elif 'hospital' in text or 'health' in text: sector = "Healthcare"
    elif 'government' in text or 'federal' in text: sector = "Government"
    
    return t_type, severity, score, sector

# --- ROUTES ---
@app.route('/')
@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html', page="dashboard", user="CHALABI-CERINE", date=datetime.utcnow().strftime("%Y-%m-%d %H:%M"))

@app.route('/intel')
def intel():
    return render_template('intel.html', page="intel", user="CHALABI-CERINE", date=datetime.utcnow().strftime("%Y-%m-%d %H:%M"))

@app.route('/reports')
def reports():
    return render_template('reports.html', page="reports", user="CHALABI-CERINE", date=datetime.utcnow().strftime("%Y-%m-%d %H:%M"))

@app.route('/api/scan', methods=['POST'])
def scan_feeds():
    new_count = 0
    for source_name, url in FEEDS.items():
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries[:4]: # Grab top 4
                if not Threat.query.filter_by(link=entry.link).first():
                    summary = entry.get('summary', entry.get('description', ''))
                    t_type, severity, score, sector = analyze_threat(entry.title, summary)
                    
                    threat = Threat(
                        source=source_name, title=entry.title, link=entry.link,
                        published_date=entry.get('published', datetime.now().strftime("%Y-%m-%d")),
                        summary=summary[:300], threat_type=t_type, severity=severity,
                        threat_score=score, target_sector=sector
                    )
                    db.session.add(threat)
                    new_count += 1
        except: continue
    db.session.commit()
    return jsonify({'status': 'success', 'count': new_count})

@app.route('/api/data')
def get_data():
    threats = Threat.query.order_by(Threat.id.desc()).limit(50).all()
    all_t = Threat.query.all()
    
    stats = {
        'total': len(all_t),
        'critical': sum(1 for t in all_t if t.severity == 'Critical'),
        'avg_score': round(sum(t.threat_score for t in all_t) / len(all_t)) if len(all_t) > 0 else 0,
        'types': {}
    }
    
    # Count types for charts
    for t in all_t:
        stats['types'][t.threat_type] = stats['types'].get(t.threat_type, 0) + 1
        
    data = [t.__dict__ for t in threats]
    for d in data: d.pop('_sa_instance_state', None)
    
    return jsonify({'stats': stats, 'threats': data})

if __name__ == '__main__':
    with app.app_context(): db.create_all()
    app.run(debug=True, port=5001) # Running on port 5001 to avoid conflict