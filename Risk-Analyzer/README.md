# Digital Identity Fragmentation Risk Analyzer

An advanced cybersecurity tool designed to analyze the distribution of a person's digital identity across multiple platforms and evaluate the security risks caused by identity fragmentation and attribute reuse.

## 🚀 Features
- **Real-time Risk Engine:** Computes a Risk Score (0-100) based on platform volume, attribute duplication, and password strength.
- **Identity Fragmentation Detection:** Identifies how many platforms share the same Email, Phone, or Username.
- **Visual Analytics:** Interactive dashboards showing platform distribution and security hygiene.
- **Hybrid Data Entry:** Supports both manual entry and bulk CSV dataset uploads.
- **Security Recommendations:** Dynamically generated advice based on the detected threat level.

## 🛠️ Tech Stack
- **Backend:** Python 3.x, Flask (Web Server), Pandas (Data Analysis)
- **Frontend:** HTML5, CSS3 (SaaS Theme), JavaScript (Chart.js)
- **Storage:** CSV-based local database for portability and transparency.

## 📊 Risk Scoring Algorithm
The system evaluates risk using three primary pillars:
1. **Surface Area:** Increasing platforms increases the probability of a data breach.
2. **Fragmentation (Re-use):** High reuse of a single email/phone across 10+ platforms creates a single point of failure.
3. **Hygiene:** Presence of "Weak" passwords significantly boosts the risk score.

## 📁 Project Structure
```text
Risk-Analyzer/
├── app.py              # Flask Application & Routes
├── analyzer.py         # Logic for Risk & Fragmentation analysis
├── sample_identities.csv # Mock data for testing
├── templates/          # Jinja2 HTML Templates
├── static/             # CSS & JS assets
└── data/               # Persistent identity storage
```

## 📋 Instructions
1. Install requirements: `pip install -r requirements.txt`
2. Run the application: `python app.py`
3. Access at: `http://127.0.0.1:5000`

---
*Developed for AI/ML & Cybersecurity Competitions.*
