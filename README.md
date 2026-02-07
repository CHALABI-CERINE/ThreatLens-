# 🔍 ThreatLens

An intelligent cybersecurity threat detection and analysis platform using Natural Language Processing (NLP) and machine learning to identify, categorize, and alert on security threats.

## 🛡️ Overview

ThreatLens is a Python-based security monitoring system that collects, analyzes, and processes threat intelligence data. It uses NLP techniques to extract meaningful insights from security logs and alerts, helping security teams stay ahead of potential threats.

## ✨ Key Features

- **Automated Threat Collection**: Continuous monitoring and data gathering
- **NLP-Powered Analysis**: Advanced text processing for threat intelligence
- **Real-time Alerts**: Immediate notification system for critical threats
- **Docker Support**: Containerized deployment for easy scaling
- **Web Dashboard**: Flask-based interface for threat visualization
- **Configurable Rules**: YAML-based configuration for custom threat detection

## 🏗️ Project Architecture

```
ThreatLens/
├── app.py                 # Flask web application
├── collector.py           # Threat data collection module
├── nlp_pipeline.py        # NLP processing engine
├── alerts.py              # Alert management system
├── utils.py               # Utility functions
├── init_data.py           # Database initialization
├── config.yaml            # Configuration file
├── requirements.txt       # Python dependencies
├── Dockerfile             # Container configuration
├── docker-compose.yml     # Multi-container setup
└── src/                   # Source code modules
```

## 🛠️ Technology Stack

- **Backend**: Python (75.3%)
- **Web Framework**: Flask
- **Frontend**: HTML (16.2%), JavaScript (6.8%), CSS (0.5%)
- **NLP**: Natural Language Processing libraries
- **Containerization**: Docker (1.2%)
- **Configuration**: YAML

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Docker & Docker Compose (optional)
- pip package manager

### Installation

```bash
# Clone the repository
git clone https://github.com/CHALABI-CERINE/ThreatLens.git
cd ThreatLens

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Initialize database
python init_data.py

# Run the application
python app.py
```

### Docker Deployment

```bash
# Build and run with Docker Compose
docker-compose up -d

# Access the dashboard
# Visit http://localhost:5000
```

## 📋 Configuration

Edit `config.yaml` to customize threat detection:

```yaml
# Threat sources
sources:
  - type: "log_files"
    path: "/var/log/security"
  - type: "api"
    endpoint: "https://threat-feed.example.com"

# Alert settings
alerts:
  email: "security@example.com"
  severity_threshold: "medium"
  
# NLP settings
nlp:
  model: "threat_detection_v1"
  confidence_threshold: 0.75
```

## 🔍 Core Modules

### Collector (`collector.py`)
- Gathers threat intelligence from multiple sources
- Supports log files, APIs, and data feeds
- Normalizes data for processing

### NLP Pipeline (`nlp_pipeline.py`)
- Text analysis and feature extraction
- Threat categorization
- Sentiment analysis for severity assessment
- Entity recognition for IOCs (Indicators of Compromise)

### Alerts (`alerts.py`)
- Multi-channel notification system
- Email and webhook support
- Alert prioritization and deduplication
- Integration with incident response tools

### Web Dashboard (`app.py`)
- Real-time threat visualization
- Historical data analysis
- Alert management interface
- System configuration

## 📊 Features in Detail

### Threat Detection
- Malware signatures
- Suspicious patterns
- Anomaly detection
- Zero-day threat indicators

### NLP Capabilities
- Automated threat classification
- Context-aware analysis
- Multi-language support
- Custom rule creation

### Alerting System
- Severity-based prioritization
- Customizable alert rules
- Integration capabilities
- Alert escalation workflows

## 🔐 Security Considerations

- Secure credential storage
- Encrypted communications
- Access control and authentication
- Audit logging
- Regular security updates

## 📈 Use Cases

- SOC (Security Operations Center) monitoring
- Threat intelligence gathering
- Incident response automation
- Security research and analysis
- Compliance monitoring

## 🧪 Testing

```bash
# Run unit tests
python -m pytest tests/

# Run with coverage
pytest --cov=src tests/
```



## 📝 Current Issues

Check the [Issues](https://github.com/CHALABI-CERINE/ThreatLens/issues) section for known bugs and feature requests (2 open issues).

## 🗺️ Roadmap

- [ ] Machine learning model integration
- [ ] Advanced threat correlation
- [ ] Mobile application
- [ ] Integration with SIEM platforms
- [ ] Threat hunting automation

## 👤 Author

**CHALABI CERINE**

## 📄 License

This project is for educational and research purposes.

---

🛡️ **Detecting threats before they become problems!**

---

**⚠️ Note**: This is a private repository focused on cybersecurity research and development.
