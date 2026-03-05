🛡️ Agentic AI Honeypot for Scam Detection

An AI-powered honeypot system that simulates a vulnerable user and intelligently interacts with scammers to analyze scam patterns, collect threat intelligence, and delay attackers.

Built during the India AI Impact Buildathon 2026.

🚀 Overview

Traditional scam detection systems only block attackers after detection.
This project takes a different approach:

Instead of blocking scammers immediately, the system engages them in conversation, gathers behavioral signals, and extracts intelligence about scam techniques.

The honeypot behaves like a confused or vulnerable user to keep scammers engaged longer.

🎯 Objectives

Detect and analyze scam conversations

Engage attackers automatically using AI-generated responses

Collect threat intelligence

Waste attacker time

Build a dataset of real scam strategies

🧠 Key Features
🤖 AI Agent Interaction

The honeypot acts like a real user and responds naturally to scammers.

🧪 Scam Simulation

Predefined conversation flows simulate scenarios such as:

Bank KYC scams

Government subsidy scams

OTP scams

Refund scams

🔍 Threat Intelligence

The system logs:

scammer messages

behavioral patterns

conversation history

⚙️ Engagement Strategy

The agent uses tactics like:

confusion

repeated clarification

fake delays

asking irrelevant questions

to extend scammer interaction time.

🏗️ Tech Stack

Backend

FastAPI

Python

AI / Logic

Rule based conversational flows

Pattern detection

Deployment

Render

Version Control

GitHub

📂 Project Structure
agentic-honeypot
│
├── main.py              # FastAPI application
├── requirements.txt     # Dependencies
├── README.md            # Project documentation
└── logs/                # Interaction logs
⚡ Installation

Clone the repository

git clone https://github.com/SuryaanshPandey/agentic-honeypot-guvi.git
cd agentic-honeypot-guvi

Install dependencies

pip install -r requirements.txt

Run the server

uvicorn main:app --reload

Server will run at

http://127.0.0.1:8000
📡 API Usage
POST Request

Endpoint

/honeypot

Example Request

{
  "message": "Your bank KYC is expired. Update now."
}

Example Response

{
  "reply": "Oh really? I don't remember getting any message from my bank."
}
🧪 Example Scam Scenario

Scammer

Your PM government subsidy of ₹8000 is approved.

Agent

I don't remember applying for this. Which department is this?

Scammer

Benefits department, Delhi.

Agent

Oh okay. How will I receive the money?

📊 Future Improvements

LLM powered dynamic conversations

Scam classification model

Real-time scammer fingerprinting

Dashboard for threat analytics

Automated scam dataset generation

🏆 Buildathon

This project was developed during:

India AI Impact Buildathon 2026
at the AI Impact Summit

👨‍💻 Author

Suryaansh Pandey

BTech Student | AI Builder | Founder – DMCOI

GitHub
https://github.com/SuryaanshPandey

📜 License

This project is for research and educational purposes.
