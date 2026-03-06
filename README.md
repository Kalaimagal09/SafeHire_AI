# 🛡️ SafeHire AI: Enterprise HR Compliance Engine

**Built by Team Supernova for Hackathon Problem Statement 21**

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)](https://fastapi.tiangolo.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.25+-red.svg)](https://streamlit.io/)
[![Scikit-Learn](https://img.shields.io/badge/scikit--learn-Machine%20Learning-orange.svg)](https://scikit-learn.org/)

SafeHire AI is a predictive, privacy-first enterprise software suite designed for **Human Resources (HR) teams and Corporate Recruiters**. It actively prevents interviewers from asking illegal or non-compliant interview questions (e.g., age, marital status, pregnancy, religion) that result in costly discrimination lawsuits and PR damage.

🎥 **[Watch our 2-Minute Demo Video Here](Insert_Your_Video_Link_Here)**

---

## 👥 The HR Problem & Our Novelty

Standard HR compliance currently relies on passive training modules or invasive AI bots that record candidate audio—creating massive data privacy liabilities. 

**SafeHire AI solves this with a 3-Pillar Approach:**

1. **Active HR Interception:** We transform compliance from a yearly training video into an active safety net that lives *inside* the interview.
2. **Predictive Mid-Sentence Warnings:** Our Chrome Extension uses interim edge-speech processing to catch dangerous sentence trajectories, flashing a warning *before* the recruiter fully speaks the illegal thought.
3. **Zero-Storage Edge Privacy:** We strictly monitor the recruiter's local microphone. Candidate audio is never recorded, ensuring 100% compliance with corporate data privacy laws.

---

## 🏗️ The HR Ecosystem (System Architecture)

SafeHire AI is an API-first platform featuring two primary frontends connected to a central NLP (Natural Language Processing) brain.

* **Phase 1: Pre-Interview HR Portal (Streamlit):** A web dashboard for HR Directors to bulk-audit standardized CSV interview scripts, instantly generating litigation risk scores across the company.
* **Phase 2: Live Edge Monitor (Chrome Extension):** A lightweight browser extension equipping recruiters with a real-time AI co-pilot during Google Meet or Zoom Web calls.
* **The AI Engine (FastAPI & Scikit-Learn):** An asynchronous Python API running a custom **Logistic Regression** model trained explicitly on official university Human Resources legal guidelines.

---

## 💻 Tech Stack

* **Machine Learning:** Scikit-Learn, Pandas, Joblib, TF-IDF NLP
* **Backend API:** FastAPI, Uvicorn, Python
* **HR Web Dashboard:** Streamlit
* **Live Edge Extension:** HTML, CSS, Vanilla JavaScript, Web Speech API

---

## ⚙️ Local Installation & Setup

### 1. Clone the Repository
```bash
git clone [https://github.com/YourUsername/SafeHire-AI.git](https://github.com/YourUsername/SafeHire-AI.git)
cd SafeHire-AI
