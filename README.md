# 🛡️ Agentic AI Honeypot for Scam Detection

An AI-powered **honeypot system** designed to simulate a vulnerable user and intelligently interact with scammers to analyze scam patterns and gather threat intelligence.

This project was built during the **India AI Impact Buildathon 2026**.

---

# 🚀 Overview

Most scam detection systems focus on **blocking attackers after detection**.

This project explores a different approach:

Instead of immediately blocking scammers, the system **engages them in conversation**, behaves like a confused user, and collects useful information about scam techniques.

The goal is to:

- Analyze scam strategies
- Waste attacker time
- Collect threat intelligence
- Understand scam behavior patterns

---

# 🎯 Objectives

- Detect potential scam messages
- Automatically respond using an AI agent
- Simulate realistic user conversations
- Analyze scammer behavior
- Collect structured scam interaction data

---

# 🧠 Key Features

## 🤖 AI Agent Interaction
The honeypot responds like a real user and keeps scammers engaged through natural conversation.

## 🧪 Scam Scenario Simulation
The system supports multiple scam scenarios such as:

- Bank KYC scams  
- Government subsidy scams  
- OTP verification scams  
- Refund and reward scams  

## 🔍 Threat Intelligence Collection
The system records:

- scammer messages
- response patterns
- conversation flow
- engagement duration

## ⏳ Engagement Strategy
The agent uses tactics like:

- confusion
- asking repeated questions
- requesting clarification
- pretending lack of technical knowledge

This **extends scammer interaction time** and increases intelligence collection.

---

# 🏗️ Tech Stack

**Backend**
- FastAPI
- Python

**AI Logic**
- Rule-based conversational agent
- Scam pattern simulation

**Deployment**
- Render

**Version Control**
- GitHub

---

# 📂 Project Structure
agentic-honeypot-guvi
│
├── main.py # FastAPI server
├── requirements.txt # Python dependencies
├── README.md # Project documentation
└── logs/ # Interaction logs


---

# ⚡ Installation

Clone the repository
git clone https://github.com/SuryaanshPandey/agentic-honeypot-guvi.git

cd agentic-honeypot-guvi


Install dependencies
pip install -r requirements.txt


Run the server
uvicorn main:app --reload


Server will start at:
http://127.0.0.1:8000


---

# 📡 API Usage

### Endpoint
POST /honeypot


### Example Request

```json
{
  "message": "Your bank KYC is expired. Update immediately."
}
```

### Example Response

```json
{
  "reply": "Oh really? I don't remember getting any notification from my bank."
}
```

### 🧪 Example Scam Conversation

Scammer
Your PM Government subsidy of ₹8000 is approved.
Agent
I don't remember applying for this. Which department is this?
Scammer
Benefits department, Delhi.
Agent
Oh okay. How will I receive the money?

### 📊 Future Improvements

LLM-powered dynamic scam conversations

Scam classification model

Automated scam dataset generation

Real-time threat analytics dashboard

Advanced attacker behavior profiling



### 🏆 Buildathon

This project was developed during:

India AI Impact Buildathon 2026
at the AI Impact Summit

### 👨‍💻 Author

Suryaansh Pandey

BTech Student | AI Builder | Founder of DMCOI

### GitHub
https://github.com/SuryaanshPandey

### 📜 License

This project is intended for educational and research purposes.
